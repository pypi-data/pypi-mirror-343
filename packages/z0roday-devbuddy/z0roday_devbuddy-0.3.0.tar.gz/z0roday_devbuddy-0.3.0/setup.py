from setuptools import setup

setup(
    name="z0roday-devbuddy",
    version="0.3.0",
    packages=["devbuddy", "devbuddy.plugins"],
    entry_points={
        'console_scripts': [
            'dbuddy=devbuddy.cli:cli',
        ],
    },
) 