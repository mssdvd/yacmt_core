import os
import sys

from . import obd_converter
from . import obd_io


def to_hhmmss(secs):
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return f"{hours}:{mins}:{secs}"


def print_obd_values(values):
    for query, result in values.items():
        if query[0] == "01":
            if query[1] == '04':
                print("Engine load:")
                print(str(obd_converter.find_converter(query, result)) + ' %')
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
            elif query[1] == '0f':
                print("Intake air temperature:")
                print(str(obd_converter.find_converter(query, result)) + ' C')
            elif query[1] == '10':
                print("MAF:")
                # yapf: disable
                print(str(obd_converter.find_converter(query, result)) + ' g/s')
                # yapf: enable
            elif query[1] == '11':
                print("Throttle position:")
                print(str(obd_converter.find_converter(query, result)) + ' %')
            elif query[1] == '1f':
                print("Run time:")
                if result == "NO DATA" or result == "?":
                    print(obd_converter.find_converter(query, result))
                else:
                    # yapf: disable
                    print(to_hhmmss(obd_converter.find_converter(query, result)))
                    # yapf: enable
            elif query[1] == '2f':
                print("Fuel tank level:")
                print(str(obd_converter.find_converter(query, result)) + ' %')
            elif query[1] == '46':
                print("Ambient air temperature:")
                print(str(obd_converter.find_converter(query, result)) + ' C')
            elif query[1] == '51':
                print("Fuel type:")
                print(obd_converter.find_converter(query, result))
            elif query[1] == '5c':
                print("Engine oil temperature:")
                print(obd_converter.find_converter(query, result))


def main(port):
    obd_codes = [
        "04",  # Engine load
        "05",  # Engine coolant temperature
        "0c",  # Engine rpm
        "0d",  # Speed
        "0f",  # Intake air temperature
        "10",  # MAF
        "11",  # Throttle position
        "1f",  # Run time
        "2f",  # Fuel tank level
        "46",  # Ambient air temperature
        "51",  # Fuel type
        "5c"  # Engine oil temperature
    ]
    mode = '01'
    comm = obd_io.ObdIO(port)
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
