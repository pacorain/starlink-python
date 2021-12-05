# Starlink Python

![Status: Pre-Alpha](https://img.shields.io/badge/status-pre--alpha-orange)

A Python library for loading data from a [SpaceX Starlink](https://www.starlink.com/) satellite.

The goal is to be a simple interface for Starlink. It builds upon the work done on [starlink-grpc-tools](https://github.com/sparky8512/starlink-grpc-tools)to connect to Starlink from Python (and I'm also using it to understand gRPC, which I've never used before this).

I'm writing this in order to create a Home Assistant component for Starlink. I'll update the README when I have that started.

I currently have the first iteration of Starlink satellites and am developing with this. Feel free to create an issue if you have a second iteration and want to help add support for this.

## Example

The goal is to write an interface that is friendly for users and that abstracts the connection details. For example:

```python
from spacex.starlink import StarlinkDish

def is_my_dish_obstructed() -> bool:
    # Using a context manager automatically connects
    with StarlinkDish() as dish:
        return dish.status.obstructed
```
