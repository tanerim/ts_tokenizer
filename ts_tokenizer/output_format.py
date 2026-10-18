"""Output formats shared by the Python API and command-line interface."""

from enum import Enum
from typing import Literal, Union


class OutputFormat(str, Enum):
    """Select the representation returned by :func:`tokenize`."""

    TOKENIZED = "tokenized"
    LINES = "lines"
    TAGGED = "tagged"
    TAGGED_LINES = "tagged_lines"

    def __str__(self) -> str:
        return self.value


OutputFormatLike = Union[
    OutputFormat, Literal["tokenized", "lines", "tagged", "tagged_lines"]
]
