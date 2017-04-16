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
