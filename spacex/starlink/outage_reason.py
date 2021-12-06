from enum import Enum

class OutageReason(int, Enum):
    """The reported reason for a Starlink outage
    
    While the reflection process creates an Enum on its own, this creates one that is accessible through code 
    completion, and assigns a user-friendly label to each enumeration.

    The enum values match the value that will be returned by Starlink in the case of an outage.

    Attributes
    ----------
    value : int
        The raw value, matching the value that will be returned by the host

    label : str
        A user-friendly label to help someone determine why their internet is out
    """

    def __new__(cls, value, label):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        return obj

    UNKNOWN = (0, 'Unknown')
    BOOTING = (1, 'Dish Booting')
    STOWED = (2, 'Stowed')
    THERMAL_SHUTDOWN = (3, 'Thermal Shutdown')
    NO_SCHEDULE = (4, 'Searching')
    NO_SATS = (5, 'No Satellites')
    OBSTRUCTED = (6, 'Starlink Obstructed')
    NO_DOWNLINK = (7, 'No Downlink')
    NO_PINGS = (8, 'No Pings')