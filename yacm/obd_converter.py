"""This module traslates obd codes to a nicer form"""

from typing import Tuple


def find_converter(query: Tuple[str, str], result: Tuple[str, ...]):
    mode = query[0]
    code = query[1]
    if result == "NO DATA" or result == "?":
        return result
    else:
        try:
            if mode == "01":
                if code == "4":
                    return eng_load(result)
                if code == "5":
                    return eng_cool_temp(result)
                if code == "a":
                    return intake_manifold_abs_press(result)
                if code == "c":
                    return eng_rpm(result)
                if code == "d":
                    return speed(result)
                if code == "f":
                    return intake_air_temp(result)
                if code == "10":
                    return mass_air_flow(result)
                if code == "11":
                    return throttle_pos(result)
                if code == "1f":
                    return run_time(result)
                if code == "2f":
                    return fuel_tank_level(result)
                if code == "42":
                    return control_mod_voltage(result)
                if code == "46":
                    return amb_air_temp(result)
                if code == "51":
                    return fuel_type(result)
                if code == "5c":
                    return eng_oil_temp(result)
        except:
            return "ERROR"


def eng_load(result: Tuple[str, ...]) -> int:
    """Returun the engine load"""
    return int(result[0], 16) * 100 // 255


def eng_cool_temp(result: Tuple[str, ...]) -> int:
    """Return the engine coolant temperature (C)"""
    return int(result[0], 16) - 40


def intake_manifold_abs_press(result: Tuple[str, ...]) -> int:
    """Retunr the intake manifold absolute pressure (kPa)"""
    return int(result[0], 16)


def eng_rpm(result: Tuple[str, ...]):
    """Return the engine rpm (RPM)"""
    return (int(result[0], 16) * 256 + int(result[1], 16)) // 4


def speed(result: Tuple[str, ...]) -> int:
    """Return the car speed (km/h)"""
    return int(result[0], 16)


def intake_air_temp(result: Tuple[str, ...]) -> int:
    """Return the intake air temperature (C)"""
    return int(result[0], 16) - 40


def mass_air_flow(result: Tuple[str, ...]):
    """Return the mass air flow rate (g/s)"""
    return (int(result[0], 16) * 256 + int(result[1], 16)) // 100


def throttle_pos(result: Tuple[str, ...]) -> int:
    """Return the throttle position"""
    return int(result[0], 16) * 100 // 255


def run_time(result: Tuple[str, ...]):
    """Return the run time since engine start (s)"""
    return int(result[0], 16) * 256 + int(result[1], 16)


def fuel_tank_level(result: Tuple[str, ...]) -> int:
    """Return the fuel tank input"""
    return int(result[0], 16) * 100 // 255


def control_mod_voltage(result: Tuple[str, ...]):
    """Return the control module voltage (V)"""
    return (int(result[0], 16) * 256 + int(result[1], 16)) // 1000


def amb_air_temp(result: Tuple[str, ...]) -> int:
    """Return the ambient air temperature (C)"""
    return int(result[0], 16) - 40


def fuel_type(result: Tuple[str, ...]) -> str:
    """Return the fuel type"""
    fuel_code = int(result[0], 16)
    if fuel_code == 0:
        fuel_string = "Not available"
    elif fuel_code == 1:
        fuel_string = "Gasolin"
    elif fuel_code == 2:
        fuel_string = "Methanol"
    elif fuel_code == 3:
        fuel_string = "Ethanol"
    elif fuel_code == 4:
        fuel_string = "Diesel"
    elif fuel_code == 5:
        fuel_string = "LPG"
    elif fuel_code == 6:
        fuel_string = "CNG"
    elif fuel_code == 7:
        fuel_string = "Propane"
    elif fuel_code == 8:
        fuel_string = "Electric"
    elif fuel_code == 9:
        fuel_string = "Bifuel running Gasoline"
    elif fuel_code == 10:
        fuel_string = "Bifuel running Methanol"
    elif fuel_code == 11:
        fuel_string = "Bifuel running Ethanol"
    elif fuel_code == 12:
        fuel_string = "Bifuel running LPG"
    elif fuel_code == 13:
        fuel_string = "Bifuel running CNG"
    elif fuel_code == 14:
        fuel_string = "Bifuel running Propane"
    elif fuel_code == 15:
        fuel_string = "Bifuel running Electricity"
    elif fuel_code == 16:
        fuel_string = "Bifuel running electric and combustion engine"
    elif fuel_code == 17:
        fuel_string = "Hybrid Gasoline"
    elif fuel_code == 18:
        fuel_string = "Hybrid Ethanol"
    elif fuel_code == 19:
        fuel_string = "Hybrid Diesel"
    elif fuel_code == 20:
        fuel_string = "Hybrid Electric"
    elif fuel_code == 21:
        fuel_string = "Hybrid running electric and combustion engine"
    elif fuel_code == 22:
        fuel_string = "Hybrid Regenerative"
    elif fuel_code == 23:
        fuel_string = "Bifuel running Diesel"
    return fuel_string


def eng_oil_temp(result: Tuple[str, ...]) -> int:
    """Return the engine oil temp (C)"""
    return int(result[0], 16) + 40
