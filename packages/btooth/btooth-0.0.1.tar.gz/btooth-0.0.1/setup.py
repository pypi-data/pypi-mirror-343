from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Bluetooth handler'
LONG_DESCRIPTION = 'A package that allows to setup bluetooth communication.'

# Setting up
setup(
    name="btooth",
    version=VERSION,
    author="Blue Whale",
    author_email="<mail@bluewhale.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'bluetooth'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
