from ..modes import (
    BeerModeCommand, FridgeModeCommand,
    OffModeCommand, ProfileModeCommand
)


class TestSerialization:
    def test_setpoint_property(self):
        cmd = BeerModeCommand(setpoint=7.0)
        assert(cmd.setpoint == 7.0)

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

    def test_profile_mode(self):
        cmd = ProfileModeCommand(setpoint=10.0)
        data = cmd.render()

        is_same = ProfileModeCommand.compare_data(data, "j{mode: p, beerSet: 10.0}")
        assert(is_same)

    def test_off_mode(self):
        cmd = OffModeCommand(setpoint=20.0)
        data = cmd.render()

        is_same = OffModeCommand.compare_data(data, "j{mode: o}")
        assert(is_same)
