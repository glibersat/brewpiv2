from abc import ABC, abstractmethod
import re
import logging
import serial
from serial.tools import list_ports

from .exceptions import (
    ControllerNotConnectedException,
    ControllerPortNotOpenException
)
from .utils import (
    Observable, Observer, Event,
    Visitor
)

LOGGER = logging.getLogger(__name__)

# -- events -- #
controller_connected = Event("controller_connected", "A controller has connected")
controller_disconnected = Event("controller_disconnected", "A controller has been disconnected")


# -- decorators -- #
def requires_port_open(f):
    """
    Only call method if controller port is open and readable, otherwise throw
    an exception.
    """
    def wrapper(obj, *args):
        if (obj.serial and obj.serial.is_open) is True:
            return f(obj, *args)
        else:
            raise ControllerPortNotOpenException()
    return wrapper


def requires_connected(f):
    """
    Only call method if controller is connected, otherwise throw an exception.
    """
    def wrapper(obj, *args):
        if obj.is_connected is True:
            return f(obj, *args)
        else:
            raise ControllerNotConnectedException()
    return wrapper


# -- Classes -- #
class BrewPiController(Observable):
    """
    The actual BrewPi Controller.
    Handle reading and writing commands to/from the serial port.
    """
    def __init__(self, serial_port):
        super().__init__()

        self.serial = None
        self.serial_port = serial_port

        self.buffer = ''

        self.is_connected = False

    def log_debug(self, message):
        self.log(message, level=logging.DEBUG)

    def log(self, message, level=logging.INFO):
        LOGGER.log(level, "[{0}] {1}".format(self.serial_port, message))

    def connect(self):
        """
        Initiate a serial connection to the controller
        """
        self.log_debug("Opening controller...")

        try:
            self.serial = serial.serial_for_url(self.serial_port, 57600, timeout=0)
            self.serial.write_timeout = 2
            self.is_connected = True
        except serial.serialutil.SerialException as e:
            self.log("Error while opening controller, aborting ({0})".format(e), level=logging.WARNING)
            return False

        if self.is_connected:
            self.notify(controller_connected, self)
            self.log_debug("Controller connected!")

        return self.is_connected

    def disconnect(self):
        if (self.serial is not None) and self.serial.is_open:
            self.serial.close()
            self.is_connected = False

        self.notify(controller_disconnected, self)
        self.log_debug("Controller disconnected".format(self.serial_port))

        return not self.is_connected

    @requires_connected
    def send(self, aCommand):
        """
        Send a `Command` to the controller
        """
        rendered_cmd = aCommand.render()
        self.log_debug("Sending to controller: {0}".format(rendered_cmd))
        self.send_raw(rendered_cmd)

    @requires_port_open
    def send_raw(self, raw_message):
        """
        Send raw payload to controller
        """
        full_message = "{0}\n".format(raw_message)
        self.serial.write(full_message.encode('ascii'))
        self.serial.flush()

    @requires_port_open
    def process_messages(self):
        in_waiting = self.serial.in_waiting
        if in_waiting > 0:
            new_data = self.serial.read(in_waiting)
            new_data = new_data.decode("utf8")

            if new_data:
                self.buffer += new_data
                yield from self._coerce_message_from_buffer()

    def _filter_out_log_messages(self, input_string):
        """
        Removes log messages from string received from Serial
        log messages are sometimes printed in the middle of a JSON string, which causes decode errors
        this function filters them out and yield them
        """
        m = re.compile("D:\{.*?\}\r?\n")
        log_messages = m.findall(input_string)
        stripped = m.sub('', input_string)

        return (stripped, log_messages)

    def _coerce_message_from_buffer(self):
        """
        Try to make a message out of the buffer and find log messages intertwined
        into the buffer.
        """
        while '\n' in self.buffer:
            stripped_buffer, log_messages = self._filter_out_log_messages(self.buffer)
            if len(log_messages) > 0:
                yield from log_messages
                self.buffer = stripped_buffer
                continue

            lines = self.buffer.partition('\n')  # returns 3-tuple with line, separator, rest
            if not lines[1]:
                # '\n' not found, first element is incomplete line
                self.buffer = lines[0]
            else:
                # complete line received, [0] is complete line [1] is separator [2] is the rest
                self.buffer = lines[2]
                yield lines[0].rstrip('\r').rstrip('\n')


class ControllerObserver(Observer):
    """
    Abstract class that answers to controller manager events
    """
    @abstractmethod
    def _on_controller_connected(self, aBrewPiController):
        pass

    @abstractmethod
    def _on_controller_disconnected(self, aBrewPiController):
        pass


class BrewPiControllerManager(Observable):
    """
    Helper for discovering BrewPi controllers on USB serial lines
    """
    BREWPI_PHOTON_HWID = r"VID:PID=2B04:C006"

    def __init__(self):
        super().__init__()

        self.controllers = {}

    def update(self):
        """
        Update list of serial ports where a BrewPi Controller *might* be
        attached.

        Yields new controllers
        """
        detected_ports = list(list_ports.grep(regexp=self.BREWPI_PHOTON_HWID))

        # Remove stale devices
        for device, controller in list(self.controllers.items()):
            found = False

            # Look for our device in the detected ports
            for port in detected_ports:
                if port.device == device:
                    found = True
                    break

            # Mark as disconnected if stale
            if not found:
                controller.disconnect()
                self.controllers.pop(device)

        # Add new devices
        for port in detected_ports:
            if port.device not in self.controllers:
                LOGGER.info("Found new controller on port {0}".format(port.device))
                self.controllers[port.device] = BrewPiController(port.device)

                yield self.controllers[port.device]


class MessageHandler(ABC):
    """
    An abstract class handling visits from Messages
    """
    def accept(self, aMessage):
        aMessage.visit(self)

    @abstractmethod
    def installed_device(self, anInstalledDeviceMessage):
        raise NotImplementedError

    @abstractmethod
    def uninstalled_device(self, anUninstalledDeviceMessage):
        raise NotImplementedError

    @abstractmethod
    def available_device(self, anAvailableDeviceMessage):
        raise NotImplementedError

    @abstractmethod
    def log_message(self, aLogMessage):
        raise NotImplementedError

    @abstractmethod
    def control_settings(self, aControlSettingsMessage):
        raise NotImplementedError

    @abstractmethod
    def control_constants(self, aControlConstantsMessage):
        raise NotImplementedError

    @abstractmethod
    def temperatures(self, aTemperaturesMessage):
        raise NotImplementedError
