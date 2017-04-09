from .base import ControllerCommand


class ListInstalledDevicesCommand(ControllerCommand):
    cmd = "d"

    default_options = {
        'r': 1
    }

class ListAvailableDevicesCommand(ControllerCommand):
    cmd = "h"

    default_options = {
        'u': -1,
        'v': 1
    }
