from ..modes import (
    BeerModeCommand, FridgeModeCommand,
    OffModeCommand
)


class TestSerialization:
    def test_beer_mode(self):
        cmd = BeerModeCommand(setpoint=20.0)
        data = cmd.render()

        is_same = BeerModeCommand.compare_data(data, "j{mode: b, beerSet: 20.0}")
        assert(is_same)

    def test_fridge_mode(self):
        cmd = FridgeModeCommand(setpoint=18.0)
        data = cmd.render()

        is_same = FridgeModeCommand.compare_data(data, "j{mode: f, fridgeSet: 18.0}")
        assert(is_same)

    def test_off_mode(self):
        cmd = OffModeCommand(setpoint=20.0)
        data = cmd.render()

        is_same = OffModeCommand.compare_data(data, "j{mode: o}")
        assert(is_same)
