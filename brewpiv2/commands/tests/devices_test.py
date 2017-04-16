from ..devices import (
    ListAvailableDevicesCommand,
    ListInstalledDevicesCommand
)


class TestSerialization:
    def test_list_available_devices(self):
        cmd = ListAvailableDevicesCommand()
        data = cmd.render()

        is_same = ListAvailableDevicesCommand.compare_data(data, "h{u:-1}")
        assert(is_same)

    def test_list_available_devices_with_values(self):
        cmd = ListAvailableDevicesCommand(with_values=True)
        data = cmd.render()

        is_same = ListAvailableDevicesCommand.compare_data(data, "h{u:-1,v:1}")
        assert(is_same)

    def test_list_installed_devices(self):
        cmd = ListInstalledDevicesCommand()
        data = cmd.render()
        
        is_same = ListInstalledDevicesCommand.compare_data(data, "d")
        assert(is_same)

    def test_list_installed_devices_with_values(self):
        cmd = ListInstalledDevicesCommand(with_values=True)
        data = cmd.render()

        is_same = ListInstalledDevicesCommand.compare_data(data, "d{r:1}")
        assert(is_same)

