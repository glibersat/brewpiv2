from distutils.core import setup

setup(
    name = 'BrewPi v2 Communication Library',
    version = '0.1',

    author = 'Guillaume Libersat',
    description = 'Library for driving BrewPi v2 controllers',
    license = 'GNU AGPL',

    packages = ['brewpiv2', 'brewpiv2/commands']
)
