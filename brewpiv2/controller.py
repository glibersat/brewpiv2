import io
import logging
import serial

LOGGER = logging.getLogger(__name__)


class BrewPiController:
    """
    The actual BrewPi Controller.
    Handle reading and writing commands to/from the serial port.
    """
    def __init__(self, serial_port):
        self.serial = None
        self.serial_port = serial_port

    def connect(self):
        """
        Initiate a serial connection to the controller
        """
        LOGGER.debug("Opening controller at: {0}".format(self.serial_port))
        self.serial = serial.serial_for_url(self.serial_port, 57600, timeout=0.2)
        self.serial_io = io.TextIOWrapper(io.BufferedRWPair(self.serial, self.serial))
        return self.serial.is_open

    def send(self, aCommand):
        """
        Send a `Command` to the controller
        """
        rendered_cmd = aCommand.render()
        LOGGER.debug("Sending to controller: {0}".format(rendered_cmd))
        self.send_raw(rendered_cmd)

    def send_raw(self, raw_message):
        """
        Send raw payload to controller
        """
        self.serial_io.write("{0}\n".format(raw_message))
        self.serial_io.flush()

    def read_messages(self):
        """
        Read messages from controller wire and return them as iterator
        """
        for payload in self.serial_io.readlines():
            yield payload
