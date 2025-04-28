# **************************************************************************************

# @package        gnssrtc
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import logging
from argparse import ArgumentParser
from asyncio import CancelledError, get_running_loop, run, sleep

from gnssrtc import GNSSStratum1NTPServer, GPSUARTDeviceInterface

# **************************************************************************************


async def main(
    port: str = "/dev/serial0",
    baudrate: int = 9600,
) -> None:
    # Retrieve the current running asynchronous event loop:
    loop = get_running_loop()

    # Create a GPS device interface using the specified serial port and baud rate:
    device = GPSUARTDeviceInterface(port=port, baudrate=baudrate)

    # Setup the NTP server with the GPS device:
    with GNSSStratum1NTPServer(device=device) as server:
        # Create a UDP server endpoint on all interfaces at port 123:
        transport, _ = await loop.create_datagram_endpoint(
            lambda: server,
            local_addr=server.address,
        )

        logging.info(
            f"Listening for NTP requests on {server.address[0]}:{server.address[1]}"
        )

        logging.info(f"Using GPS device on {device._port} at {device._baudrate} baud")

        try:
            # Maintain the server indefinitely by sleeping in 3600-second intervals:
            while True:
                await sleep(3600)
        except KeyboardInterrupt:
            # Log that a shutdown has been initiated:
            logging.error("KeyboardInterrupt: Shutting down server...")
        except CancelledError:
            # A CancelledError was raised (likely from the sleep task); log a shutdown message:
            logging.error("CancelledError: Shutting down server...")
        finally:
            # Close the UDP transport:
            transport.close()


# **************************************************************************************

if __name__ == "__main__":
    parser = ArgumentParser(description="Run GNSSRTC GPS")

    # Add an argument for the serial port:
    parser.add_argument(
        "--port",
        type=str,
        default="/dev/serial0",
        help='Serial port to use (default: "/dev/serial0")',
    )

    # Add an argument for the baud rate:
    parser.add_argument(
        "--baudrate",
        type=int,
        default=9600,
        help="Baud rate for the serial connection (default: 9600)",
    )

    # Parse command-line arguments:
    args = parser.parse_args()

    # Run the main function with the provided command-line arguments:
    run(
        main(
            port=args.port,
            baudrate=args.baudrate,
        )
    )


# **************************************************************************************
