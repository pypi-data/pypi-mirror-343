# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
from typing import Any
from typing import Generic
from typing import TypeVar
from typing import TYPE_CHECKING

from .droppable import Droppable
from .messageheader import MessageHeader
if TYPE_CHECKING:
    from .message import Message


T = TypeVar('T', bound='Message')


class Envelope(MessageHeader, Droppable, Generic[T]):
    model_config = {'populate_by_name': True}

    @functools.cached_property
    def api_group(self):
        return self.message.api_group

    @property
    def header(self) -> MessageHeader:
        return MessageHeader.model_validate(self.model_dump())

    @property
    def message(self) -> T:
        return self.get_message()

    def clone(self, handler_class: type[Any]):
        envelope = self.model_validate(self.model_dump())
        envelope.metadata.handlers = [f'{handler_class.__module__}.{handler_class.__name__}']
        return envelope

    def model_dump(self, *args: Any, **kwargs: Any) -> Any:
        kwargs.setdefault('by_alias', True)
        return super().model_dump(*args, **kwargs)
    
    def get_message(self) -> T:
        raise NotImplementedError
    
    def is_bound(self) -> bool:
        return bool(self.metadata.handlers)

    def is_known(self) -> bool:
        """Return a boolean if the enclosed message is known."""
        return True

    def is_namespaced(self) -> bool:
        """Return a boolean indicating if the envelope is namespaced."""
        return bool(self.metadata.namespace)

    def wants(self, handler_class: type[Any]) -> bool:
        return self.metadata.handler == f'{handler_class.__module__}.{handler_class.__name__}'