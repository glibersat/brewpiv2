from .base import ControllerCommand


class ControlSettingsCommand(ControllerCommand):
    """
    Request Control Settings
    """
    cmd = "j"

    def __init__(self,
                 beer2fridge_kp=None, beer2fridge_ti=None, beer2fridge_td=None, beer2fridge_maxdif=None,
                 heater1_kp=None, heater1_ti=None, heater1_td=None, heater1_pwm_period=None,
                 heater2_kp=None):
        super().__init__()

        # Heater 1
        self.options['heater1_kp'] = heater1_kp
        self.options['heater1_ti'] = heater1_ti
        self.options['heater1_td'] = heater1_td
        self.options['heater1PwmPeriod'] = heater1_pwm_period

        # Beer2fridge
        self.options['beer2fridge_kp'] = beer2fridge_kp
        self.options['beer2fridge_ti'] = beer2fridge_ti
        self.options['beer2fridge_td'] = beer2fridge_td
        self.options['beer2fridge_pidMax'] = beer2fridge_maxdif

        # Heater 2
        self.options['heater2_kp'] = heater2_kp


