from typing import Union, overload

from eth_typing import HexStr

from checksum_dict._utils import to_bytes


class HexBytes(bytes):
    """
    A thin wrapper around the Python built-in :class:`bytes` class for handling hexadecimal bytes.

    This class provides additional functionality for initializing with various types and
    representing the bytes in a hexadecimal format with a '0x' prefix.

    Examples:
        Create a HexBytes object from a hex string:

        >>> hb = HexBytes("0x1234")
        >>> print(hb)
        HexBytes('0x1234')

        Create a HexBytes object from an integer:

        >>> hb = HexBytes(4660)
        >>> print(hb)
        HexBytes('0x1234')

    See Also:
        - :func:`to_bytes` for converting various types to bytes.
    """

    def __new__(cls, val: Union[bool, bytearray, bytes, int, str]) -> "HexBytes":
        return super().__new__(cls, to_bytes(val))

    def hex(self) -> HexStr:  # type: ignore [override]
        """
        Output hex-encoded bytes, with an "0x" prefix.

        Everything following the "0x" is output exactly like :meth:`bytes.hex`.

        Examples:
            >>> hb = HexBytes("0x1234")
            >>> hb.hex()
            '0x1234'
        """
        return f"0x{super().hex()}"  # type: ignore [return-value]

    @overload  # type: ignore [override]
    def __getitem__(self, key: int) -> int: ...

    @overload  # noqa: F811
    def __getitem__(self, key: slice) -> "HexBytes": ...

    def __getitem__(self, key: Union[int, slice]) -> Union[int, bytes, "HexBytes"]:  # noqa: F811
        result = super().__getitem__(key)
        if hasattr(result, "hex"):
            return type(self)(result)
        else:
            return result

    def __repr__(self) -> str:
        return f"HexBytes({self.hex()!r})"
