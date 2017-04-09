from .base import Message
from .decoder import register_to_decoder


@register_to_decoder()
class AvailableDeviceMessage(Message):
    """
    Available devices (not installed) on the controller
    """
    cmd = 'h'

    data_mapping = {
        'i': 'slot',
        't': 't',
        'c': 'c',
        'b': 'b',
        'f': 'f',
        'h': 'hardware_type',
        'd': 'd',
        'p': 'pin',
        'x': 'x',
        'a': 'address',
        'j': 'value'
    }

    def __init__(self, slot, t, c, b, f, hardware_type, d, pin, x=None, address=None, value=None):
        self.slot = slot
        self.t = t
        self.c = c
        self.b = b
        self.f = f
        self.hardware_type = hardware_type
        self.d = d
        self.pin = pin
        self.x = x
        self.address = address
        self.value = value

    def __str__(self):
        return "Available Device <slot:{self.slot}, t:{self.t}, " \
            "c:{self.c}, b:{self.b}, f:{self.f}, hardware_type:{self.hardware_type}, " \
            "d:{self.d}, pin:{self.pin}, x:{self.x}, address:{self.address}, value:{self.value}>".format(self=self)
