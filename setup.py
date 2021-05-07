import setuptools
from pathlib import Path

setuptools.setup(
    name="GooglePatents",
    version='0.0.1',
    long_description=Path('README.md').read_text(),
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=[
        'json',
        'requests',
        'pandas',
        'beautifulsoup4'
    ],
)
