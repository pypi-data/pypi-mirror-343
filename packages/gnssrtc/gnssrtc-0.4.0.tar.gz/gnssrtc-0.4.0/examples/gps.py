# **************************************************************************************

# @package        gnssrtc
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import time
from argparse import ArgumentParser

from gnssrtc.gps import GPSUARTDeviceInterface

# **************************************************************************************

if __name__ == "__main__":
    parser = ArgumentParser(description="Run GNSSRTC GPS")

    parser.add_argument(
        "--port",
        type=str,
        default="/dev/serial0",
        help='Serial port to use (default: "/dev/serial0")',
    )

    parser.add_argument(
        "--baudrate",
        type=int,
        default=9600,
        help="Baud rate for the serial connection (default: 9600)",
    )

    args = parser.parse_args()

    gps = GPSUARTDeviceInterface(port=args.port, baudrate=args.baudrate)

    gps.connect()

    print("GPS module over serial 0 UART is ready")

    try:
        while gps.is_ready():
            data = gps.get_nmea_data()

            if data:
                print(data)

            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        gps.disconnect()

# **************************************************************************************
