from typing import List
from spacex.starlink import OutageReason, DishAlert


class DishStatus:
    """Helper for parsing device status from Starlink"""
    __slots__ = ['raw']

    def __init__(self, status_response): 
        self.raw = status_response.dish_get_status

    @property
    def connected(self) -> bool:
        """Whether the Starlink is connected or has an outage reported"""
        return not self.raw.HasField("outage")

    @property
    def outage_reason(self) -> OutageReason:
        """An OutageReason corresponding to the reason for the outage, or None if the Starlink is connected"""
        if self.connected:
            return None
        raw_cause_val = self.raw.cause.value
        return OutageReason(raw_cause_val)

    @property
    def obstructed(self) -> bool:
        """Whether or not the Starlink is obstructed"""
        obstruction_stats = self.raw.obstruction_stats
        return obstruction_stats.currently_obstructed

    @property
    def uptime_as_seconds(self) -> int:
        """Uptime, in seconds"""
        return self.raw.device_state.uptime_s

    @property
    def ping_drop_rate(self) -> float:
        """Rate of pings being dropped (out of 1)"""
        return self.raw.pop_ping_drop_rate
    
    @property
    def ping_latency(self):
        """Average time for a single ping (in milleseconds)"""
        return self.raw.pop_ping_latency_ms

    @property
    def downlink_throughput(self) -> float:
        """Downlink throughput, in bps
        
        (It is currently unclear if bps refers to bytes or bits)
        """
        return self.raw.downlink_throughput_bps

    @property
    def uplink_throughput(self) -> float:
        """Uplink throughput, in bps
        
        (It is currently unclear if bps refers to bytes or bits)
        """
        # TODO: Find out if this is bytes or bits per second
        return self.raw.uplink_throughput_bps

    @property
    def azimuth_deg(self) -> float:
        """The angle of the satellite in azimuth degrees"""
        return self.raw.boresight_azimuth_deg

    @property
    def elevation_deg(self) -> float:
        """The angle of the satellite in elevation degrees"""
        return self.raw.boresight_elevation_deg

    @property
    def alerts(self) -> List[DishAlert]:
        return DishAlert.from_source(self.raw.alerts)


    def __repr__(self):
        return self.raw.__repr__()

    
