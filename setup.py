from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='ig_prices',  # Required

    version='1.0',  # Required

    description='Simple IG Markets Client to retreive historical price data.',  # Optional

    long_description=long_description,  # Optional

    keywords='trading, investment, finance',

    package_dir={'': 'src'},

    packages=find_packages(where='src'),

    python_requires='>=3.5, <4',

    install_requires=required,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        'console_scripts': [
            'sample=sample:main',
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/darrenlawton/ig_generator/issues',
        'Source': 'https://github.com/darrenlawton/ig_generator/',
    },
)