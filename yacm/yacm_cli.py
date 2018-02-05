import logging
import os
import sys

import click

from yacm import obd_converter, obd_io


def ss2hhmmss(secs):
    """Converter secods to hours:minutes:seconds"""
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return f"{hours}:{mins}:{secs}"


def print_obd_values(values):
    """Print ECU results"""
    for query, result in values.items():
        if query[0] == "01":
            if query[1] == '4':
                print("Engine load:")
                print(str(obd_converter.find_converter(query, result)) + ' %')
            elif query[1] == '5':
                print("Engine coolant temperature:")
                print(str(obd_converter.find_converter(query, result)) + ' C')
            elif query[1] == 'a':
                print("Intake manifold absolute pressure:")
                # yapf: disable
                print(str(obd_converter.find_converter(query, result)) + ' kPa')
                # yapf: enable
            elif query[1] == 'c':
                print("Engine rpm:")
                print(str(obd_converter.find_converter(query, result)))
            elif query[1] == 'd':
                print("Speed:")
                # yapf: disable
                print(str(obd_converter.find_converter(query, result)) + ' km/h')
                # yapf: enable
            elif query[1] == 'f':
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
                    print(ss2hhmmss(obd_converter.find_converter(query, result)))
                    # yapf: enable
            elif query[1] == '2f':
                print("Fuel tank level:")
                print(str(obd_converter.find_converter(query, result)) + ' %')
            elif query[1] == '42':
                print("Control module voltage:")
                print(str(obd_converter.find_converter(query, result)) + ' V')
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
    """Main"""
    obd_codes = [
        "4",  # Engine load
        "5",  # Engine coolant temperature
        "a",  # Intake manifold absolute pressure
        "c",  # Engine rpm
        "d",  # Speed
        "f",  # Intake air temperature
        "10",  # MAF
        "11",  # Throttle position
        "1f",  # Run time
        # "2f",  # Fuel tank level
        "42"  # Control module voltage
        # "46",  # Ambient air temperature
        # "51",  # Fuel type
        # "5c"  # Engine oil temperature
    ]
    mode = '01'
    comm = obd_io.ObdIO(port)
    with comm:
        try:
            print("Supported pids:")
            print(comm.supported_pids())
            while True:
                results = {(mode, code): comm.query(mode, code)
                           for code in obd_codes}
                os.system('clear')
                print_obd_values(results)
        except KeyboardInterrupt:
            print("\nExit")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Port is missing")
