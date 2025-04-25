import sys
import os

from setuptools import setup, find_packages

# Don't import raindrop-ai module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'raindrop'))
from version import VERSION

setup(
    name="raindrop-ai",
    version=VERSION,
    description="Raindrop AI (Python SDK)",
    author="Raindrop AI",
    author_email="sdk@raindrop.ai",
    long_description="For questions, email us at sdk@raindrop.ai",
    long_description_content_type="text/markdown",
    url="https://raindrop.ai",
    packages=find_packages(include=["raindrop", "README.md"]),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
