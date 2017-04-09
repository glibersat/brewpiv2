import logging
import serial

LOGGER = logging.getLogger(__name__)


class BrewPiController:
    """
    The actual BrewPi Controller
    """
    def __init__(self, serial_port):
        self.serial = None
        self.serial_port = serial_port

    def connect(self):
        LOGGER.debug("Opening controller at: {0}".format(self.serial_port))
        self.serial = serial.serial_for_url(self.serial_port)
        return self.serial.is_open

    def send(self, aCommand):
        rendered_cmd = aCommand.render()
        LOGGER.debug("Sending to controller: {0}".format(rendered_cmd))
        self.serial.write("{0}\n".format(rendered_cmd))
        self.serial.flush()
