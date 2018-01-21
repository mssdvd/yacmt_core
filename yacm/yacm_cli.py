import os
import sys

import obd_converter
import obd_io


def print_obd_values(values):
    for query, result in values.items():
        if query[0] == "01":
            if query[1] == '05':
                print("Engine coolant temperature:")
                print(str(obd_converter.find_converter(query, result)) + ' C')
            elif query[1] == '0c':
                print("Engine rpm:")
                print(str(obd_converter.find_converter(query, result)))
            elif query[1] == '0d':
                print("Speed:")
                # yapf: disable
                print(str(obd_converter.find_converter(query, result)) + ' km/h')
                # yapf: enable
            elif query[1] == '10':
                print("MAF:")
                # yapf: disable
                print(str(obd_converter.find_converter(query, result)) + ' g/s')
                # yapf: enable
            elif query[1] == '11':
                print("Throttle position:")
                print(str(obd_converter.find_converter(query, result)) + ' %')


def main(port):
    obd_codes = [
        "05",  # Engine coolant temperature
        "0c",  # Engine rpm
        "0d",  # Speed
        "10",  # MAF
        "11"  # Throttle position
    ]
    mode = '01'
    comm = obd_io.OBD_IO(port)
    results = {}
    with comm:
        while True:
            results = {(mode, code): comm.query(mode, code)
                       for code in obd_codes}
            os.system('clear')
            print_obd_values(results)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Port is missing")
