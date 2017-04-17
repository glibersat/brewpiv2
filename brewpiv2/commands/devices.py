from .base import ControllerCommand


class ListInstalledDevicesCommand(ControllerCommand):
    """
    Request listing installed devices
    """
    cmd = "d"

    def __init__(self, with_values=False):
        super().__init__()
        if with_values:
            self.options['r'] = 1


class ListAvailableDevicesCommand(ControllerCommand):
    """
    Request listing available (= not installed) devices
    """
    cmd = "h"

    default_options = {
        'u': -1,
    }

    def __init__(self, with_values=False):
        super().__init__()
        if with_values:
            self.options['v'] = 1


class InstallDeviceCommand(ControllerCommand):
    """
    Install an available device
    """
    cmd = 'U'

    def __init__(self, slot, assigned_to_chamber, assigned_to_beer,
                 function, hardware_type, pin, pin_inverted=0,
                 address=None):
        super().__init__()

        self.options['i'] = slot
        self.options['c'] = assigned_to_chamber
        self.options['b'] = assigned_to_beer
        self.options['f'] = function
        self.options['h'] = hardware_type
        self.options['p'] = pin
        self.options['x'] = int(pin_inverted)
        self.options['a'] = address


class UninstallDeviceCommand(ControllerCommand):
    """
    Uninstall a device
    """
    cmd = 'U'

    default_options = {
        'f': 0,
    }

    def __init__(self, slot):
        super().__init__()

        self.options['i'] = slot

#  Uninstall:
#  U:{"i":"1","c":"1","b":"0","f":"0","h":"2","p":"0","a":"28126E5E0700002F"}
#  Pin
#  U:{"i":"25","c":"1","b":"0","f":"0","h":"1","p":"10","x":"0"}
#  Install:
#  Temp Sensor
#  U:{"i":"22","c":"1","b":"0","f":"5","h":"2","p":"0","a":"28126E5E0700002F"}
#  Actuator/Pin ctrl
#  U:{"i":"25","c":"1","b":"0","f":"3","h":"1","p":"10","x":"0"}
