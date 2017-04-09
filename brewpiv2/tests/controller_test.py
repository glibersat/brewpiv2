from unittest.mock import patch, call

from ..controller import BrewPiController


class TestController:
    def test_connect(self):
        ctrl = BrewPiController('loop://?logging=debug')
        ctrl.connect()
