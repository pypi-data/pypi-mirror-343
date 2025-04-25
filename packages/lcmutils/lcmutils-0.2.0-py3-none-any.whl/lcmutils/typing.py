from collections.abc import Callable
from typing import BinaryIO, Protocol, Any, runtime_checkable


@runtime_checkable
class LCMType(Protocol):
    """
    LCM type protocol to support static duck typing for LCM type classes generated via lcm-gen.
    """

    def encode(self) -> bytes: ...

    def _encode_one(self, buf: BinaryIO): ...

    @staticmethod
    def decode(data: bytes) -> "LCMType": ...

    @staticmethod
    def _decode_one(buf: BinaryIO) -> "LCMType": ...

    @staticmethod
    def _get_hash_recursive(parents: list[Any]) -> int: ...

    @staticmethod
    def _get_packed_fingerprint() -> bytes: ...

    def get_hash(self) -> int: ...


class LCMHandler(Callable[[str, bytes], None]):
    """
    LCM message handler type.
    """


__all__ = ["LCMType", "LCMHandler"]
