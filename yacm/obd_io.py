import serial


class OBD_IO(object):
    """create a server"""

    def __init__(self, port):
        self.port = port

    def __enter__(self):
        self.ser = serial.Serial(
            self.port, parity=serial.PARITY_NONE, stopbits=1, bytesize=8)
        self.ser.baudrate = 38400
        # self.__write("at", "ws")  # Reset device
        self.__write("at", "l0")  # Disable line feed
        self.__write("at", "e0")  # Disable echo
        self.__write("at", "h0")  # Disable headers
        return self.ser

    def __exit__(self, type, value, traceback):
        self.__write("at", "ws")  # Reset device
        self.ser.close()

    def query(self, mode, code):
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
        self.raw_data = self.ser.read_until(b'\r>')
        while len(self.raw_data) == 0:
            self.raw_data = self.ser.read_until(b'\r>')
        # print(self.raw_data)
        if self.raw_data[0] == 13 and self.raw_data[-3] != 13:  # Emulator
            self.raw_data = self.raw_data[1:-2]
        if self.raw_data[0] != 13 and self.raw_data[-3] == 13:  # Car
            self.raw_data = self.raw_data[:-3]
        # print(self.raw_data)
        if self.raw_data != b"NO DATA":
            self.result = self.raw_data.decode("ascii").split(' ')[2:]
        else:
            self.result = "NO DATA"
        # print(self.result)
        return self.result
