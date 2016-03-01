from setuptools import setup


setup(
    name="nocql",
    version="0.1",
    description="CQL query abstraction",
    author="Paul W",
    author_email="noptical@gmail.com",
    url="https://github.com/pilate/nocql",
    packages=[
        "nocql",
    ],
    install_requires=[
        "cassandra-driver",
    ])