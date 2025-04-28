# **************************************************************************************

# @package        gnssrtc
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from datetime import datetime, timezone
from re import compile
from typing import TypedDict

# **************************************************************************************


class GPZDANMEASentence(TypedDict):
    # Message ID $GPZDA or $GNZDA:
    id: str

    # UTC datetime extracted from the ZDA message:
    utc: datetime

    # Local time zone offset in hours:
    local_zone_offset_hours: int

    # Local time zone offset in minutes:
    local_zone_offset_minutes: int

    # The checksum of the message (starts with "*"):
    checksum: str


# **************************************************************************************

GPZDA_NMEA_MESSAGE_REGEX = compile(
    r"^\$(GPZDA|GNZDA),"
    r"(\d{6}\.\d{1,2}),"
    r"(\d{2}),"
    r"(\d{2}),"
    r"(\d{4}),"
    r"([-+]?\d{1,2}),"
    r"(\d{2})"
    r"\*([0-9A-Fa-f]{2})$"
)

# **************************************************************************************


def parse_gpzda_nmea_sentence(value: str) -> GPZDANMEASentence:
    """Parses a ZDA message and returns structured data."""
    # Validate that the ZDA sentence starts with a '$' character.
    if not value.startswith("$"):
        raise ValueError("Invalid NMEA sentence: must start with '$'")

    # Match the ZDA sentence against the regex.
    match = GPZDA_NMEA_MESSAGE_REGEX.match(value)

    # Ensure the regex matched the sentence.
    if not match:
        raise ValueError("Invalid ZDA sentence: regex did not match")

    # Extract the message header ID from the matched groups:
    id = match.group(1)

    # Extract the checksum from the matched groups, and prepend the '*' character:
    checksum = "*" + match.group(8)

    # UTC datetime of position fix; using a default date of 1900-01-01:
    utc_time = match.group(2)

    # Extract the local time zone offset hours:
    local_zone_offset_hours = match.group(6)

    # Extract the local time zone offset minutes:
    local_zone_offset_minutes = match.group(7)

    when = datetime.strptime(utc_time, "%H%M%S.%f")

    # Combine the current date with the parsed time to create a complete UTC datetime:
    utc = datetime(
        int(match.group(5)),
        int(match.group(4)),
        int(match.group(3)),
        when.hour,
        when.minute,
        when.second,
        when.microsecond,
        timezone.utc,
    )

    # Return the parsed ZDA sentence as a GPZDANMEASentence:
    return GPZDANMEASentence(
        id=f"${id}",
        utc=utc,
        local_zone_offset_hours=int(local_zone_offset_hours),
        local_zone_offset_minutes=int(local_zone_offset_minutes),
        checksum=checksum,
    )


# **************************************************************************************
