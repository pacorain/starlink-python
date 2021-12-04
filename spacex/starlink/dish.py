import grpc
from yagrc.reflector import GrpcReflectionClient

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
        Whether or not to initiate a connection and do reflection when loading a property. By default, you must 
        manually connect to make sure the host is reachable before loading any data. To change this behavior, set 
        `autoconnect=True`.

    [yagrc]: https://github.com/sparky8512/yagrc

    """
    def __init__(self, address="192.168.100.1:9200", *, autoconnect=False):
        self.address = address
        self.reflector = GrpcReflectionClient()
        self.autoconnect = autoconnect
        self._device_info = None

    def connect(self):
        """Attempts to connect to the gRPC host and reflect, and loads device info"""
        with grpc.insecure_channel(self.address) as channel:
            self.reflector.load_protocols(channel)
            DeviceStub = self.reflector.service_stub_class("SpaceX.API.Device.Device")
            Request = self.reflector.message_class("SpaceX.API.Device.Request")

            stub = DeviceStub(channel)
            response = stub.Handle(Request(get_device_info={}))
            self._device_info = response.get_device_info.device_info

    @property
    def hardware_version(self):
        self._ensure_connected()
        return self._device_info.hardware_version

    @property
    def software_version(self):
        self._ensure_connected()
        return self._device_info.software_version

    @property
    def country_code(self):
        self._ensure_connected()
        return self._device_info.country_code

    @property
    def utc_offset_s(self):
        self._ensure_connected()
        return self._device_info.utc_offset_s

    @property
    def id(self):
        self._ensure_connected()
        return self._device_info.id

    @property
    def connected(self):
        return self._device_info is not None

    def _ensure_connected(self):
        if not self.connected and self.autoconnect:
            self.connect()
        elif not self.connected:
            raise ValueError("StarlinkDish.connect() must be run to get this property")

        