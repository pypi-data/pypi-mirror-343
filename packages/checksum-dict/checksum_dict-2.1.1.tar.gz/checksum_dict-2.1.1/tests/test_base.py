import pytest

from checksum_dict import ChecksumAddressDict


@pytest.mark.parametrize(
    "seed, expected",
    [
        (
            {"0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb": True},
            {"0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB": True},
        ),  # id: seed-dict
        (None, {}),  # id: seed-none
        (
            [("0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb", True)],
            {"0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB": True},
        ),  # id: seed-iterable
        ([], {}),  # id: seed-empty-iterable
    ],
)
def test_checksum_address_dict_init(seed, expected):
    # Act
    cad = ChecksumAddressDict(seed)

    # Assert
    assert dict(cad) == expected


@pytest.mark.parametrize(
    "key, value, expected",
    [
        ("0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb", True, True),  # id: set-and-get-lowercase
        ("0xB47E3CD837DDF8E4C57F05D70AB865DE6E193BBB", False, False),  # id: set-and-get-uppercase
        ("0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb", 123, 123),  # id: set-and-get-checksummed
    ],
)
def test_checksum_address_dict_set_and_get(key, value, expected):
    # Act
    cad = ChecksumAddressDict()
    cad[key] = value

    # Assert
    assert cad[key] == expected


@pytest.mark.parametrize(
    "key, expected_error",
    [
        ("0x123", ValueError),  # id: invalid-address-length
        (123, TypeError),  # id: invalid-address-type
    ],
)
def test_checksum_address_dict_get_error(key, expected_error):
    # Arrange
    cad = ChecksumAddressDict()

    # Act & Assert
    with pytest.raises(expected_error):
        cad[key]


@pytest.mark.parametrize(
    "key, value",
    [
        ("0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb", True),  # id: set-nochecksum-valid
    ],
)
def test_checksum_address_dict_set_and_get_nochecksum(key, value):
    # Arrange
    cad = ChecksumAddressDict()

    # Act
    cad._setitem_nochecksum(key, value)

    # Assert
    assert cad._getitem_nochecksum(key) == value
    assert cad[key] == value


@pytest.mark.parametrize(
    "key, value, expected_error",
    [
        ("0x123", True, ValueError),  # id: set-nochecksum-invalid-address
        (
            "0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb123",
            True,
            ValueError,
        ),  # id: set-nochecksum-invalid-address-length
        (123, True, ValueError),  # id: set-nochecksum-invalid-address-type
    ],
)
def test_checksum_address_dict_set_nochecksum_error(key, value, expected_error):
    # Arrange
    cad = ChecksumAddressDict()

    # Act & Assert
    with pytest.raises((expected_error, AttributeError)):
        cad._setitem_nochecksum(key, value)


def test_checksum_address_dict_repr():
    # Arrange
    cad = ChecksumAddressDict({"0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb": True})

    # Act
    representation = repr(cad)

    # Assert
    assert (
        representation
        == "ChecksumAddressDict({'0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB': True})"
    )
