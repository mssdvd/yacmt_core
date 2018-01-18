def eng_cool_temp(codes):
    """Return the engine coolant temperature in Celsius"""
    return int(codes[0], 16) - 40


def eng_rpm(codes):
    """Return the engine rpm"""
    return (int(codes[0], 16) * 256 + int(codes[1], 16)) // 4


def speed(codes):
    """Return the car speed in km/h"""
    return int(codes[0], 16)


def mass_air_flow(codes):
    """Return the mass air flow rate in g/s"""
    return (int(codes[0], 16) * 256 + int(codes[1], 16)) // 100


def throttle_pos(codes):
    """Return the throttle position"""
    return int(codes[0], 16) * 100 // 255
