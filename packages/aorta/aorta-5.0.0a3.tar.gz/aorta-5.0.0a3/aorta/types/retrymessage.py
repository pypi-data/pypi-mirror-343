from typing import Any
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aorta import MessageHandler


class RetryMessage(Exception):

    @property
    def qualname(self):
        return self.handler.qualname

    def __init__(self, handler: 'MessageHandler[Any]'):
        self.handler = handler