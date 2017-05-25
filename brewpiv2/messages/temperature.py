from .base import Message
from .decoder import register_to_decoder


@register_to_decoder()
class TemperaturesMessage(Message):
    """
    Receive Temperatures update
    """
    cmd = 'T'

    data_mapping = {
        'BeerTemp': 'beer_temp',
        'BeerSet': 'beer_setpoint',
        'BeerAnn': 'beer_annotation',
        'FridgeTemp': 'fridge_temp',
        'FridgeSet': 'fridge_setpoint',
        'FridgeAnn': 'fridge_annotation',
        'RoomTemp': 'room_temp',
        'State': 'state'
    }

    def __init__(self, beer_temp, beer_setpoint, beer_annotation,
                 fridge_temp, fridge_setpoint, fridge_annotation,
                 room_temp, state):
        self.beer_temp = beer_temp
        self.beer_setpoint = beer_setpoint
        self.beer_annotation = beer_annotation
        self.fridge_temp = fridge_temp
        self.fridge_setpoint = fridge_setpoint
        self.fridge_annotation = fridge_annotation
        self.room_temp = room_temp
        self.state = state

    def visit(self, aMessageHandler):
        aMessageHandler.temperatures(self)

    def __str__(self):
        return "Temperatures <...>"
