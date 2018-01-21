def find_converter(query, result):
    mode = query[0]
    code = query[1]
    if result == "NO DATA":
        return result
    else:
        if mode == "01":
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
