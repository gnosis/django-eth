from django.db import models

from ..models import EthereumAddressField, Sha3HashField, Uint256Field


class EthereumAddress(models.Model):
    value = EthereumAddressField()


class Uint256(models.Model):
    value = Uint256Field()


class Sha3Hash(models.Model):
    value = Sha3HashField()
