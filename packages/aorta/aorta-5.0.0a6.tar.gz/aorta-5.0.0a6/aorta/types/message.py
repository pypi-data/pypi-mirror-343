# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import ClassVar
from typing import Self
from typing import Union
from typing import TYPE_CHECKING

import pydantic

from .envelope import Envelope
from .messageheader import MessageHeader
if TYPE_CHECKING:
    from .messagemetadata import MessageMetadata


class Message(pydantic.BaseModel):
    api_version: ClassVar[str]
    api_group: ClassVar[str]
    __abstract__: ClassVar[bool] = True
    __envelope__: ClassVar[type[Envelope[Any]]] = Envelope
    __message_attr__: ClassVar[str]
    __message_type__: ClassVar[str]
    __registry__: ClassVar[dict[tuple[str, str], type[Self]]]
    __version__: ClassVar[str] = 'v1'

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any):
        k: tuple[str, str] = (cls.api_version, cls.__name__)
        if k in cls.__registry__:
            raise TypeError('Message {0}/{1} is already registered.'.format(*k))
        cls.__envelope__ = cls.__registry__[k] = type( # type: ignore
            f'{cls.__name__}Envelope',
            (cls.__envelope__,), # type: ignore
            {
                '__annotations__': {
                    cls.__message_attr__: cls
                }
            }
        )

    @classmethod
    def parse(cls: type[Any], data: Any) -> Envelope[Any] | MessageHeader | None:
        header = None
        try:
            header = MessageHeader.model_validate(data)
            if header.type == cls.__message_type__:
                return cls.__registry__[(header.api_version, header.kind)].model_validate(data)
        except (KeyError, pydantic.ValidationError, TypeError, ValueError):
            return header

    def __init_subclass__(cls, group: str = '', version: str = 'v1', **kwargs: pydantic.ConfigDict):
        group = group or getattr(cls, 'api_group', group)
        version = str.split(getattr(cls, 'api_version', version), '/')[-1]
        cls.api_group = group
        cls.api_version = version
        if group and version:
            cls.api_version = f'{cls.api_group}/{cls.api_version}'
        return super().__init_subclass__(**kwargs) # type: ignore

    def envelope(
        self,
        correlation_id: str | None = None,
        audience: set[str] | None = None,
        labels: dict[str, str | None] | None = None,
        annotations: dict[str, str | None] | None = None,
        namespace: str = '',
        metadata: Union['MessageMetadata', None] = None
    ) -> Envelope[Self]:
        return self.__envelope__.model_validate({
            'apiVersion': self.api_version,
            'kind': type(self).__name__,
            'type': self.__message_type__,
            'metadata': metadata or {
                'annotations': annotations or {},
                'audience': audience or set(),
                'correlationId': correlation_id,
                'labels': labels or {},
                'namespace': namespace
            },
            self.__message_attr__: self.model_dump()
        })