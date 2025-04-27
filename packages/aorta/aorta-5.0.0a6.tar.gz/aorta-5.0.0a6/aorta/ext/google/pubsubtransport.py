# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import functools
import json
import logging
from typing import Any
from typing import AsyncIterable
from typing import Callable

from google.api_core.retry import Retry
from google.api_core.exceptions import NotFound
from google.api_core.exceptions import PermissionDenied
from google.api_core.exceptions import ResourceExhausted
from google.auth.impersonated_credentials import Credentials as ImpersonatedCredentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google.cloud import pubsub_v1 # type: ignore

import aorta
from aorta.types import Envelope


class PubsubTransport:
    __module__: str = 'aorta.ext.google'
    client: pubsub_v1.PublisherClient
    logger: logging.Logger = logging.getLogger(__name__)
    max_pull_messages: int = 1000
    retry_topic: str | None
    topic: str | list[str] | Callable[..., list[str]]

    def __init__(
        self,
        *,
        project: str,
        topic: str | list[str] | Callable[..., list[str]],
        retry_topic: str | None = None,
        credentials: ServiceAccountCredentials | ImpersonatedCredentials | None = None,
        pclient: pubsub_v1.PublisherClient | None = None,
        sclient: pubsub_v1.SubscriberClient | None = None,
        logger: logging.Logger | None = None
    ):
        """Initialize a new :class:`GoogleTransport`:

        Args:
            project: the name of the Google Cloud project.
            topic_path: either a string, list of string, or a callable that
                returns a string or list of strings, that specify the topic
                to which messages must be published.
        """
        self.logger = logger or self.logger
        self.pclient = pclient or pubsub_v1.PublisherClient(credentials=credentials)
        self.sclient = sclient or pubsub_v1.SubscriberClient(credentials=credentials)
        self.project = project
        self.retry_topic = retry_topic
        self.topic = topic

    def get_topics(self, envelope: Envelope[Any], is_retry: bool = False) -> list[str]:
        """Return the list of topics to which the given `message` must be
        published.
        """
        topics: list[str] = []
        if is_retry and self.retry_topic:
            topics = [self.retry_topic]
        elif callable(self.topic):
            topics = self.topic(envelope)
        elif isinstance(self.topic, str):
            topics = [self.topic]
        elif isinstance(self.topic, list): # type: ignore
            topics = self.topic
        assert isinstance(topics, (str, list)) # nosec
        topics = [topics] if isinstance(topics, str) else topics
        return [self.pclient.topic_path(self.project, x) for x in topics]

    async def pull(
        self,
        channel: str,
        max_messages: int = 25,
        dry_run: bool = False
    ) -> AsyncIterable[Envelope[Any]]:
        loop = asyncio.get_running_loop()
        subscription = self.sclient.subscription_path(self.project, channel)
        while True:
            # TODO: Not threadsafe - will go horribly wrong. It is assumed that pull()
            # is not ran concurrently.
            pull = functools.partial(
                self.sclient.pull, # type: ignore
                subscription=subscription,
                return_immediately=True,
                max_messages=max_messages or self.max_pull_messages,
                retry=Retry(deadline=300)
            )
            try:
                response = await loop.run_in_executor(None, pull)
            except ResourceExhausted as e:
                self.logger.critical(e.message) # type: ignore
                break
            except NotFound:
                self.logger.critical("Subscription does not exist: %s", subscription)
                break
            if len(response.received_messages) == 0:
                self.logger.info("No messages received from %s", subscription)
                break
            if not dry_run:
                self.sclient.acknowledge( # type: ignore
                    subscription=subscription,
                    ack_ids=[message.ack_id for message in response.received_messages]
                )
            for wrapped in response.received_messages:
                try:
                    envelope = aorta.parse(json.loads(wrapped.message.data))
                    if not isinstance(envelope, Envelope) and envelope is not None:
                        self.logger.warning(
                            "Received unknown Aorta message: %s %s",
                            envelope.api_version,
                            envelope.kind
                        )
                        continue
                    if envelope is None:
                        # Envelope could not be parsed.
                        continue
                    yield envelope
                except (TypeError, ValueError, json.JSONDecodeError):
                    self.logger.warning('Dropping malformed message from %s', subscription)

    async def send(
        self,
        messages: list[Envelope[Any]],
        is_retry: bool = False
    ) -> None:
        futures: list[asyncio.Future[Any]] = []

        for envelope in messages:
            topics = self.get_topics(envelope, is_retry=is_retry)
            for topic in topics:
                futures.append(asyncio.ensure_future(self._send(topic, envelope)))
            await asyncio.gather(*futures)

    async def _send(self, topic: str, message: Envelope[Any]):
        future: asyncio.Future[Any] = asyncio.wrap_future(
            future=self.pclient.publish( # type: ignore
                topic=topic,
                data=bytes(message),
                api_group=message.api_group,
                api_version=message.api_version,
                kind=message.kind
            )
        )
        try:
            return await future
        except PermissionDenied:
            self.logger.critical(
                'Insufficient permission to publish to %s',
                topic
            )
        except NotFound:
            self.logger.critical(
                'Topic does not exist: %s',
                topic
            )