from .base import Message
from .decoder import register_to_decoder


class DeviceMessage(Message):
    """
    Abtract Class that holds common device information
    """
    (DIGITAL_PIN, TEMP_SENSOR,
     DS2413, DS2408VALVE) = range(1, 5)  # Hardware Type

    hardware_types = {0: 'Unknown hardware',
                      DIGITAL_PIN: 'Digital Pin',
                      TEMP_SENSOR: 'Temperature Sensor',
                      DS2413: 'DS2413 Expansion Board',
                      DS2408VALVE: 'DS2408 Valve Board'}

    (TEMP_SENSOR, SWITCH_SENSOR,
     SWITCH_ACTUATOR, PWM_ACTUATOR,
     MANUAL_ACTUATOR) = range(1, 6)  # Device type

    device_types = {0: 'Unknown device type',
                    TEMP_SENSOR: 'Temperature Sensor',
                    SWITCH_SENSOR: 'Switch Sensor',
                    SWITCH_ACTUATOR: 'Switch Actuator',
                    PWM_ACTUATOR: 'PWN Actuator',
                    MANUAL_ACTUATOR: 'Manual Actuator'}

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

    def hardware_type_str(self):
        """
        Represent hardware type as string
        """
        return self.hardware_types[self.hardware_type]

    def device_type_str(self):
        """
        Represent device type as string
        """
        return self.device_types[self.device_type]

    def __str__(self):
        return "Device <slot:{self.slot}, device_type:{device_type}, " \
            "chamber:{self.assigned_to_chamber}, beer:{self.assigned_to_beer}, " \
            "function:{self.function}, hardware_type:{hardware_type}, " \
            "d:{self.d}, pin:{self.pin}, pin_inverted?:{self.pin_inverted}, "\
            "output_nr:{self.output_nr}, " \
            "address:{self.address}, value:{self.value}>".format(self=self,
                                                                 device_type=self.device_type_str(),
                                                                 hardware_type=self.hardware_type_str())


@register_to_decoder()
class AvailableDeviceMessage(DeviceMessage):
    """
    Available devices (not installed) on the controller
    """
    cmd = 'h'

    def __str__(self):
        return "Available {0}".format(super().__str__())


@register_to_decoder()
class InstalledDeviceMessage(DeviceMessage):
    """
    Installed devices (installed) on the controller
    """
    cmd = 'd'

    def __str__(self):
        return "Installed {0}".format(super().__str__())
