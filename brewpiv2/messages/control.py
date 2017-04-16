from .base import Message
from .decoder import register_to_decoder


@register_to_decoder()
class ControlSettingsMessage(Message):
    """
    Ask the controller for a Control Settings change
    """
    cmd = 'S'

    mode = None
    beer_setpoint = None
    fridge_setpoint = None

    data_mapping = {
        'mode': 'mode',
        'beerSet': 'beer_setpoint',
        'fridgeSet': 'fridge_setpoint'
    }

    def __init__(self, mode, beer_setpoint, fridge_setpoint):
        self.mode = mode
        self.beer_setpoint = beer_setpoint
        self.fridge_setpoint = fridge_setpoint

    def __str__(self):
        return "Control Settings <mode:{0}, beer setpoint:{1}, fridget setpoint:{2}>".format(self.mode,
                                                                                             self.beer_setpoint,
                                                                                             self.fridge_setpoint)
