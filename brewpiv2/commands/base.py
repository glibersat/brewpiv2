import json
import re
from copy import copy


class ControllerCommand:
    """
    Any command that can be send to a `BrewPiController`
    """
    cmd = None

    default_options = {}

    def __init__(self):
        self.options = copy(self.default_options)

    @staticmethod
    def make_data_json(data):
        """
        Given some data string, make it a parseable json
        """
        return re.sub(r'([a-zA-Z_]+)', r'"\1"', data)

    @staticmethod
    def compare_data(data1, data2):
        data1_cmd = data1[0]
        data1_json_options = ControllerCommand.make_data_json(data1[1:])
        if data1_json_options:
            data1_options = json.loads(data1_json_options)
        else:
            data1_options = None

        data2_cmd = data2[0]
        data2_json_options = ControllerCommand.make_data_json(data2[1:])
        if data2_json_options:
            data2_options = json.loads(data2_json_options)
        else:
            data2_options = None

        return (data1_cmd == data2_cmd) and (data1_options == data2_options)

    def render(self):
        """
        Render this command as a brewpi-formatted string
        """
        # If we don't have options, just return command name
        if self.options == {}:
            return self.cmd

        # Don't serialize options without a value
        cleaned_options = {key: value
                           for key, value in self.options.items()
                           if value is not None}

        json_options = json.dumps(cleaned_options)

        # Remove quotes around keys (BrewPi doesn't really use true json)
        cmd_options = re.sub(r'"(\S*?)"', '\\1', json_options)

        cmd_with_options = "{0}{1}".format(self.cmd,
                                           cmd_options)

        return cmd_with_options
