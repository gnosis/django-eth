import ethereum.utils
from django.db import models
from hexbytes import HexBytes

from .validators import validate_checksumed_address


class EthereumAddressField(models.CharField):
    default_validators = [validate_checksumed_address]
    description = "Ethereum address"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 42
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        value = super().to_python(value)
        if value:
            return ethereum.utils.checksum_encode(value)
        else:
            return value

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value:
            return ethereum.utils.checksum_encode(value)
        else:
            return value


class EthereumBigIntegerField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 64
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        """
        Retrieve value as int
        :param value: number in hexadecimal
        :return: number as int
        """
        value = super().to_python(value)
        if not value:
            return value
        else:
            return int(value, 16)

    def get_prep_value(self, value):
        """
        :param value:  number in hex or int
        :return: number in hex without 0x
        """
        if not value:
            return value
        if isinstance(value, str):
            return value
        else:
            return hex(int(value))[2:]


class Uint256Field(models.DecimalField):
    """
    Field to store ethereum uint256 values
    """
    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = 78  # 2^256 is 78 digits
        kwargs['decimal_places'] = 0
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_digits']
        del kwargs['decimal_places']


class HexField(models.CharField):
    """
    Field to store hex values (without 0x). Returns hex with 0x prefix.

    On Database side a CharField is used.
    """
    description = "Stores a hex value into an CharField"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 64
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        return value if value is None else HexBytes(value).hex()

    def get_prep_value(self, value):
        if value is None:
            return value
        elif isinstance(value, bytes):
            return value.hex()  # bytes.hex() retrieves hexadecimal without '0x'
        elif isinstance(value, HexBytes):
            return value.hex()[2:]  # HexBytes.hex() retrieves hexadecimal with '0x', remove it
        else:  # str
            return HexBytes(value).hex()[2:]
