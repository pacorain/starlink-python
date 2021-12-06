from enum import Enum

class DishAlert(str, Enum):
    """An alert for something prohibiting Dishy from operating normally"""

    def __new__(cls, value, label):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        return obj

    MOTORS_STUCK = ('motors_stuck', 'Dish motots stuck')
    THERMAL_THROTTLE = ('thermal_throttle', 'Throttled due to temperature')
    THERMAL_SHUTDOWN = ('thermal_shutdown', 'Shutdown due to themral conditions')
    MAST_NOT_NEAR_VERTICAL = ('mast_not_near_vertical', 'Mast is not near vertical')
    UNEXPECTED_LOCATION = ('unexpected_location', 'Unexpected location')
    SLOW_ETHERNET_SPEEDS = ('slow_ethernet_speeds', 'Ethernet connection to dish too slow')

    @classmethod
    def from_source(cls, source):
        """Get a list of alerts (if any) from a SpaceX.API.Device.DishgetStatusresponse.alerts response."""
        alerts = []
        for alert in DishAlert:
            if bool(getattr(source, alert.value)):
                alerts.append(alert)
        return alerts

