class HardwareType:
    (DIGITAL_PIN, TEMP_SENSOR,
     DS2413, DS2408VALVE) = range(1, 5)  # Hardware Type

    hardware_types = {0: 'Unknown hardware',
                      DIGITAL_PIN: 'Digital Pin',
                      TEMP_SENSOR: 'Temperature Sensor',
                      DS2413: 'DS2413 Expansion Board',
                      DS2408VALVE: 'DS2408 Valve Board'}

    @classmethod
    def to_str(cls, hardware_type):
        """
        Represent hardware type as string
        """
        return cls.hardware_types[hardware_type]


class DeviceType:
    (TEMP_SENSOR, SWITCH_SENSOR,
     SWITCH_ACTUATOR, PWM_ACTUATOR,
     MANUAL_ACTUATOR) = range(1, 6)  # Device type

    device_types = {0: 'Unknown device type',
                    TEMP_SENSOR: 'Temperature Sensor',
                    SWITCH_SENSOR: 'Switch Sensor',
                    SWITCH_ACTUATOR: 'Switch Actuator',
                    PWM_ACTUATOR: 'PWM Actuator',
                    MANUAL_ACTUATOR: 'Manual Actuator'}

    @classmethod
    def to_str(cls, device_type):
        """
        Represent device type as string
        """
        return cls.device_types[device_type]


class DeviceAssignation:
    (CHAMBER,
     BEER) = range(1, 3)


class DeviceState:
    (STATE_OFF,
     STATE_ON) = range(0, 2)

    
class DeviceFunction:
    (NONE,
     CHAMBER_DOOR,
     CHAMBER_HEATER,
     CHAMBER_COOLER,
     CHAMBER_LIGHT,
     CHAMBER_TEMP,
     LOG1_TEMP,
     CHAMBER_FAN,
     MANUAL_ACTUATOR,
     BEER_TEMP,
     NOIDEA1,
     NOIDEA2,
     NOIDEA3,
     NOIDEA4,
     NOIDEA5,
     NOIDEA6,
     NOIDEA7,
     LOG2_TEMP,
     LOG3_TEMP) = range(0, 19)

    device_functions = {NONE: 'None',
                        CHAMBER_DOOR: 'Chamber Door',
                        CHAMBER_HEATER: 'Chamber Heater',
                        CHAMBER_COOLER: 'Chamber Cooler',
                        CHAMBER_LIGHT: 'Chamber Light',
                        CHAMBER_TEMP: 'Chamber Temp',
                        LOG1_TEMP: 'Log1 Temp',
                        CHAMBER_FAN: 'Chamber Fan',
                        MANUAL_ACTUATOR: 'Manual Actuator',
                        BEER_TEMP: 'Beer Temp',
                        LOG2_TEMP: 'Log2 Temp',
                        LOG3_TEMP: 'Log3 Temp'}

    @classmethod
    def to_str(cls, function):
        """
        Represent device function as string
        """
        return cls.device_functions[function]
