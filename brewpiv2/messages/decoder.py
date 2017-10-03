import logging

LOGGER = logging.getLogger(__name__)


def register_to_decoder():
    """
    Register a controller message object to `MessageDecoder`
    """
    def _register_in_messagedecoder(message_type):
        RawMessageDecoder.register_message_type(message_type)
        return message_type

    return _register_in_messagedecoder


class RawMessageDecoder:
    """
    Decode messages coming from the controller as local objects
    """
    mapping = {}  # letter -> object mapping

    @classmethod
    def register_message_type(cls, aMessageType):
        """
        Add a Message type to mapping
        """
        LOGGER.debug("Registered message type {0} -> {1}".format(aMessageType.cmd, aMessageType))
        cls.mapping[aMessageType.cmd] = aMessageType

    def decode_controller_message(self, raw_message):
        """
        Given a raw controller message, make `Message` objects
        """
        if not raw_message:
            return None

        cmd = raw_message[0]

        try:
            message_type = self.mapping[cmd]
            yield from message_type.from_raw(raw_message)
        except KeyError:
            LOGGER.error("Message <{0}> not supported, dropping (was {1})".format(cmd, raw_message))
