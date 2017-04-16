import pytest
import serial

from ..controller import BrewPiController
from ..exceptions import (
    ControllerPortNotOpenException,
    ControllerNotConnectedException
)


class FakeCommand:
    def render(self):
        return 'fake'


class TestDisconnectedController:
    def setup_method(self):
        self.ctrl = BrewPiController('loop://?logging=debug')

    def test_port_does_not_exist(self):
        self.ctrl = BrewPiController('/dev/does_not_exist')
        assert(self.ctrl.connect() == False)

    def test_connect(self):
        assert(self.ctrl.connect() == True)

    def test_disconnect_not_connected(self):
        assert(self.ctrl.disconnect() is True)

    def test_connect_then_disconnect(self):
        self.ctrl.connect()
        assert(self.ctrl.disconnect() is True)

    def test_send_raw_command_no_port_open(self):
        with pytest.raises(ControllerPortNotOpenException):
            self.ctrl.send_raw('v')

    def test_send_command_no_port_open(self):
        with pytest.raises(ControllerNotConnectedException):
            self.ctrl.send(FakeCommand())

    def test_process_messages(self):
        with pytest.raises(ControllerPortNotOpenException):
            list(self.ctrl.process_messages())

    def test_filter_out_msg(self):
        log_msg = 'D:{"logType":"E","logID":10,"V":[10]}\n'
        cmd_msg = 'h:[{"i":0,"t":4,"c":1,"b":0,"f":3,"h":1,"d":0,"p":17,"x":0}]\n'
        input_string = "{0}{1}{2}".format(cmd_msg[0:3],
                                          log_msg,
                                          cmd_msg[3:])

        result_cmd, result_log_messages = self.ctrl._filter_out_log_messages(input_string)
        assert(result_cmd == cmd_msg)
        assert(result_log_messages == [log_msg])

    def test_coerce_message(self):
        log_msg = 'D:{"logType":"E","logID":10,"V":[10]}\n'
        cmd_msg = 'h:[{"i":0,"t":4,"c":1,"b":0,"f":3,"h":1,"d":0,"p":17,"x":0}]'
        self.ctrl.buffer = "{0}{1}{2}\n".format(cmd_msg[0:3],
                                                log_msg,
                                                cmd_msg[3:])

        messages = list(self.ctrl._coerce_message_from_buffer())
        assert(len(messages) == 2)
        assert(messages[0] == log_msg)
        assert(messages[1] == cmd_msg)

    def test_coerce_message_not_enough_data(self):
        log_msg = 'D:{"logType":"E","logID":10,"V":[10]}\n'
        cmd_msg = 'h:[{"i":0,"t":4,"c":'
        self.ctrl.buffer = "{0}{1}{2}".format(cmd_msg[0:3],
                                              log_msg,
                                              cmd_msg[3:])

        messages = list(self.ctrl._coerce_message_from_buffer())
        assert(len(messages) == 1)
        assert(messages[0] == log_msg)


class TestConnectedController:
    def setup_method(self):
        self.ctrl = BrewPiController('loop://?logging=debug')
        self.ctrl.connect()

    def test_send_raw_command(self):
        self.ctrl.send_raw('v')

    def test_send_command(self):
        self.ctrl.send(FakeCommand())

    def test_process_messages(self):
        list(self.ctrl.process_messages())
