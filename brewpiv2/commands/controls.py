from .base import ControllerCommand


class ControlSettingsCommand(ControllerCommand):
    """
    Request Control Settings
    """
    cmd = "j"

    def __init__(self, heater1_kp=None):
        super().__init__()

        self.options['heater1_kp'] = heater1_kp

