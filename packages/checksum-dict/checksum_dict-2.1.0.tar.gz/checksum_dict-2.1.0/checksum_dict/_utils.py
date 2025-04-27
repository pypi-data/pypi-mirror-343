"""
This library was built to have minimal dependencies, to minimize dependency conflicts for users.
The following code was ripped out of eth-brownie on 2022-Aug-06.
A big thanks to the many maintainers and contributors for their valuable work!
"""

import binascii
from typing import Final, Union

import cchecksum  # type: ignore [import-not-found]
from eth_typing import ChecksumAddress, HexStr  # type: ignore [import-not-found]

from checksum_dict import _hexbytes


HexBytes: Final = _hexbytes.HexBytes


to_checksum_address: Final = cchecksum.to_checksum_address
unhexlify: Final = binascii.unhexlify


def checksum_value(value: Union[str, bytes]) -> ChecksumAddress:
    if isinstance(value, bytes):
        converted_value = (
            value.hex() if type(value).__name__ == "HexBytes" else HexBytes(value).hex()
        )
    else:
        converted_value = add_0x_prefix(str(value))
    try:
        return to_checksum_address(converted_value)
    except ValueError as e:
        raise ValueError(f"'{converted_value}' is not a valid ETH address") from e


def add_0x_prefix(value: str) -> HexStr:
    return value if value.startswith(("0x", "0X")) else f"0x{value}"  # type: ignore [return-value]


def to_bytes(val: Union[bool, bytearray, bytes, int, str]) -> bytes:
    """
    Convert a value to its bytes representation.

    This function is equivalent to `eth_utils.hexstr_if_str(eth_utils.to_bytes, val)`.
    It can convert a hex string, integer, or boolean to a bytes representation.
    Alternatively, it passes through bytes or bytearray as a bytes value.

    Args:
        val: The value to convert, which can be a bool, bytearray, bytes, int, or str.

    Raises:
        ValueError: If the integer is negative.
        TypeError: If the value is of an unsupported type.

    Examples:
        Convert a hex string to bytes:

        >>> to_bytes("0x1234")
        b'\x124'

        Convert an integer to bytes:

        >>> to_bytes(4660)
        b'\x124'

        Convert a boolean to bytes:

        >>> to_bytes(True)
        b'\x01'
    """
    if isinstance(val, bytes):
        return val
    elif isinstance(val, str):
        return hexstr_to_bytes(val)
    elif isinstance(val, bytearray):
        return bytes(val)
    elif isinstance(val, bool):
        return b"\x01" if val else b"\x00"
    elif isinstance(val, int):
        # Note that this int check must come after the bool check, because
        #   isinstance(True, int) is True
        if val < 0:
            raise ValueError(f"Cannot convert negative integer {val} to bytes")
        else:
            return to_bytes(hex(val))
    else:
        raise TypeError(f"Cannot convert {val!r} of type {type(val)} to bytes")


def hexstr_to_bytes(hexstr: str) -> bytes:
    """
    Convert a hex string to bytes.

    Args:
        hexstr: The hex string to convert.

    Raises:
        ValueError: If the hex string contains invalid characters.

    Examples:
        Convert a hex string with a prefix:

        >>> hexstr_to_bytes("0x1234")
        b'\x124'

        Convert a hex string without a prefix:

        >>> hexstr_to_bytes("1234")
        b'\x124'
    """
    if hexstr.startswith("0x") or hexstr.startswith("0X"):
        non_prefixed_hex = hexstr[2:]
    else:
        non_prefixed_hex = hexstr

    # if the hex string is odd-length, then left-pad it to an even length
    if len(hexstr) % 2:
        padded_hex = "0" + non_prefixed_hex
    else:
        padded_hex = non_prefixed_hex

    try:
        ascii_hex = padded_hex.encode("ascii")
    except UnicodeDecodeError:
        raise ValueError(f"hex string {padded_hex} may only contain [0-9a-fA-F] characters")
    else:
        return unhexlify(ascii_hex)
