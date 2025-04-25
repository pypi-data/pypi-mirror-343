from setuptools import setup, find_packages
from seismicio.constants.__version__ import __version__
import codecs
import os

VERSION = __version__
DESCRIPTION = 'Read and write .su files for seismic data'

# Setting up
setup(
    name="seismicio",
    version=VERSION,
    author="cadu-sg",
    author_email="",
    description=DESCRIPTION,
    include_package_data=True,
    packages=find_packages(),
    install_requires=['numpy', 'fs'],
    keywords=['python', 'io'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
