# **************************************************************************************

# @package        gnssrtc
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import asyncio
import logging
from collections import deque
from datetime import datetime
from time import gmtime
from types import TracebackType
from typing import Deque, Optional, Tuple, Type

from ntps import NTPServer
from rich.console import Console, Group
from rich.panel import Panel

from .epoch import NTP_UNIX_DELTA
from .gps import GPSUARTDeviceInterface
from .system import set_system_time

# **************************************************************************************


class InMemoryLoggingHandler(logging.Handler):
    """Keep the last `capacity` log records in memory."""

    def __init__(self, capacity: int = 200) -> None:
        super().__init__()

        # Set the maximum number of records to keep in memory:
        self.records: Deque[str] = deque(maxlen=capacity)

        # Set up the logging formatter:
        fmt = logging.Formatter(
            "%(asctime)sZ %(levelname)s: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S"
        )

        # Force the timestamp to use UTC instead of localtime:
        fmt.converter = gmtime

        # Set the formatter for this handler:
        self.setFormatter(fmt)

    def emit(self, record: logging.LogRecord) -> None:
        # Format the log record and append it to the records deque:
        self.records.append(self.format(record))


# **************************************************************************************


class GNSSStratum1NTPServer(NTPServer):
    # Set the reference identifier of the NTP server:
    refid = "GPS"

    # Set the stratum level of the NTP server:
    stratum = 1

    # Define the GPS UART serial device interface:
    device: GPSUARTDeviceInterface

    # Store the last synchronisation time from the GPS device:
    _last_sync_time: datetime = datetime.now()

    def __init__(
        self,
        device: GPSUARTDeviceInterface,
        *,
        poll_interval: float = 1.0,
    ) -> None:
        super().__init__()
        # Initialize the GPS device interface:
        self.device = device
        # Set the poll interval for the GPS device:
        self._poll_interval = poll_interval

        # Set up Rich console for displaying panels:
        self.console = Console()

        # Set up in-memory logging handler:
        self._log_handler = InMemoryLoggingHandler(capacity=200)

        root = logging.getLogger()

        root.setLevel(logging.INFO)

        root.addHandler(self._log_handler)

    def _render_logging_panels(self) -> Group:
        # Create a header for the server info panel:
        header = (
            f"Stratum {self.stratum} NTP Server "
            f"(using {self.refid} system time) running on UDP port 123"
        )
        # Create a panel with the header and the last synchronised time:
        return Group(
            Panel(header, title="Server Info", padding=(1, 2)),
            Panel(
                self._last_sync_time.isoformat(sep=" ", timespec="milliseconds"),
                title="Synchronised System Time",
                padding=(1, 2),
            ),
            Panel("\n".join(self._log_handler.records), title="Logs", padding=(1, 2)),
        )

    def __enter__(self) -> "GNSSStratum1NTPServer":
        # Clear the console:
        self.console.clear()
        # Draw the panels:
        self.console.print(self._render_logging_panels())
        # Start the GPS fix task in the background:
        loop = asyncio.get_event_loop()
        # Create a task to poll the GPS device and set the system time:
        self._task = loop.create_task(self._gps_fix())
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        # Stop the GPS fix task:
        self._task.cancel()
        # Clear the console:
        self.console.clear()
        # Draw the panels:
        self.console.print(self._render_logging_panels())

    async def _gps_fix(self) -> None:
        """
        Background thread: poll GPS device, set the system clock,
        then sleep until next poll or until stopped.
        """
        while True:
            try:
                # Poll the GPS device for the current time:
                now = self.device.get_time(timeout=self._poll_interval)

                # Set the system time to the current time from the GPS device:
                set_system_time(when=now)

                # Set the last synchronised time to the current time from the GPS device:
                self._last_sync_time = now

            except TimeoutError:
                # No fix this interval → retry polling:
                logging.warning("GPS timeout, retrying...")
                continue

            except PermissionError:
                # Insufficient privileges → stop polling:
                logging.error("Permission denied setting system time; stopping.")
                break

            except OSError as e:
                # Other OS error → ignore and continue:
                logging.error(f"OS error: {e}")
                continue

            # Clear the console:
            self.console.clear()
            # Draw the panels:
            self.console.print(self._render_logging_panels())

            # Sleep for the specified poll interval:
            await asyncio.sleep(self._poll_interval)

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        # Log every incoming NTP request with the address:
        logging.info(
            f"Sent NTP response to {addr[0]}:{addr[1]} using system time (GPS-synced)."
        )
        # Then delegate to the parent NTPServer implementation to handle the request:
        super().datagram_received(data, addr)

    def get_ntp_time(self) -> float:
        now: datetime = datetime.now()

        # Add epoch delta to get NTP seconds since 1900 from POSIX timestamp.
        # N.B. NTP epoch is 1900-01-01, while Unix epoch is 1970-01-01:
        return now.timestamp() + NTP_UNIX_DELTA


# **************************************************************************************
