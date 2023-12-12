from setuptools import setup, find_packages

setup(
    name="woof",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'woof = src.main:main',
        ],
    },
)