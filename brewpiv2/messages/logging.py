from .base import Message
from .decoder import register_to_decoder

@register_to_decoder()
class LogMessage(Message):
    """
    A log message coming from the controller
    """
    cmd = 'D'

    level = None
    id = None
    message = None

    data_mapping = {
        'logType': 'level',
        'logID': 'id',
        'V': 'message'
    }

    def __init__(self, level, id, message):
        self.level = level
        self.id = id
        self.message = message

    def __str__(self):
        return "LogMessage <level:{0}, id:{1}, msg:{2}>".format(self.level,
                                                                self.id,
                                                                self.message)

