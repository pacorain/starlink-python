from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.readlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="starlink-python",
    version="0.1.2",
    description="Connect to SpaceX Starlink",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Austin Rainwater",
    author_email="hey@paco.wtf",
    url="https://github.com/pacorain/starlink-python",
    project_urls={
        "Bug Tracker": "https://github.com/pacorain/starlink-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "License :: Public Domain",
        "Topic :: Home Automation",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    packages=['spacex.starlink']
)