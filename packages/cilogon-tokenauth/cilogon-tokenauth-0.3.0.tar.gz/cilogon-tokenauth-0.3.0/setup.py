#!/usr/bin/env python
import sys

from cilogon_tokenauth import __version__

assert sys.version_info >= (3, 8), "Requires Python v3.8 or above."
from distutils.core import setup  # noqa
from setuptools import find_namespace_packages  # noqa

setup(
    name="cilogon-tokenauth",
    version=__version__,
    author="Eric Blau",
    author_email="blau@globus.org",
    url="https://github.com/access-ci-org/cilogon-tokenauth",
    description="""An authentication backend that allows CILogon bearer to authenticate users to DRF apis.""",
    keywords="django",
    zip_safe=False,
    include_package_data=True,
    packages=find_namespace_packages(),
)
