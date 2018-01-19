import serial


class OBD_IO(object):
    """create a server"""

    def __init__(self, port):
        self.port = port

    def __enter__(self):
        self.ser = serial.Serial(
            self.port, parity=serial.PARITY_NONE, stopbits=1, bytesize=8)
        self.ser.baudrate = 38400
        self.ser.timeout = 0.1
        return self.ser

    def __exit__(self, type, value, traceback):
        self.ser.close()

    def write(self, mode, code):
        self.ser.write(f'{mode} {code}\r'.encode())

    def read(self):
        self.result = self.ser.readlines()[1].decode("ascii").split(' ')[2:]
        self.result[-1] = self.result[-1].rstrip('\r\n')
        return self.result
