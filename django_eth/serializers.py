import logging

from django.utils.translation import ugettext_lazy as _
from ethereum.utils import checksum_encode
from hexbytes import HexBytes
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .constants import *

logger = logging.getLogger(__name__)


# ================================================ #
#                Custom Fields
# ================================================ #
class EthereumAddressField(serializers.Field):
    """
    Ethereum address checksumed
    https://github.com/ethereum/EIPs/blob/master/EIPS/eip-55.md
    """

    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        # Check if address is valid

        try:
            if checksum_encode(data) != data:
                raise ValueError
            elif int(data, 16) == 0:
                raise ValidationError("0x0 address is not allowed")
            elif int(data, 16) == 1:
                raise ValidationError("0x1 address is not allowed")
        except ValueError:
            raise ValidationError("Address %s is not checksumed" % data)
        except Exception:
            raise ValidationError("Address %s is not valid" % data)

        return data


class HexadecimalField(serializers.Field):
    """
    Serializes hexadecimal values starting by `0x`. Empty values should be None or just `0x`.
    """

    default_error_messages = {
        'invalid': _('{value} is not an hexadecimal value.'),
        'blank': _('This field may not be blank.'),
        'max_length': _('Ensure this field has no more than {max_length} hexadecimal chars (not counting 0x).'),
        'min_length': _('Ensure this field has at least {min_length} hexadecimal chars (not counting 0x).'),
    }

    def __init__(self, **kwargs):
        self.allow_blank = kwargs.pop('allow_blank', False)
        self.max_length = kwargs.pop('max_length', None)
        self.min_length = kwargs.pop('min_length', None)
        super().__init__(**kwargs)

    def to_representation(self, obj):
        if not obj:
            return '0x'
        else:
            return obj.hex()

    def to_internal_value(self, data):
        if isinstance(data, bytes):
            data = data.hex()

        data = data.strip()  # Trim spaces
        if data.startswith('0x'):  # Remove 0x prefix
            data = data[2:]

        if not data:
            if self.allow_blank:
                return None
            else:
                self.fail('blank')

        data_len = len(data)
        if self.min_length and data_len < self.min_length:
            self.fail('min_length', min_length=data_len)
        elif self.max_length and data_len > self.max_length:
            self.fail('max_length', max_length=data_len)

        try:
            return HexBytes(data)
        except ValueError:
            self.fail('invalid', value=data)


class Sha3HashField(HexadecimalField):
    def __init__(self, **kwargs):
        kwargs['max_length'] = 64
        kwargs['min_length'] = 64
        super().__init__(**kwargs)


# ================================================ #
#                Base Serializers
# ================================================ #
class SignatureSerializer(serializers.Serializer):
    v = serializers.IntegerField(min_value=SIGNATURE_V_MIN_VALUE,
                                 max_value=SIGNATURE_V_MAX_VALUE)
    r = serializers.IntegerField(min_value=SIGNATURE_R_MIN_VALUE,
                                 max_value=SIGNATURE_R_MAX_VALUE)
    s = serializers.IntegerField(min_value=SIGNATURE_S_MIN_VALUE,
                                 max_value=SIGNATURE_S_MAX_VALUE)


class TransactionSerializer(serializers.Serializer):
    from_ = EthereumAddressField()
    value = serializers.IntegerField(min_value=0)
    data = HexadecimalField()
    gas = serializers.IntegerField(min_value=0)
    gas_price = serializers.IntegerField(min_value=0)
    nonce = serializers.IntegerField(min_value=0)

    def get_fields(self):
        result = super().get_fields()
        # Rename `from_` to `from`
        from_ = result.pop('from_')
        result['from'] = from_
        return result


class TransactionResponseSerializer(serializers.Serializer):
    """
    Use chars to avoid problems with big ints (i.e. JavaScript)
    """
    from_ = EthereumAddressField()
    value = serializers.IntegerField(min_value=0)
    data = serializers.CharField()
    gas = serializers.CharField()
    gas_price = serializers.CharField()
    nonce = serializers.IntegerField(min_value=0)

    def get_fields(self):
        result = super().get_fields()
        # Rename `from_` to `from`
        from_ = result.pop('from_')
        result['from'] = from_
        return result
