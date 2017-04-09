import re
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

        self.buffer = ''

    def connect(self):
        """
        Initiate a serial connection to the controller
        """
        LOGGER.debug("Opening controller at: {0}".format(self.serial_port))
        self.serial = serial.serial_for_url(self.serial_port, 57600, timeout=0)
        self.serial.write_timeout = 2

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
        full_message = "{0}\n".format(raw_message)
        self.serial.write(full_message.encode('ascii'))
        self.serial.flush()

    def process_messages(self):
        in_waiting = self.serial.inWaiting()
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

            lines = self.buffer.partition('\n') # returns 3-tuple with line, separator, rest
            if not lines[1]:
                # '\n' not found, first element is incomplete line
                self.buffer = lines[0]
            else:
                # complete line received, [0] is complete line [1] is separator [2] is the rest
                self.buffer = lines[2]
                yield lines[0]

    def read_messages(self):
        """
        Read messages from controller wire and return them as iterator
        """
        for raw_message in self.read_message():
            LOGGER.debug("Received {0}".format(raw_message))
            yield raw_message
