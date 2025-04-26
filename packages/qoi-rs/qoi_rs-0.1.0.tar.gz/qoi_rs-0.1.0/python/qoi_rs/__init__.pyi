from ._types import Image, Data

def encode(data: Data, /, *, width: int, height: int) -> bytes:
    pass

def decode(data: bytes, /) -> Image:
    pass

__all__ = "encode", "decode", "Image"
