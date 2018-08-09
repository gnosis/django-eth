import logging

from ethereum.transactions import secpk1n
from ethereum.utils import checksum_encode
from hexbytes import HexBytes
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


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
    v = serializers.IntegerField(min_value=27, max_value=28)
    r = serializers.IntegerField(min_value=1, max_value=secpk1n - 1)
    s = serializers.IntegerField(min_value=1, max_value=secpk1n // 2)


class TransactionSerializer(serializers.Serializer):
    from_ = EthereumAddressField()
    value = serializers.IntegerField(min_value=0)
    # FIXME Use IntegerField and HexadecimalField
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

