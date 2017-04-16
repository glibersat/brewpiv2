from .base import ControllerCommand


class ModeCommand(ControllerCommand):
    """
    Common class for modes on the controller (Beer, Fridge, Profile, Off)
    """
    cmd = 'j'

    mode = None

    def __init__(self, setpoint=None):
        super().__init__()
        self.options['mode'] = self.mode


class ConstantTemperatureModeCommand(ModeCommand):
    """
    A mode with a constant temperature set point
    """
    setpoint_name = None

    def __init__(self, setpoint=None):
        super().__init__()
        self.setpoint = setpoint

    @property
    def setpoint(self):
        return self.options[self.setpoint_name]

    @setpoint.setter
    def setpoint(self, value):
        self.options[self.setpoint_name] = value


class BeerModeCommand(ConstantTemperatureModeCommand):
    """
    Constant Beer Mode
    """
    mode = 'b'
    setpoint_name = 'beerSet'


class FridgeModeCommand(ConstantTemperatureModeCommand):
    """
    Constant Fridge Mode
    """
    mode = 'f'
    setpoint_name = 'fridgeSet'


class ProfileModeCommand(ConstantTemperatureModeCommand):
    """
    Profile Beer Mode
    """
    mode = 'p'
    setpoint_name = 'beerSet'


class OffModeCommand(ModeCommand):
    """
    Off mode: disable temperature control
    """
    mode = 'o'
