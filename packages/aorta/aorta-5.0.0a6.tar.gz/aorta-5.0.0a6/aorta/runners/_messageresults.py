import pydantic

from ._handleroutput import HandlerOutput


class MessageResults(pydantic.BaseModel):
    outputs: list[HandlerOutput]

    def __bool__(self):
        return all(self.outputs)