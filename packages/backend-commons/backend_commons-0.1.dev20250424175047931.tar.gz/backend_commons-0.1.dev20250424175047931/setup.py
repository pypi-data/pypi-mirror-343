import os
from setuptools import setup, find_packages

version = os.getenv("PACKAGE_VERSION", "0.1.dev0")

setup(
    name="backend-commons",
    version=version,
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.7",
)
