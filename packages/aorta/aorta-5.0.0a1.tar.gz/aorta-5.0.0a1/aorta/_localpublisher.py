# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
from typing import Any
from typing import Callable
from typing import Iterable

from aorta.types import Envelope
from aorta.types import IPublisher
from aorta.types import IRunner
from aorta.types import Message
from aorta.types import MessageHeader
from aorta.types import IMessageHandler
from .transaction import Transaction


class LocalPublisher(IPublisher):
    """A publisher implementation that publishes and runs messages in
    the local process and thread.
    """
    __module__: str = 'aorta'

    def __init__(
        self,
        provider: Callable[[Envelope[Any] | MessageHeader, bool, Iterable[str] | None], Iterable[type[IMessageHandler]]],
        runner: IRunner
    ) -> None:
        self.provider = provider
        self.runner = runner

    def begin(self):
        return Transaction(publisher=self)

    async def publish(
        self,
        message: Message,
        **kwargs: Any
    ) -> None:
        envelope = message.envelope()
        await self.runner.run(
            publisher=self,
            envelope=envelope,
            handlers=set(self.provider(envelope, False, None)),
        )

    async def send(
        self,
        messages: list[Envelope[Any]],
        is_retry: bool = False
    ):
        await asyncio.gather(*[
            self.runner.run(
                publisher=self,
                envelope=m,
                handlers=self.provider(m, False, m.metadata.handlers),
            )
            for m in messages
        ])