Django Ethereum (django-eth)
############################

.. class:: no-web no-pdf

|travis| |coveralls| |python| |django| |pipy|

Django ethereum is a set of helpers for working with
ethereum using Django and Django Rest framework.

It includes:

- Basic serializers (signature, transaction)
- Serializer fields (Ethereum address field, hexadecimal field)
- Model fields (Ethereum address, Ethereum big integer field)
- Signing messages
- Utils for testing

Quick start
-----------

Just run ``pip install django-eth`` or add it to your **requirements.txt**

Contributors
------------
- Denís Graña (denis@gnosis.pm)
- Giacomo Licari (giacomo.licari@gnosis.pm)
- Uxío Fuentefría (uxio@gnosis.pm)

.. |travis| image:: https://travis-ci.org/gnosis/django-eth.svg?branch=master
    :target: https://travis-ci.org/gnosis/django-eth
    :alt: Travis CI build

.. |coveralls| image:: https://coveralls.io/repos/github/gnosis/django-eth/badge.svg?branch=master
    :target: https://coveralls.io/github/gnosis/django-eth?branch=master
    :alt: Coveralls

.. |python| image:: https://img.shields.io/badge/Python-3.6-blue.svg
    :alt: Python 3.6

.. |django| image:: https://img.shields.io/badge/Django-2-blue.svg
    :alt: Django 2

.. |pipy| image:: https://badge.fury.io/py/django-eth.svg
    :target: https://badge.fury.io/py/django-eth
    :alt: Pypi package
