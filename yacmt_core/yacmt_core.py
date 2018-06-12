import datetime
import json as JSON
import logging
import os
from typing import Dict

import click

from .obd_converter import find_converter, find_converter_name
from .obd_io import ObdIO


def print_obd_values(values: Dict) -> None:
    """Print ECU results"""
    if "eng_load" in values:
        print("Engine load:")
        print(str(values["eng_load"]) + " %")

    if "eng_cool_temp" in values:
        print("Engine coolant temperature:")
        print(str(values["eng_cool_temp"]) + " C")
    if "intake_manifold_abs_press" in values:
        print("Intake manifold absolute pressure:")
        print(str(values["intake_manifold_abs_press"]) + " kPa")
    if "eng_rpm" in values:
        print("Engine rpm:")
        print(str(values["eng_rpm"]) + " RPM")
    if "speed" in values:
        print("Speed:")
        print(str(values["speed"]) + " km/h")
    if "intake_air_temp" in values:
        print("Intake air temperature:")
        print(str(values["intake_air_temp"]) + " C")
    if "mass_air_flow" in values:
        print("MAF:")
        print(str(values["mass_air_flow"]) + " g/s")
    if "throttle_pos" in values:
        print("Throttle position:")
        print(str(values["throttle_pos"]) + " %")
    if "run_time" in values:
        print("Run time:")
        if values["run_time"] == "NO DATA" or values["run_time"] == "?":
            print(values["run_time"])
        else:
            print(str(datetime.timedelta(seconds=values["run_time"])))
    if "fuel_tank_level" in values:
        print("Fuel tank level:")
        print(str(values["fuel_tank_level"]) + " %")
    if "control_mod_voltage" in values:
        print("Control module voltage:")
        print(str(values["control_mod_voltage"]) + " V")
    if "amb_air_temp" in values:
        print("Ambient air temperature:")
        print(str(values["amb_air_temp"]) + " C")
    if "fuel_type" in values:
        print("Fuel type:")
        print(values["fuel_type"])
    if "eng_oil_temp" in values:
        print("Engine oil temperature:")
        print(values["eng_oil_temp"] + " C")


@click.command()
@click.argument('port')
@click.option('--log', default='WARNING', help='Log level')
@click.option('--supported-pids', is_flag=True, help='Show supported pids')
@click.option('--json', is_flag=True, help='Generate JSON')
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
    try:
        with ObdIO(port) as comm:
            if supported_pids:
                print("Supported pids:")
                print(JSON.dumps(comm.supported_pids()))
            else:
                while True:
                    results = {
                        find_converter_name((mode, code)): find_converter(
                            (mode, code), comm.query(mode, code))
                        for code in obd_codes
                    }
                    if json:
                        import tempfile
                        print(JSON.dumps(results))
                        with open(tempfile.gettempdir() + "/yacmt.json",
                                  "w") as f:
                            f.write(JSON.dumps(results))
                    else:
                        os.system('clear')
                        print_obd_values(results)
    except KeyboardInterrupt:
        print("\nExit")


if __name__ == '__main__':
    main()
