import json as JSON
import logging
import os
from typing import Dict

import click

from yacm import obd_converter, obd_io


def json_generator(values: Dict) -> str:
    return JSON.dumps({
        obd_converter.find_converter_name(query): obd_converter.find_converter(
            query, result)
        for query, result in values.items()
    })


def ss2hhmmss(secs: int) -> str:
    """Converter secods to hours:minutes:seconds"""
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return f"{hours}:{mins}:{secs}"


def print_obd_values(values: Dict) -> None:
    """Print ECU results"""
    for query, result in values.items():
        if query[0] == "01":
            if query[1] == '04':
                print("Engine load:")
                print(str(obd_converter.find_converter(query, result)) + ' %')
            elif query[1] == '05':
                print("Engine coolant temperature:")
                print(str(obd_converter.find_converter(query, result)) + ' C')
            elif query[1] == '0a':
                print("Intake manifold absolute pressure:")
                # yapf: disable
                print(str(obd_converter.find_converter(query, result)) + ' kPa')
                # yapf: enable
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


@click.command()
@click.argument('port')
@click.option('--log', default='WARNING', help='Log level')
@click.option('--supported-pids', is_flag=True, help='Show supported pids')
@click.option('--json', is_flag=True, help='Print Json')
def main(port, log, supported_pids, json):
    """Read and print information from the ECU"""
    logging.basicConfig(level=getattr(logging, log.upper()))
    obd_codes = [
        "04",  # Engine load
        "05",  # Engine coolant temperature
        "0a",  # Intake manifold absolute pressure
        "0c",  # Engine rpm
        "0d",  # Speed
        "0f",  # Intake air temperature
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
    try:
        with comm:
            if supported_pids:
                print("Supported pids:")
                print(comm.supported_pids())
            else:
                while True:
                    results = {(mode, code): comm.query(mode, code)
                               for code in obd_codes}
                    if json:
                        print(json_generator(results))
                        break
                    else:
                        os.system('clear')
                        print_obd_values(results)
    except KeyboardInterrupt:
        print("\nExit")


if __name__ == '__main__':
    main()
