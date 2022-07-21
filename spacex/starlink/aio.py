import grpc
import warnings

from .dish import StarlinkDish
from . import CommunicationError
from .status import DishStatus

class AsyncStarlinkDish(StarlinkDish):
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
        This is deprecated on AsyncStarlinkDish. You must manually connect, either by calling
        StarlinkDish.connect() or with a context manager (`with StarlinkDish() as dish:`).

    [yagrc]: https://github.com/sparky8512/yagrc

    """
    def __init__(self, address="192.168.100.1:9000", *, autoconnect=False):
        if autoconnect:
            warnings.warn("Autoconnect was a bad design decision, is not supported on AsyncStarlinkDish", UserWarning)
        
        super().__init__(address, autoconnect=False)

    async def connect(self, refresh=True):
        """Opens a gRPC connection to the satellite and reflects the available classes.
        
        Parameters
        ----------
        refresh : bool
            By default, the `connect` method will automatically get the current status, allowing you to query the
            status of the dish upon connection with `dish.status`. To skip this, call `connect` with 
            `refresh=False`. To fetch the status at a later point, you must call `StarlinkDish.refresh()`.
            
        """
        global Request
        try:
            # We have to load a sync client because yagrc doesn't support async
            with grpc.insecure_channel(self.address) as sync_channel:
                self.reflector.load_protocols(sync_channel)
            
            DeviceStub = self.reflector.service_stub_class("SpaceX.API.Device.Device")
            Request = self.reflector.message_class("SpaceX.API.Device.Request")
            self.channel = grpc.aio.insecure_channel(self.address)
            self.stub = DeviceStub(self.channel)

            response = await self.stub.Handle(Request(get_device_info={}))
            self._device_info = response.get_device_info.device_info
        except grpc.RpcError as e:
            raise CommunicationError from e
        if refresh:
            await self.refresh()

    async def refresh(self):
        """Refreshes status data from all endpoints. Right now, just calls SpaceX.API.Device.Request.get_status"""
        try:
            await self.fetch_status()
        except grpc.RpcError as e:
            raise CommunicationError from e

    async def fetch_status(self):
        """Uses the active connection to get an up-to-date status from the satellite"""
        global Request
        response = await self.stub.Handle(Request(get_status={}))
        self.status = DishStatus(response)
        return self.status

    async def close(self):
        if self.channel:
            await self.channel.close()
        self.channel = None
