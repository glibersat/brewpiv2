import json


class Message:
    """
    A `Message` is a high level representation of an information sent from the
    controller such as the list of available devices or a temperature.
    """
    cmd = None

    @classmethod
    def raw_to_dicts(cls, raw_message):
        """
        Convert a raw message to python key-value dictionaries
        """
        if not raw_message:
            raise ValueError("Empty Message")

        if raw_message[0] != cls.cmd:
            raise ValueError("Wrong message type, can't decode.")

        decoded_messages = []
        json.loads(raw_message[2:], object_hook=decoded_messages.append)

        return decoded_messages

    @classmethod
    def from_raw(cls, raw_message):
        """
        Given a raw message, make it an object of the system by decoding the
        message then using the parameters as constructor arguments.
        """
        # First, make the message a dictionary
        for msg_dict in cls.raw_to_dicts(raw_message):
            # Map constuctor arguments to message data values
            constructor_parameters = {}
            for letter_key, parameter_name in cls.data_mapping.items():
                try:
                    constructor_parameters[parameter_name] = msg_dict[letter_key]
                except KeyError:
                    pass

            yield cls(**constructor_parameters)
