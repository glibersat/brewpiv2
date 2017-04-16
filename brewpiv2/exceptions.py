class ControllerPortNotOpenException(Exception):
    """
    When a serial port is not opened yet
    """

class ControllerNotConnectedException(Exception):
    """
    When a serial port is open but the controller isn't yet connected (i.e.
    recognized as a BrewPi Device)
    """
