"""`amplifai.examples` module."""

from typing import Generic, TypeVar

from pydantic import BaseModel

Schema = TypeVar("Schema", bound=BaseModel)


class Example(BaseModel, Generic[Schema]):
    """`amplifier.examples.Example` class.

    A representation of an example. An example consists of a text input and the expected objects that should be extracted from the text.

    Args:
        input: str
            The example text.
        outputs: list[Schema]
            The expected objects that should be extracted from the text.
    """

    input: str  # This is the example text
    outputs: list[Schema]  # Instances of pydantic model that should be extracted


class Examples(BaseModel, Generic[Schema]):
    """`amplifier.examples.Examples` class.

    A collection of examples.
    """

    examples: list[Example[Schema]]
