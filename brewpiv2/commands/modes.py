from .base import ControllerCommand

class ModeCommand(ControllerCommand):
    """
    Common class for modes on the controller (Beer, Fridge, Profile, Off)
    """
    cmd = 'j'

    mode = None
    setpoint_name = None

    def __init__(self, setpoint=None):
        super().__init__()
        self.options['mode'] = self.mode

    @property
    def setpoint(self):
        return self.options[self.setpoint_name]

    @setpoint.setter
    def setpoint(self, value):
        self.options[self.setpoint_name] = value


class BeerModeCommand(ModeCommand):
    """
    Constant Beer Mode
    """
    mode = 'b'
    setpoint_name = 'beerSet'

class FridgeModeCommand(ModeCommand):
    """
    Constant Fridge Mode
    """
    mode = 'f'
    setpoint_name = 'frigeSet'

class OffModeCommand(ModeCommand):
    """
    Off mode: disable temperature control
    """
    mode = 'o'
