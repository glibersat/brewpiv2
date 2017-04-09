import json
import re


class ControllerCommand:
    """
    Any command that can be send to a `BrewPiController`
    """
    cmd = None

    def __init__(self):
        self.options = {}

    def render(self):
        # Don't serialize options without a value
        cleaned_json_options = {key: value
                                for key, value in self.options.items()
                                if value is not None}

        json_options = json.dumps(cleaned_json_options)

        # Remove quotes around keys (BrewPi doesn't really use true json)
        cmd_options = re.sub(r'"(\S*?)"', '\\1', json_options)

        cmd_with_options = "{0}{1}".format(self.cmd,
                                           cmd_options)

        return cmd_with_options.encode()
