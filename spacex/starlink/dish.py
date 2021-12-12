from typing import Optional
import grpc
from yagrc.reflector import GrpcReflectionClient

from .status import DishStatus

Request = None

def autoconnect(fn):
    """Annotation to autoconnect to Starlink or raise an error when not connected"""
    def ensure_connected(dish, *args, **kwargs):
        if not dish.connected and dish.autoconnect:
            dish.connect()
        elif not dish.connected:
            raise ValueError("StarlinkDish.connect() must be run to get this property")
        return fn(dish, *args, **kwargs)
    return ensure_connected


class StarlinkDish:
    """A class representing a connection to the Starlink satellite.
    
    Uses the [yagrc][] library to automatically reflect the gRPC server hosted by Dishy McFlatface.
    
    Attributes
    ----------
    address : str
        The IP and port number to connect to. This defaults to `192.168.100.1:9200`, which the dish expects
        a static route to in order to display data. In other words, whatever makes the actual connection to Dishy must
        connect to IP 192.168.100.1 on port 9200.

        However, I don't know if it's possible to proxy connections to gRPC so I'm including this option in case
        someone has such a proxy set up.

    autoconnect : bool
        Before informational and status methods work, you need to do an initial connection to the server and reflect
        the available interfaces.

        By default, you must manually connect to make sure the host is reachable before loading any data. To change 
        this behavior, set `autoconnect=True`.

        Note that you must still remember to call `StarlinkDish.close()` to close the connection. Neither the 
        `autoconnect` parameter nor calling `close()` are necessary if you are using a context manager (i.e. 
        `with StarlinkDish() as dish:`), as connecting and disconnecting are managed by the context manager.

    [yagrc]: https://github.com/sparky8512/yagrc

    """
    def __init__(self, address="192.168.100.1:9200", *, autoconnect=False):
        self.address = address
        self.reflector = GrpcReflectionClient()
        self.autoconnect = autoconnect
        self._device_info = None
        self.status = None
        self.stub = None
        self.Request = None
        self.channel: Optional[grpc.Channel] = None

    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, *_):
        if self.channel:
            self.channel.close()

    def connect(self, refresh=True):
        """Opens a gRPC connection to the satellite and reflects the available classes.
        
        Parameters
        ----------
        refresh : bool
            By default, the `connect` method will automatically get the current status, allowing you to query the
            status of the dish upon connection with `dish.status`. To skip this, call `connect` with 
            `refresh=False`. To fetch the status at a later point, you must call `StarlinkDish.refresh()`.
            
        """
        global Request

        self.channel = grpc.insecure_channel(self.address)
        self.reflector.load_protocols(self.channel)
        
        DeviceStub = self.reflector.service_stub_class("SpaceX.API.Device.Device")
        Request = self.reflector.message_class("SpaceX.API.Device.Request")

        self.stub = DeviceStub(self.channel)
        response = self.stub.Handle(Request(get_device_info={}))
        self._device_info = response.get_device_info.device_info
        if refresh:
            self.refresh()

    @autoconnect
    def refresh(self):
        """Refreshes status data from all endpoints. Right now, just calls SpaceX.API.Device.Request.get_status"""
        self.fetch_status()

    @autoconnect
    def fetch_status(self):
        """Uses the active connection to get an up-to-date status from the satellite"""
        global Request
        response = self.stub.Handle(Request(get_status={}))
        self.status = DishStatus(response)
        return self.status

    @property
    @autoconnect
    def hardware_version(self):
        return self._device_info.hardware_version

    @property
    @autoconnect
    def software_version(self):
        return self._device_info.software_version

    @property
    @autoconnect
    def country_code(self):
        return self._device_info.country_code

    @property
    @autoconnect
    def utc_offset_s(self):
        return self._device_info.utc_offset_s

    @property
    @autoconnect
    def id(self):
        return self._device_info.id

    @property
    def connected(self):
        return self.channel is not None

    def close(self):
        if self.channel:
            self.channel.close()
        self.channel = None


        