"""This module traslates obd codes to a nicer form"""


def find_converter(query, result):
    mode = query[0]
    code = query[1]
    if result == "NO DATA" or result == "?":
        return result
    else:
        if mode == "01":
            if code == "04":
                return eng_load(result)
            if code == "05":
                return eng_cool_temp(result)
            if code == "0c":
                return eng_rpm(result)
            if code == "0d":
                return speed(result)
            if code == "10":
                return mass_air_flow(result)
            if code == "11":
                return throttle_pos(result)
            if code == "1f":
                return run_time(result)
            if code == "2f":
                return fuel_tank_level(result)
            if code == "46":
                return amb_air_temp(result)
            if code == "51":
                return fuel_type(result)
            if code == "5c":
                return eng_oil_temp(result)


def eng_load(result):
    """Returun the engine load"""
    return int(result[0], 16) * 100 // 255


def eng_cool_temp(result):
    """Return the engine coolant temperature in Celsius"""
    return int(result[0], 16) - 40


def eng_rpm(result):
    """Return the engine rpm"""
    return (int(result[0], 16) * 256 + int(result[1], 16)) // 4


def speed(result):
    """Return the car speed in km/h"""
    return int(result[0], 16)


def mass_air_flow(result):
    """Return the mass air flow rate in g/s"""
    return (int(result[0], 16) * 256 + int(result[1], 16)) // 100


def throttle_pos(result):
    """Return the throttle position"""
    return int(result[0], 16) * 100 // 255


def run_time(result):
    """Return the run time since engine start"""
    return int(result[0], 16) * 256 + int(result[1], 16)


def fuel_tank_level(result):
    """Return the fuel tank input"""
    return int(result[0], 16) * 100 // 255


def amb_air_temp(result):
    """Return the ambient air temperature"""
    return int(result[0], 16) - 40


def fuel_type(result):
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


def eng_oil_temp(result):
    """Return the engine oil temp"""
    return int(result[0], 16), 40
