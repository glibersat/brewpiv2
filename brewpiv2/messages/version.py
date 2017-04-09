from .base import Message
from .decoder import register_to_decoder


@register_to_decoder()
class VersionMessage(Message):
    cmd = "N"

    version = None
    build = None
    board = None

    data_mapping = {
        'v': 'version',
        'n': 'build',
        'b': 'board'
    }

    def __init__(self, version, build, board):
        self.version = version
        self.build = build
        self.board = board

    def __str__(self):
        return "Version <version:{0}, build:{1}, board: {2}".format(self.version,
                                                                    self.build,
                                                                    self.board)
