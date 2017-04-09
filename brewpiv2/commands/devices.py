from .base import ControllerCommand


class ListInstalledDevicesCommand(ControllerCommand):
    cmd = "d"


class ListAvailableDevicesCommand(ControllerCommand):
    cmd = "h"
