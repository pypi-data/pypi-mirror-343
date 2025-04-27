from typing import TYPE_CHECKING, Final, Union, final, overload

from eth_typing import AnyAddress  # type: ignore [import-not-found]

from checksum_dict import _utils


if TYPE_CHECKING:
    import brownie  # type: ignore [import-not-found]
    import y  # type: ignore [import-not-found]

    AnyAddressOrContract = Union[AnyAddress, brownie.Contract, y.Contract]

else:

    AnyAddressOrContract = AnyAddress


checksum_value: Final = _utils.checksum_value


@final
class EthAddressKey(str):
    """
    A string subclass that represents a checksummed Ethereum address.

    This class ensures that Ethereum addresses are stored in a checksummed format,
    which is crucial for preventing errors due to mistyped addresses.

    Note:
        This implementation uses a custom Cython function for checksumming to optimize
        performance over the standard :func:`eth_utils.to_checksum_address`.

    Examples:
        Create a checksummed Ethereum address from a string:

        >>> address = EthAddressKey("0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb")
        >>> print(address)
        '0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB'

        Create a checksummed Ethereum address from bytes:

        >>> address_bytes = bytes.fromhex("b47e3cd837ddf8e4c57f05d70ab865de6e193bbb")
        >>> address = EthAddressKey(address_bytes)
        >>> print(address)
        '0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB'

    Raises:
        ValueError: If the provided value cannot be converted to a valid Ethereum address.

    See Also:
        - :func:`eth_utils.to_checksum_address` for the standard checksum conversion.
        - :func:`checksum_dict.checksum.to_checksum_address` for our implementation.
    """

    def __new__(cls, value: Union[bytes, str]) -> "EthAddressKey":
        return super().__new__(cls, checksum_value(value))


__all__ = ["EthAddressKey"]
