"""starlink-python library

This library uses gRPC to communicate with your Starlink satellite and make its state accessible in Python.

Examples
--------
You can use the `StarlinkDish` class to connect to Starlink and get information.

>>> from spacex.starlink import StarlinkDish
>>> with StarlinkDish() as dish:  # Automatically connects and fetches data
...   obstructed = dish.status.obstructed
"""

__all__ = ['StarlinkDish', 'DishStatus', 'OutageReason', 'DishAlert']

from .alert import DishAlert
from .outage_reason import OutageReason
from .status import DishStatus
from .dish import StarlinkDish
