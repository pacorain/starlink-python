from unittest import TestCase
from unittest.mock import MagicMock, patch

from grpc import RpcError

from spacex.starlink import CommunicationError

class TestStarlinkDish(TestCase):
    @patch('grpc.insecure_channel')
    @patch('yagrc.reflector.GrpcReflectionClient')
    def test_default_connection_address(self, _, mock_channel):
        from spacex.starlink import StarlinkDish

        dish = StarlinkDish()
        mock_channel.assert_not_called()
        dish.connect()
        mock_channel.assert_called_with('192.168.100.1:9200')
        mock_channel.reset_mock()

        with StarlinkDish():
            mock_channel.assert_called_with('192.168.100.1:9200')

        

    @patch('grpc.insecure_channel')
    @patch('yagrc.reflector.GrpcReflectionClient')
    def test_custom_connection_address(self, _, mock_channel):
        from spacex.starlink import StarlinkDish

        dish = StarlinkDish('10.999.999.999:invalid_port')
        mock_channel.assert_not_called()
        dish.connect()
        mock_channel.assert_called_with('10.999.999.999:invalid_port')
        mock_channel.reset_mock()

        with StarlinkDish('10.999.999.999:invalid_port'):
            mock_channel.assert_called_with('10.999.999.999:invalid_port')

    
    @patch('grpc.insecure_channel')
    @patch('yagrc.reflector.GrpcReflectionClient')
    def test_channel_closes(self, _, mock_channel):
        from spacex.starlink import StarlinkDish

        dish = StarlinkDish()
        dish.connect()
        mock_channel.assert_called()

        # StarlinkDish discards a closed channel - keep it so we can check it
        channel = dish.channel
        dish.close()
        channel.close.assert_called()

        mock_channel.reset_mock()

        with StarlinkDish() as dish:
            channel = dish.channel

        channel.close.assert_called()

    @patch('grpc.insecure_channel')
    @patch('yagrc.reflector.GrpcReflectionClient')
    def test_autoconnect(self, _, mock_channel):
        from spacex.starlink import StarlinkDish

        dish = StarlinkDish()
        with self.assertRaises(ValueError):
            dish.refresh()

        dish = StarlinkDish(autoconnect=True)
        mock_channel.assert_not_called()
        dish.refresh()
        mock_channel.assert_called()
        dish.stub.Handle.assert_called()

    @patch('grpc.insecure_channel')
    @patch('yagrc.reflector.GrpcReflectionClient')
    def test_cannot_connect(self, mock_reflector, mock_channel):
        from spacex.starlink import StarlinkDish

        dish = StarlinkDish()
        dish.reflector = MagicMock()
        dish.reflector.load_protocols.side_effect = RpcError()

        with self.assertRaises(CommunicationError):
            dish.connect()

    @patch('grpc.insecure_channel')
    @patch('yagrc.reflector.GrpcReflectionClient')
    def test_communication_error(self, mock_reflector, mock_channel):
        from spacex.starlink import StarlinkDish

        dish = StarlinkDish()
        dish.reflector = MagicMock()
        dish.connect()
        dish.refresh()

        dish.stub.Handle.side_effect = RpcError()

        with self.assertRaises(CommunicationError):
            dish.refresh()
    