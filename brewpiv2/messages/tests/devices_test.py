from .. import (
    InstalledDeviceMessage,
    AvailableDeviceMessage
)


class TestDeviceMessages:
    def test_installed_device_from_raw(self):
        dev = InstalledDeviceMessage.from_raw('d:[{"i":0,"t":4,"c":1,"b":0,"f":3,"h":1,"d":0,"p":17,"x":0}]')

        assert(dev.slot == 0 and
               dev.function == 3 and
               dev.device_type == 4 and
               dev.assigned_to_chamber == 1 and
               dev.assigned_to_beer == 0 and
               dev.hardware_type == 1 and
               dev.d == 0 and
               dev.pin == 17 and
               dev.pin_inverted is False)

    def test_available_device_from_raw(self):
        dev = AvailableDeviceMessage.from_raw('h:[{"i":0,"t":4,"c":1,"b":0,"f":3,"h":1,"d":0,"p":17,"x":0}]')

        assert(dev.slot == 0 and
               dev.function == 3 and
               dev.device_type == 4 and
               dev.assigned_to_chamber == 1 and
               dev.assigned_to_beer == 0 and
               dev.hardware_type == 1 and
               dev.d == 0 and
               dev.pin == 17 and
               dev.pin_inverted is False)
