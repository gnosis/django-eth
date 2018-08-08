import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

requirements = [
    "Django>=2.0.0",
    "ethereum>=2.3.2",
    "hexbytes>=0.1.0",
    "web3>=4",
]

setup(
    name='django-eth',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Ethereum utilities for Django and Django Rest projects',
    long_description=README,
    url='https://github.com/gnosis/django-eth',
    author='Uxío',
    author_email='uxio@gnosis.pm',
    keywords=['ethereum', 'django', 'rest', 'gnosis'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
