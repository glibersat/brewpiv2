import json


class Message:
    """
    A `Message` is a high level representation of an information sent from the
    controller such as the list of available devices or a temperature.
    """
    cmd = None

    @classmethod
    def raw_to_dict(cls, raw_message):
        """
        Convert a raw message to a python key value dictionary
        """
        if not raw_message:
            raise ValueError("Empty Message")

        if raw_message[0] != cls.cmd:
            raise ValueError("Wrong message type, can't decode.")

        return json.loads(raw_message[2:])

    @classmethod
    def from_raw(cls, raw_message):
        """
        Given a raw message, make it an object of the system by decoding the
        message then using the parameters as constructor arguments.
        """
        # First, make the message a dictionary
        msg_dict = cls.raw_to_dict(raw_message)

        # Map constuctor arguments to message data values
        constructor_parameters = {}
        for letter_key, parameter_name in cls.data_mapping.items():
            constructor_parameters[parameter_name] = msg_dict[letter_key]

        return cls(**constructor_parameters)
