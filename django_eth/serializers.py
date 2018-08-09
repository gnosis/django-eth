import logging

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
    def to_representation(self, obj):
        if not obj:
            return '0x'
        else:
            return obj.hex()

    def to_internal_value(self, data):
        if not data or data == '0x':
            return None
        try:
            return HexBytes(data)
        except ValueError:
            raise ValidationError("%s is not hexadecimal" % data)


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
    data = serializers.CharField()
    gas = serializers.HexadecimalField(min_value=0)
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
