class DishStatus:
    """Helper for parsing device status from Starlink"""
    __slots__ = ['raw']

    def __init__(self, status_response): 
        self.raw = status_response.dish_get_status

    @property
    def connected(self):
        return not self.raw.HasField("outage")

    @property
    def obstructed(self):
        obstruction_stats = self.raw.obstruction_stats
        return obstruction_stats.currently_obstructed


    def __repr__(self):
        return self.raw.__repr__()

    
