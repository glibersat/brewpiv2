from .base import Message
from .decoder import register_to_decoder


@register_to_decoder()
class ControlConstantsMessage(Message):
    """
    Receive Control Constants changes
    """
    cmd = 'S'

    mode = None
    beer_setpoint = None
    fridge_setpoint = None

    data_mapping = {
        'mode': 'mode',
        'beerSet': 'beer_setpoint',
        'fridgeSet': 'fridge_setpoint'
    }

    def __init__(self, mode, beer_setpoint, fridge_setpoint):
        self.mode = mode
        self.beer_setpoint = beer_setpoint
        self.fridge_setpoint = fridge_setpoint

    def visit(self, aMessageHandler):
        aMessageHandler.control_constants(self)

    def __str__(self):
        return "Control Constants <mode:{0}, beer setpoint:{1}, fridget setpoint:{2}>".format(self.mode,
                                                                                              self.beer_setpoint,
                                                                                              self.fridge_setpoint)


@register_to_decoder()
class ControlSettingsMessage(Message):
    """
    Receive Control Settings changes
    """
    cmd = 'C'

    data_mapping = {
        'tempFormat': 'temp_format',

        'heater1_kp': 'heater1_kp',
        'heater1_ti': 'heater1_ti',
        'heater1_td': 'heater1_td',
        'heater1_infilt': 'heater1_infilter',
        'heater1_dfilt': 'heater1_dfilter',
        'heater1PwmPeriod': 'heater1_pwm_period',

        'heater2_kp': 'heater2_kp',
        'heater2_ti': 'heater2_ti',
        'heater2_td': 'heater2_td',
        'heater2_infilt': 'heater2_infilter',
        'heater2_dfilt': 'heater2_dfilter',
        'heater2PwmPeriod': 'heater2_pwm_period',

        'cooler_kp': 'cooler_kp',
        'cooler_ti': 'cooler_ti',
        'cooler_td': 'cooler_td',
        'cooler_infilt': 'cooler_infilter',
        'cooler_dfilt': 'cooler_dfilter',
        'coolerPwmPeriod': 'cooler_pwm_period',

        'beer2fridge_kp': 'beer2fridge_kp',
        'beer2fridge_ti': 'beer2fridge_ti',
        'beer2fridge_td': 'beer2fridge_td',
        'beer2fridge_infilt': 'beer2fridge_infilter',
        'beer2fridge_dfilt': 'beer2fridge_dfilter',

        'minCoolTime': 'min_cool_time',
        'minCoolIdleTime': 'min_cool_idle_time',
        'beer2fridge_pidMax': 'beer2fridge_pid_max',
        'deadTime': 'deadtime'
    }

    def __init__(self, temp_format,
                 heater1_kp, heater1_ti, heater1_td, heater1_infilter, heater1_dfilter, heater1_pwm_period,
                 heater2_kp, heater2_ti, heater2_td, heater2_infilter, heater2_dfilter, heater2_pwm_period,
                 cooler_kp, cooler_ti, cooler_td, cooler_infilter, cooler_dfilter, cooler_pwm_period,
                 min_cool_time, min_cool_idle_time,
                 beer2fridge_kp, beer2fridge_ti, beer2fridge_td, beer2fridge_infilter, beer2fridge_dfilter, beer2fridge_pid_max,
                 deadtime):
        self.temp_format = temp_format

        # heater 1
        self.heater1_kp = heater1_kp
        self.heater1_ti = heater1_ti
        self.heater1_td = heater1_td
        self.heater1_infilter = heater1_infilter
        self.heater1_dfilter = heater1_dfilter

        self.heater1_pwm_period = heater1_pwm_period

        # heater 2
        self.heater2_kp = heater2_kp
        self.heater2_ti = heater2_ti
        self.heater2_td = heater2_td
        self.heater2_infilter = heater2_infilter
        self.heater2_dfilter = heater2_dfilter

        self.heater2_pwm_period = heater2_pwm_period

        # cooler 1
        self.cooler_kp = cooler_kp
        self.cooler_ti = cooler_ti
        self.cooler_td = cooler_td
        self.cooler_infilter = cooler_infilter
        self.cooler_dfilter = cooler_dfilter

        self.cooler_pwm_period = cooler_pwm_period

        self.min_cool_time = min_cool_time
        self.min_cool_idle_time = min_cool_idle_time

        # beer2fridge
        self.beer2fridge_kp = beer2fridge_kp
        self.beer2fridge_ti = beer2fridge_ti
        self.beer2fridge_td = beer2fridge_td
        self.beer2fridge_infilter = beer2fridge_infilter
        self.beer2fridge_dfilter = beer2fridge_dfilter
        self.beer2fridge_pid_max = beer2fridge_pid_max

        self.deadtime = deadtime


    def visit(self, aMessageHandler):
        aMessageHandler.control_settings(self)

    def __str__(self):
        return "Control Settings <...>"
