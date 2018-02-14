"""Send and receiver data from ELM-327 devices"""

import logging
from tempfile import gettempdir
from typing import List

import serial

from filelock import FileLock


class ObdIO(object):
    """Create a obd server"""

    def __init__(self, port):
        self.port = port
        self.ser = None
        self.__lock = FileLock(
            gettempdir() + "/yacm-" + self.port.replace("/", "") + ".lock",
            timeout=1)
        self.__lock.acquire()

    def __enter__(self):
        self.ser = serial.Serial(
            self.port, parity=serial.PARITY_NONE, stopbits=1, bytesize=8)
        self.ser.baudrate = 500000
        # self.__write("at", "ws")  # Reset device
        self.__write("at", "d0")  # Set defaults
        self.__write("at", "l0")  # Disable line feed
        self.__write("at", "e0")  # Disable echo
        self.__write("at", "h0")  # Disable headers
        self.__write("at", "sp0")  # Auto set protocol
        return self.ser

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.__write("at", "ws")  # Reset device
        self.ser.close()
        self.__lock.release()

    def query(self, mode: str, code: str) -> str:
        """Query obd requests"""
        self.__write(mode, code)
        return self.__read()

    def __write(self, mode: str, code: str) -> None:
        self.ser.flushInput()
        self.ser.write(f"{mode}{code}\r".encode())
        logging.info(f"Mode: {mode} Code: {code}")
        self.ser.flush()
        if mode == "at":
            if code == "ws":
                self.ser.readline()
            else:
                self.ser.read_until(b'>')  # Discard the "OK" message

    def __read(self) -> str:
        raw_data = self.ser.read_until(b'\r>')
        while raw_data == 0:
            raw_data = self.ser.read_until(b'\r>')
        logging.info(f"raw_data: {raw_data}")
        if raw_data not in {b'\r?\r>', b'?\r\r'}:
            if raw_data[0] == 13 and raw_data[-3] != 13:  # Emulator
                raw_data = raw_data[1:-2]
            if raw_data[0] != 13 and raw_data[-3] == 13:  # Car
                raw_data = raw_data[:-3]
            if raw_data == b"NO DATA":
                result = "NO DATA"
            else:
                result = raw_data.decode("ascii").lower().split(' ')[2:]
        else:
            result = "?"
        logging.info(f"result: {result}\n")
        return result

    def supported_pids(self) -> List[str]:
        """Return supported pids"""
        hex2bin_map = {
            "0": "0000",
            "1": "0001",
            "2": "0010",
            "3": "0011",
            "4": "0100",
            "5": "0101",
            "6": "0110",
            "7": "0111",
            "8": "1000",
            "9": "1001",
            "a": "1010",
            "b": "1011",
            "c": "1100",
            "d": "1101",
            "e": "1110",
            "f": "1111",
        }
        supported_pids = []
        for pid in ["00", "20", "40", "60", "80"]:
            pids = ''.join(self.query("01", pid))
            if pids not in {"?", "NO DATA"}:
                binary_pids = ''.join(hex2bin_map[nibble] for nibble in pids)
                pid_code = int(pid)
                for bit in binary_pids:
                    pid_code += 1
                    if bit == "1":
                        supported_pids.append(hex(pid_code)[2:])
        return supported_pids
