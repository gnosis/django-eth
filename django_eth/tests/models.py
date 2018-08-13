from ..models import Sha3HashField, EthereumAddressField, Uint256Field
from django.db import models


class EthereumAddress(models.Model):
    value = EthereumAddressField()


class Uint256(models.Model):
    value = Uint256Field()


class Sha3Hash(models.Model):
    value = Sha3HashField()

