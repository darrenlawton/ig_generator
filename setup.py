from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='IGPrices',  # Required

    version='1.0',  # Required

    description='Simple IG Markets Client to retreive historical price data.',  # Optional

    long_description=long_description,  # Optional

    keywords='trading, investment, finance',

    packages=['IGPrices'],

    python_requires='>=3.5, <4',

    install_requires=required,
    tests_require=['unittest'],

    project_urls={
        'Bug Reports': 'https://github.com/darrenlawton/ig_generator/issues',
        'Source': 'https://github.com/darrenlawton/ig_generator/',
    },
)