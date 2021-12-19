from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name="starlink-python",
    version="0.1.0",
    description="Connect to SpaceX Starlink",
    author="Austin Rainwater",
    author_email="hey@paco.wtf",
    url="https://github.com/pacorain/starlink-python",
    install_requires=requirements,
    packages=['spacex.starlink']
)