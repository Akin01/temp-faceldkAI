import serial


class Arduino:
    def __init__(self, port, bauderate):
        self.port = port
        self.bauderate = bauderate

    def open_serial(self):
        arduino = serial.Serial(self.port, self.bauderate)
        return arduino

    def get_temp(self, sep: str = None, ser=None) -> tuple or float:
        arduino_data = ser.readline()

        if sep:
            temp = str(arduino_data[:len(arduino_data)].decode("utf-8")).split(sep)
            return tuple(map(float, temp))

        temp = str(arduino_data[:len(arduino_data) - 1].decode("utf-8"))
        return float(temp)

    def close_serial(self, ser):
        ser.close()
