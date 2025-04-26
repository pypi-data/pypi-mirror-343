from collections.abc import Sequence
from typing import Protocol

type Data = (
    Sequence[tuple[int, int, int]]
    | Sequence[tuple[int, int, int, int]]
    | Sequence[int]
    | bytes
    | bytearray
)

class Image(Protocol):
    @property
    def width(self) -> int: pass
    @property
    def height(self) -> int: pass
    @property
    def data(self) -> bytes: pass
    @property
    def channels(self) -> int: pass
    @property
    def colorspace(self) -> str: pass
    @property
    def mode(self) -> str: pass
