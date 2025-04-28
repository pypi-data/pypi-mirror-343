# **************************************************************************************

# @package        gnssrtc
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import errno
from datetime import datetime
from time import CLOCK_REALTIME, clock_settime

# **************************************************************************************


def set_system_time(when: datetime) -> None:
    """
    Set the system clock (CLOCK_REALTIME) to `timestamp` (seconds since epoch,
    as a float, so you can pass GPS/NMEA-style times with sub-second precision).

    Raises PermissionError if you're not privileged, or OSError on other failure.
    """
    try:
        clock_settime(CLOCK_REALTIME, when.timestamp())
    except OSError as e:
        # Map EPERM → PermissionError for clarity:
        if e.errno == errno.EPERM:
            raise PermissionError(
                "setting system time requires root/administrator"
            ) from e
        raise


# **************************************************************************************
