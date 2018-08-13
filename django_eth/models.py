import ethereum.utils
from django import forms
from django.core import exceptions
from django.db import models
from django.utils.translation import gettext_lazy as _
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


class Uint256Field(models.Field):
    description = _("Ethereum uint256 number")
    """
    Field to store ethereum uint256 values. Uses Decimal db type without decimals to store
    in the database, but retrieve as `int` instead of `Decimal` (https://docs.python.org/3/library/decimal.html)
    """
    def __init__(self, *args, **kwargs):
        self.max_digits, self.decimal_places = 79, 0  # 2 ** 256 is 78 digits
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "DecimalField"

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_db_prep_save(self, value, connection):
        return connection.ops.adapt_decimalfield_value(self.to_python(value),
                                                       max_digits=self.max_digits,
                                                       decimal_places=self.decimal_places)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return self.to_python(value)

    def to_python(self, value):
        if value is None:
            return value
        try:
            return int(value)
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.IntegerField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class HexField(models.CharField):
    """
    Field to store hex values (without 0x). Returns hex with 0x prefix.

    On Database side a CharField is used.
    """
    description = "Stores a hex value into an CharField"

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        return value if value is None else HexBytes(value).hex()

    def get_prep_value(self, value):
        if value is None:
            return value
        elif isinstance(value, HexBytes):
            return value.hex()[2:]  # HexBytes.hex() retrieves hexadecimal with '0x', remove it
        elif isinstance(value, bytes):
            return value.hex()  # bytes.hex() retrieves hexadecimal without '0x'
        else:  # str
            return HexBytes(value).hex()[2:]


class Sha3HashField(HexField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 64
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs


class EthereumBigIntegerField(models.Field):
    """
    Deprecated
    """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 64
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def get_internal_type(self):
        return "CharField"

    def from_db_value(self, value, expression, connection):
        """
        Retrieve value as int
        :param value: number in hexadecimal
        :return: number as int
        """
        if value is None:
            return value
        else:
            return int(value, 16)

    def to_python(self, value):
        """
        Use value from form
        :param value: value as int
        :return: number as int
        """
        value = super().to_python(value)
        if value is None:
            return value
        else:
            return int(value)

    def get_prep_value(self, value):
        """
        :param value:  number in hex or int
        :return: number in hex without 0x
        """
        if value is None:
            return value
        elif isinstance(value, str):
            return value
        else:
            return hex(int(value))[2:]
