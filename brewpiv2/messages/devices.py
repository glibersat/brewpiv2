from .base import Message
from ..constants import (
    DeviceFunction,
    DeviceType,
    HardwareType
)

from .decoder import register_to_decoder


class DeviceMessage(Message):
    """
    Abtract Class that holds common device information
    """

    data_mapping = {
        'i': 'slot',
        't': 'device_type',
        'c': 'assigned_to_chamber',
        'b': 'assigned_to_beer',
        'f': 'function',
        'h': 'hardware_type',
        'd': 'd',
        'p': 'pin',
        'x': 'pin_inverted',
        'n': 'output_nr',
        'a': 'address',
        'v': 'value'
    }

    def __init__(self, slot, device_type, assigned_to_chamber,
                 assigned_to_beer, function, hardware_type, d, pin, pin_inverted=None,
                 output_nr=None, address=None, value=None):
        self.slot = slot
        self.device_type = device_type
        self.assigned_to_chamber = assigned_to_chamber
        self.assigned_to_beer = assigned_to_beer
        self.function = function
        self.hardware_type = hardware_type
        self.d = d
        self.pin = pin
        self.output_nr = output_nr
        self.pin_inverted = bool(pin_inverted)
        self.address = address
        self.value = value

    def __str__(self):
        return "Device <slot:{self.slot}, device_type:{device_type}, " \
            "chamber:{self.assigned_to_chamber}, beer:{self.assigned_to_beer}, " \
            "function:{function}, hardware_type:{hardware_type}, " \
            "d:{self.d}, pin:{self.pin}, pin_inverted?:{self.pin_inverted}, "\
            "output_nr:{self.output_nr}, " \
            "address:{self.address}, value:{self.value}>".format(self=self,
                                                                 device_type=DeviceType.to_str(self.device_type),
                                                                 hardware_type=HardwareType.to_str(self.hardware_type),
                                                                 function=DeviceFunction.to_str(self.function))


@register_to_decoder()
class AvailableDeviceMessage(DeviceMessage):
    """
    Available devices (not installed) on the controller
    """
    cmd = 'h'

    def visit(self, aMessageHandler):
        aMessageHandler.available_device(self)

    def __str__(self):
        return "Available {0}".format(super().__str__())


@register_to_decoder()
class InstalledDeviceMessage(DeviceMessage):
    """
    Installed devices (installed) on the controller
    """
    cmd = 'd'

    def visit(self, aMessageHandler):
        aMessageHandler.installed_device(self)

    def __str__(self):
        return "Installed {0}".format(super().__str__())

@register_to_decoder()
class UninstalledDeviceMessage(DeviceMessage):
    """
    When a device has been uninstalled
    """
    cmd = 'U'

    def visit(self, aMessageHandler):
        aMessageHandler.uninstalled_device(self)

    def __str__(self):
        return "Uinstalled {0}".format(super().__str__())

