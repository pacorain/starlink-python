"""Checks the connection to an existing Starlink and a few of the status methods."""

import unittest
from spacex.starlink import StarlinkDish

class TestStarlinkHardware(unittest.TestCase):
    """Test hardware for compatibility with Starlink Python"""
    def test_connects_to_satellite(self):
        with StarlinkDish():
            pass

    def test_loads_hardware_info(self):
        dish = StarlinkDish()
        dish.connect()
        print("Starlink Hardware info:", dish._device_info)

    def test_refresh(self):
        with StarlinkDish() as dish:
            self.assertIsNotNone(dish.status)
            self.assertTrue(dish.status.connected)
            self.assertIsNotNone(dish.status.uptime_as_seconds)
            self.assertIsNotNone(dish.status.downlink_throughput)
            self.assertIsNotNone(dish.status.azimuth_deg)
            self.assertIsNotNone(dish.status.alerts)

if __name__ == '__main__':
    unittest.main()