import os
import sys

import obd_converter
import obd_io


def print_obd_values(values):
    for code, result in values.items():
        if code == '05':
            print("Engine coolant temperature:")
            print(str(obd_converter.eng_cool_temp(result)) + ' C')
        elif code == '0c':
            print("Engine rpm:")
            print(str(obd_converter.eng_rpm(result)))
        elif code == '0d':
            print("Speed:")
            print(str(obd_converter.speed(result)) + ' km/h')
        elif code == '10':
            print("MAF:")
            print(str(obd_converter.mass_air_flow(result)) + ' g/s')
        elif code == '11':
            print("Throttle position:")
            print(str(obd_converter.throttle_pos(result)) + ' %')


def main(port):
    obd_codes = ['05', '0c', '0d', '10', '11']
    mode = '01'
    comm = obd_io.OBD_IO(port)
    results = {}
    with comm:
        while True:
            for code in obd_codes:
                comm.write(mode, code)
                results[code] = comm.read()
            os.system('clear')
            print_obd_values(results)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Port is missing")
