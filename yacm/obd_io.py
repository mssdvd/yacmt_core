"""Send and receiver data from ELM-327 devices"""

import serial


class ObdIO(object):
    """Create a obd server"""

    def __init__(self, port):
        self.port = port
        self.ser = None

    def __enter__(self):
        self.ser = serial.Serial(
            self.port, parity=serial.PARITY_NONE, stopbits=1, bytesize=8)
        self.ser.baudrate = 38400
        # self.__write("at", "ws")  # Reset device
        self.__write("at", "d0")  # Set defaults
        self.__write("at", "l0")  # Disable line feed
        self.__write("at", "e0")  # Disable echo
        self.__write("at", "h0")  # Disable headers
        self.__write("at", "sp 0")
        return self.ser

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.__write("at", "ws")  # Reset device
        self.ser.close()

    def query(self, mode, code):
        """Query obd requests"""
        self.__write(mode, code)
        return self.__read()

    def __write(self, mode, code):
        self.ser.flushInput()
        self.ser.write(f"{mode} {code}\r\n".encode())
        self.ser.flush()
        if mode == "at" and code != "ws":
            self.ser.read_until(b'>')  # Discard the "OK" message
        if mode == "at" and code == "ws":
            self.ser.readline()

    def __read(self):
        raw_data = self.ser.read_until(b'\r>')
        while raw_data == 0:
            raw_data = self.ser.read_until(b'\r>')
        # print(raw_data)
        if raw_data == b'\r?\r>' or raw_data == b'?\r\r':
            result = "?"
        else:
            if raw_data[0] == 13 and raw_data[-3] != 13:  # Emulator
                raw_data = raw_data[1:-2]
            if raw_data[0] != 13 and raw_data[-3] == 13:  # Car
                raw_data = raw_data[:-3]
            # print(raw_data)
            if raw_data != b"NO DATA":
                result = raw_data.decode("ascii").split(' ')[2:]
            else:
                result = "NO DATA"
        # print(result)
        return result

    def pids_supported(self):
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
            "A": "1010",
            "B": "1011",
            "C": "1100",
            "D": "1101",
            "E": "1110",
            "F": "1111",
        }
        pids_supported = []
        for pid in [00, 20, 40, 60, 80]:
            pids = ''.join(self.query("01", pid))
            if pids != "?":
                binary_pids = ''.join(hex2bin_map[nibble] for nibble in pids)
                pid_code = pid
                for bit in binary_pids:
                    pid_code += 1
                    if bit == "1":
                        pids_supported.append(hex(pid_code)[2:])
        return pids_supported
