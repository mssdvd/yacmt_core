import obd_converter
import serial

# ser serial.Serial('/dev/pts/x', 38400, timeout=1)
# ser.write(b'01 0D\r')
# ser.readlines()


def com(pts_num):
    with serial.Serial('/dev/pts/' + str(pts_num)) as ser:
        ser.baudrate = 38400
        ser.timeout = 0.2
        while True:
            print('>', end=' ')
            command = input().lower()
            ser.write(f'01 {command}\r'.encode())
            result = ser.readlines()[1].decode("utf-8").split(' ')[2:]
            result[-1] = result[-1].rstrip('\r\n')
            if command == '05':
                print(obd_converter.eng_cool_temp(result))
            elif command == '0c':
                print(obd_converter.eng_rpm(result))
            elif command == '0d':
                print(obd_converter.speed(result))
            elif command == '10':
                print(obd_converter.mass_air_flow(result))
            elif command == '11':
                print(obd_converter.throttle_pos(result))


if __name__ == '__main__':
    com(8)
