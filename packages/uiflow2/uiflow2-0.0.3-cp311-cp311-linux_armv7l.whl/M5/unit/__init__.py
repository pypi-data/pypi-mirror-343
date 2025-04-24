# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

_attrs = {
    "ADCV11Unit": "adc_v11",
    "ADCUnit": "adc",
    "AngleUnit": "angle",
    "ColorUnit": "color",
    "DACUnit": "dac",
    "DAC2Unit": "dac2",
    "EarthUnit": "earth",
    "ENVUnit": "env",
    "ENVPROUnit": "envpro",
    "EXTIOUnit": "extio",
    "EXTIO2Unit": "extio2",
    "FingerUnit": "finger",
    "TMOSUnit": "tmos",
    "GPSV11Unit": "gps_v11",
    "IMUUnit": "imu",
    "IMUProUnit": "imu_pro",
    "PAHUBUnit": "pahub",
    "RGBUnit": "rgb",
    "Roller485Unit": "roller485",
    "RollerCANUnit": "rollercan",
    "ISO485Unit": "rs485_iso",
    "RS485Unit": "rs485",
    "ToFUnit": "tof",
}

import sys
def __getattr__(attr):
    mod = _attrs.get(attr, None)
    if mod is None:
        raise AttributeError(attr)
    if sys.platform == "linux": # for linux
        value = getattr(__import__(mod, globals(), None, [attr], 1), attr)  # python
    else:
        value = getattr(__import__(mod, None, None, True, 1), attr)
    globals()[attr] = value
    return value
