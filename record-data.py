"""

RECORD ACCELEROMETER MEASUREMENTS FOR ACCELEROMETER CALIBRATION 
VIA MAGNETO

Code By: Michael Wrona
Created: 17 Aug 2021

This code reads accelerometer measurements in G's over a serial connection 
and logs them to a tab-delimited text file. It also pauses between each 
reading and averages a few measurements.

"""

import os
import math
import argparse
import pandas
import serial


# global variables
MAX_MEAS = 200  # max number of readings in the session, so that we don't create an infinite loop
AVG_MEAS = 25  # for each reading, take this many measurements and average them
SER_PORT = 'COM4'  # serial port the device is connected to
SER_BAUD = 115200  # serial port baud rate
FILENAME = os.path.join(os.getcwd(), 'acceldata.txt')  # output file


class SerialPort:
    """Create and read data from a serial port.

    Attributes:
        read(**kwargs): Read and decode data string from serial port.
    """

    def __init__(self, port, baud=9600):
        """Create and read serial data.

        Args:
            port (str): Serial port name. Example: 'COM4'
            baud (int): Serial baud rate, default 9600.
        """
        if not isinstance(port, str):
            raise TypeError('port must be a string.')

        if not isinstance(baud, int):
            raise TypeError('Baud rate must be an integer.')

        self.port = port
        self.baud = baud

        # Initialize serial connection
        self.ser = serial.Serial(
            self.port, self.baud, timeout=None, xonxoff=False, rtscts=False, dsrdtr=False)
        if hasattr(self.ser, 'reset_input_buffer'):
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
        else:
            self.ser.flushInput()
            self.ser.flushOutput()

    def Read(self, clean_end=True) -> str:
        """
        Read and decode data string from serial port.

        Args:
            clean_end (bool): Strip '\\r' and '\\n' characters from string. Common if used Serial.println() Arduino function. Default true

        Returns:
            (str): utf-8 decoded message.
        """
        bytesToRead = self.ser.readline()
        decodedMsg = bytesToRead.decode('utf-8', errors='replace')

        if clean_end:
            decodedMsg = decodedMsg.rstrip()  # Strip extra chars at the end

        return decodedMsg

    def Close(self) -> None:
        """Close serial connection."""
        self.ser.close()


def RecordDataPt(ser: SerialPort) -> tuple:
    """Record data from serial port and return averaged result."""
    samples = []
    max_retries = 10
    retries = 0

    while len(samples) < AVG_MEAS:
        try:
            line = ser.Read()
            data = line.split(',')
            if len(data) < 3:
                raise ValueError(f"Expected 3 comma-separated values, got: {line}")
            ax_now = float(data[0])
            ay_now = float(data[1])
            az_now = float(data[2])
            samples.append((ax_now, ay_now, az_now))
        except (ValueError, IndexError):
            retries += 1
            if retries > max_retries:
                ser.Close()
                raise SystemExit("[ERROR]: Exceeded maximum retries reading serial connection.")
            continue

    ax = sum(s[0] for s in samples) / AVG_MEAS
    ay = sum(s[1] for s in samples) / AVG_MEAS
    az = sum(s[2] for s in samples) / AVG_MEAS

    # standard deviation
    std_x = math.sqrt(sum((s[0] - ax)**2 for s in samples) / AVG_MEAS)
    std_y = math.sqrt(sum((s[1] - ay)**2 for s in samples) / AVG_MEAS)
    std_z = math.sqrt(sum((s[2] - az)**2 for s in samples) / AVG_MEAS)
    std_total = math.sqrt(std_x**2 + std_y**2 + std_z**2)
    if std_total > 0.05:
        print("[WARNING]: High sensor motion detected during reading (std={:.4f}). Ensure sensor is stationary!".format(std_total))

    return (ax, ay, az)


def List2DelimFile(mylist: list, filename: str, delimiter: str = ',', f_mode='a') -> None:
    """Convert list to Pandas dataframe, then save as a text file."""
    df = pandas.DataFrame(mylist)
    df.to_csv(
        filename,  # path and filename
        sep=delimiter,
        mode=f_mode,
        header=False,  # no col. labels
        index=False  # no row numbers
    )


def main():
    parser = argparse.ArgumentParser(description='Record accelerometer measurements for calibration.')
    parser.add_argument('--port', default=SER_PORT, help='Serial port name (default: %(default)s)')
    parser.add_argument('--baud', type=int, default=SER_BAUD, help='Serial baud rate (default: %(default)s)')
    parser.add_argument('--file', default=FILENAME, help='Output text file path (default: %(default)s)')
    args = parser.parse_args()

    ser = SerialPort(args.port, baud=args.baud)
    data = []  # data list

    print('[INFO]: Place sensor level and stationary on desk.')
    input('[INPUT]: Press any key to continue...')

    # take measurements
    for _ in range(MAX_MEAS):
        user = input(
            '[INPUT]: Ready for measurement? Type \'m\' to measure or \'q\' to save and quit: ').lower().strip()
        if user == 'm':
            # record data to list
            ax, ay, az = RecordDataPt(ser)
            magn = math.sqrt(ax**2 + ay**2 + az**2)
            print('[INFO]: Avgd Readings: {:.4f}, {:.4f}, {:.4f} Magnitude: {:.4f}'.format(
                ax, ay, az, magn))
            data.append([ax, ay, az])
        elif user == 'q':
            # save, then quit
            print('[INFO]: Saving data and exiting...')
            List2DelimFile(data, args.file, delimiter='\t')
            ser.Close()
            print('[INFO]: Done!')
            return
        else:
            print('[WARNING]: \'{}\' is an unknown input. Please enter \'m\' to measure or \'q\' to save and quit.'.format(user))

    # save once max is reached
    print('[WARNING]: Reached max. number of datapoints, saving file...')
    List2DelimFile(data, args.file, delimiter='\t')
    ser.Close()
    print('[INFO]: Done!')


if __name__ == '__main__':
    main()
