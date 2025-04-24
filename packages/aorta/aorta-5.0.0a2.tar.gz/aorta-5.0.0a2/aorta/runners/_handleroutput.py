from typing import Any

import pydantic

from aorta.types import RetryMessage


class HandlerOutput(pydantic.BaseModel):
    success: bool
    output: Any

    def is_retry(self):
        return isinstance(self.output, RetryMessage)

    def __bool__(self):
        return self.success