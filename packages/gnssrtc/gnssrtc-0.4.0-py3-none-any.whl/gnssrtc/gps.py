# **************************************************************************************

# @package        gnssrtc
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from datetime import datetime, timezone
from enum import Enum
from time import time_ns
from typing import Optional, Tuple

from serial import Serial

from .nmea import GPCGGNMEASentence, parse_gpcgg_nmea_sentence

# **************************************************************************************


class BaseDeviceState(Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DISCONNECTING = "disconnecting"
    ERROR = "error"


# **************************************************************************************

# Enables GPS, BeiDou, Galileo, and QZSS signals:
ENABLE_GPS_BD_Galileo_QZSS_CMD: bytes = (
    b"\x06\x3e\x3c\x00\x00\x20\x20\x07\x00\x08\x10\x00\x01\x00\x01"
    b"\x01\x01\x01\x03\x00\x00\x00\x01\x01\x02\x04\x08\x00\x00\x00"
    b"\x01\x01\x03\x08\x10\x00\x01\x00\x01\x01\x04\x00\x08\x00\x00"
    b"\x00\x01\x03\x05\x00\x03\x00\x01\x00\x01\x05\x06\x08\x0e\x00"
    b"\x00\x00\x01\x01"
)

# Enables NMEA version 4.10 output for BeiDou sentences:
ENABLE_NMEA_BD_SENTENCES_CMD: bytes = (
    b"\xb5\x62\x06\x17\x14\x00\x00\x41\x00\x02\x00\x00\x00\x00\x00"
    b"\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00"
)

# UBX protocol header that must be prefixed to every command:
ubx_header: bytes = b"\xb5\x62"

# **************************************************************************************


def compute_checksum(command: bytes) -> Tuple[int, int]:
    """
    Compute the two 8-bit checksum values for a UBX protocol command.

    The checksum is calculated over the message class, message ID, length, and payload.

    Args:
        command (bytes): The raw command bytes (excluding the UBX header).

    Returns:
        Tuple[int, int]: A tuple containing (checksum_a, checksum_b).
    """
    cxa = 0
    cxb = 0

    for byte in command:
        cxa = (cxa + byte) & 0xFF
        cxb = (cxb + cxa) & 0xFF

    return cxa, cxb


# **************************************************************************************


def build_ubx_command(raw_command: bytes) -> bytes:
    """
    Build a full UBX command by calculating its checksum and appending it
    to the raw command, then prefixing the UBX header.

    Args:
        raw_command (bytes): The raw command content without header or checksum.

    Returns:
        bytes: The complete UBX command.
    """
    cxa, cxb = compute_checksum(raw_command)
    # Prepend the UBX header and return the full command bytes:
    return ubx_header + raw_command + bytes([cxa, cxb])


# **************************************************************************************


class GPSUARTDeviceInterface(object):
    # The default UART port for the GPS module:
    _port = "/dev/serial0"

    # The UART Serial interface object for the GPS module:
    _uart: Serial

    # The default baudrate for the GPS module, in bits per second:
    _baudrate: int = 115200

    _last_fix: Optional[GPCGGNMEASentence] = None

    # The current state of the device:
    state: BaseDeviceState = BaseDeviceState.DISCONNECTED

    def __init__(
        self,
        port: Optional[str] = None,
        baudrate: Optional[int] = None,
        timeout: float = 1.0,
    ) -> None:
        super().__init__()

        # If the port is provided, update the default port:
        self._port = port or self._port

        # If the baudrate is provided, update the default baudrate:
        self._baudrate = baudrate or self._baudrate

        # The timeout for reading data from the GPS module, in seconds:
        self._timeout = timeout

        # Initialize the UART Serial interface object for the GPS module:
        self.initialise()

    def initialise(self) -> None:
        """
        Initialise the device.

        This method should handle any necessary setup required before the device can be used.
        """
        # Initialize the UART Serial interface object for the GPS module:
        try:
            self._uart = Serial(
                self._port, baudrate=self._baudrate, timeout=self._timeout
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to open serial port {self._port} at {self._baudrate} baud: {e}"
            )

        # Flush the input buffer to remove any stale data:
        self._uart.reset_input_buffer()

        # Open the UART Serial interface object for the GPS module if it is not already open:
        if not self._uart.is_open:
            self._uart.open()

        # Build the UBX commands to enable GPS, BeiDou, Galileo, and QZSS signals:
        ubx_command1: bytes = build_ubx_command(ENABLE_GPS_BD_Galileo_QZSS_CMD)

        # Build the UBX command to enable NMEA version 4.10 output for BeiDou sentences:
        ubx_command2: bytes = build_ubx_command(ENABLE_NMEA_BD_SENTENCES_CMD)

        # Send the UBX command to enable GPS, BeiDou, Galileo, and QZSS signals:
        self._uart.write(ubx_command1)

        # Send the UBX command to enable NMEA version 4.10 output for BeiDou sentences:
        self._uart.write(ubx_command2)

    def reset(self) -> None:
        """
        Reset the device.

        This method should restore the device to its default or initial state.
        """
        # Attempt to reset the GPS device:
        self.disconnect()

        # Attempt to re-initialise the GPS device:
        self.connect()

    def connect(self) -> None:
        """
        Establish a connection to the device.

        This method should implement the operations required to connect to the device.
        """
        if self.state not in [BaseDeviceState.DISCONNECTED, BaseDeviceState.ERROR]:
            return

        # Update the device state to connecting:
        self.state = BaseDeviceState.CONNECTING

        try:
            # Attempt to initialise the device:
            self.initialise()
        except Exception as e:
            self.state = BaseDeviceState.ERROR
            raise e

        # Update the device state to connected:
        self.state = BaseDeviceState.CONNECTED

    def disconnect(self) -> None:
        """
        Disconnect from the device.

        This method should handle any cleanup or shutdown procedures necessary to safely
        disconnect from the device.
        """
        if self.state == BaseDeviceState.DISCONNECTED:
            return

        # Update state to disconnecting to prevent reconnection:
        self.state = BaseDeviceState.DISCONNECTING

        # Close the UART Serial interface object for the GPS module:
        self._uart.close()

        # Update the device state to disconnected:
        self.state = BaseDeviceState.DISCONNECTED

    def is_connected(self) -> bool:
        """
        Check if the device is connected.

        Returns:
            bool: True if the device is connected; otherwise, False.
        """
        return self.state == BaseDeviceState.CONNECTED

    def is_ready(self) -> bool:
        """
        Check if the device is ready for operation.

        Returns:
            bool: True if the device is ready; otherwise, False.
        """
        return (
            self.is_connected()
            and not self._uart.closed
            and self._uart.readable()
            and self._uart.writable()
        )

    def get_firmware_version(self) -> Tuple[int, int, int]:
        """
        Get the version of the device firmware as a tuple (major, minor, patch).

        Returns:
            Tuple[int, int, int]: The firmware version. Defaults to (0, 0, 0).
        """
        return 0, 0, 0

    def get_raw_line(self) -> str:
        """
        Get a raw line of data from the GPS device
        """
        return self._uart.readline().decode("ascii", errors="ignore").strip()

    def get_nmea_data(self) -> Optional[GPCGGNMEASentence]:
        """
        Get the NMEA message data from the GPS and return the parsed GPGGA or GNGGA NMEA sentence
        """
        line = self.get_raw_line()

        # If the line is not a GPGGA or GNGGA NMEA sentence, return None:
        if not line.startswith("$GPGGA") and not line.startswith("$GNGGA"):
            return None

        # Return the parsed GPGGA or GNGGA NMEA sentence:
        nmea = parse_gpcgg_nmea_sentence(line)

        # Update the last fix with the new fix:
        if nmea:
            self._last_fix = nmea

        # Return the parsed GPGGA or GNGGA NMEA sentence:
        return nmea

    def get_last_fix(self) -> Optional[GPCGGNMEASentence]:
        """
        Get the last fix from the GPS device as a GPGGA or GNGGA NMEA sentence
        """
        return self._last_fix

    def get_latitude(self, timeout: float = 10.0) -> float:
        """
        Get the latitude from the GPS device

        Args:
            timeout (float): The maximum time to wait for a valid NMEA sentence in seconds. Default is 10 seconds.

        Returns:
            float: The latitude in degrees.
        """
        start = time_ns()

        timeout_ns = int(timeout * 1e9)

        while True:
            data = self.get_nmea_data()
            if data:
                break

            if (time_ns() - start) >= timeout_ns:
                raise TimeoutError("Timed out waiting for valid NMEA sentence")

        # Return the latitude from the NMEA data:
        return data.get("latitude", 0.0)

    def get_longitude(self, timeout: float = 10.0) -> float:
        """
        Get the longitude from the GPS device

        Args:
            timeout (float): The maximum time to wait for a valid NMEA sentence in seconds. Default is 10 seconds.

        Returns:
            float: The longitude in degrees.
        """
        start = time_ns()

        timeout_ns = int(timeout * 1e9)

        while True:
            data = self.get_nmea_data()
            if data:
                break

            if (time_ns() - start) >= timeout_ns:
                raise TimeoutError("Timed out waiting for valid NMEA sentence")

        # Return the longitude from the NMEA data:
        return data.get("longitude", 0.0)

    def get_altitude(self, timeout: float = 10.0) -> float:
        """
        Get the altitude from the GPS device

        Args:
            timeout (float): The maximum time to wait for a valid NMEA sentence in seconds. Default is 10 seconds.

        Returns:
            float: The altitude in meters.
        """
        start = time_ns()

        timeout_ns = int(timeout * 1e9)

        while True:
            data = self.get_nmea_data()
            if data:
                break

            if (time_ns() - start) >= timeout_ns:
                raise TimeoutError("Timed out waiting for valid NMEA sentence")

        return data.get("altitude", 0.0)

    def get_time(self, timeout: float = 5.0) -> datetime:
        """
        Get the current time from the GPS device

        Args:
            timeout (float): The maximum time to wait for valid data, in seconds. Defaults to 5.0.

        Returns:
            datetime: The UTC time from the GPS device, or the current UTC time if timeout is reached.
        """
        start = time_ns()

        timeout_ns = int(timeout * 1e9)

        while True:
            data = self.get_nmea_data()
            if data:
                break

            if (time_ns() - start) >= timeout_ns:
                raise TimeoutError("Timed out waiting for valid NMEA sentence")

        return data.get("utc", datetime.now(timezone.utc))


# **************************************************************************************
