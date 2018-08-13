from django.test import TestCase
from ethereum.utils import sha3
from hexbytes import HexBytes
from rest_framework import serializers

from ..serializers import HexadecimalField, Sha3HashField


class HexadecimalSerializerTest(serializers.Serializer):
    value = HexadecimalField()


class HexadecimalBlankSerializerTest(serializers.Serializer):
    value = HexadecimalField(allow_blank=True)


class HexadecimalNullSerializerTest(serializers.Serializer):
    value = HexadecimalField(allow_null=True)


class Sha3HashSerializerTest(serializers.Serializer):
    value = Sha3HashField()


class TestSerializers(TestCase):
    def test_hexadecimal_field(self):
        serializer = HexadecimalBlankSerializerTest(data={'value': '0x'})
        self.assertTrue(serializer.is_valid())
        self.assertIsNone(serializer.validated_data['value'])

        serializer = HexadecimalBlankSerializerTest(data={'value': None})
        self.assertFalse(serializer.is_valid())

        serializer = HexadecimalNullSerializerTest(data={'value': None})
        self.assertTrue(serializer.is_valid())
        self.assertIsNone(serializer.validated_data['value'])

        value = '0xabc'
        serializer = HexadecimalSerializerTest(data={'value': value})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['value'], HexBytes(value))

        value = 'abc'
        serializer = HexadecimalSerializerTest(data={'value': value})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['value'], HexBytes(value))

    def test_hash_serializer_field(self):
        value = sha3('test').hex()
        serializer = Sha3HashSerializerTest(data={'value': value})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['value'], HexBytes(value))

        # Hash with one more character - Must be 32 bytes
        serializer = Sha3HashSerializerTest(data={'value': value + 'a'})
        serializer.is_valid()
        self.assertFalse(serializer.is_valid())

        # Hash with one less character - Must be 32 bytes
        serializer = Sha3HashSerializerTest(data={'value': value[:-1]})
        self.assertFalse(serializer.is_valid())
