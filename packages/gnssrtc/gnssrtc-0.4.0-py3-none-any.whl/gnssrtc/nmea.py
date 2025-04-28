# **************************************************************************************

# @package        gnssrtc
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

from datetime import datetime, timezone
from math import inf
from re import compile
from typing import Literal, Optional, TypedDict, cast

# **************************************************************************************


class GPCGGNMEASentence(TypedDict):
    # Message ID $GPGGA:
    id: str

    # UTC datetime of position fix:
    utc: datetime

    # Latitude (in decimal degrees):
    latitude: float

    # Longitude (in decimal degrees):
    longitude: float

    # Orthometric height using MSL reference (in meters):
    altitude: float

    # GPS quality indicator, e.g.,:
    # 0: Fix not valid
    # 1: GPS fix
    # 2: Differential GPS fix (DGNSS), SBAS, OmniSTAR VBS, Beacon, RTX in GVBS mode
    # 3: Not applicable
    # 4: RTK Fixed, xFill
    # 5: RTK Float, OmniSTAR XP/HP, Location RTK, RTX
    # 6: INS Dead reckoning
    # 7: Manual input mode (fixed position)
    # 8: Simulator mode
    # 9: WAAS (SBAS)
    quality_indicator: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Number of SVs in use, range from 00 through to 24+:
    number_of_satellites: int

    # Horizontal dilution of precision:
    hdop: float

    # Geoid separation (in meters):
    geoid_separation: float

    # Age of differential GPS data record, Type 1 or Type 9:
    dgps_age: Optional[float]

    # The reference station ID, range 0000 to 4095:
    reference_station_id: Optional[str]

    # The checksum of the message (starts with "*"):
    checksum: str


# **************************************************************************************

GPCGG_NMEA_MESSAGE_REGEX = compile(
    # Group 1: Message ID ($GPGGA or $GNGGA for multi-GNSS)
    r"^\$(GPGGA|GNGGA),"
    # Group 2: UTC time (hhmmss.ss) with 1 or 2 decimals
    r"((?:\d{6}\.\d{1,2})?),"
    # Group 3: Latitude value, Group 4: Latitude direction
    r"((?:\d{4,}\.\d+)?),([NS]?),"
    # Group 5: Longitude value, Group 6: Longitude direction
    r"((?:\d{5,}\.\d+)?),([EW]?),"
    # Group 7: GPS quality indicator (0-9)
    r"(\d?),"
    # Group 8: Number of satellites in use
    r"(\d{1,2})?,"
    # Group 9: Horizontal dilution of precision (HDOP)
    r"([\d\.]+)?,"
    # Group 10: Altitude in meters (with optional sign)
    r"(-?[\d\.]+)?,(?:M)?,"
    # Group 11: Geoid separation in meters (with optional sign)
    r"(-?[\d\.]+)?,(?:M)?,"
    # Group 12: Differential GPS age (optional)
    r"([\d\.]+)?,"
    # Group 13: Reference station ID (optional)
    r"([A-Za-z0-9]+)?"
    # Group 14: Checksum (two hex digits)
    r"\*([0-9A-Fa-f]{2})$",
    flags=0,
)

# **************************************************************************************


def parse_gpcgg_nmea_coordinate(
    value: str, direction: Literal["N", "S", "E", "W"]
) -> float:
    if not value:
        return inf

    degrees = int(float(value) // 100)
    minutes = float(value) - (degrees * 100)

    ddegrees = degrees + (minutes / 60.0)

    if direction in ("S", "W"):
        ddegrees = -ddegrees

    return ddegrees


# **************************************************************************************


def parse_gpcgg_nmea_sentence(value: str) -> GPCGGNMEASentence:
    # Ensure that our string value starts with a $ sign:
    if not value.startswith("$"):
        raise ValueError("Invalid NMEA sentence: must start with '$'")

    # Use the regex to match and extract the message parts:
    match = GPCGG_NMEA_MESSAGE_REGEX.match(value)

    # If we can not verify a match, then the NMEA sentence by definition is invalid:
    if not match:
        raise ValueError("Invalid GPGGA sentence: regex did not match")

    # Extract the message header ID from the matched groups:
    id = match.group(1)

    # Extract the checksum from the matched groups, and prepend the '*' character:
    checksum = "*" + match.group(14)

    now = datetime.now(timezone.utc)

    # UTC datetime of position fix; using a default date of 1900-01-01:
    utc_time = (
        match.group(2)
        if match.group(2) != ""
        else now.strftime("%H%M%S.") + f"{now.microsecond // 10000:02d}"
    )

    latitude_value = match.group(3) if match.group(3) is not None else "0"

    # Extract the latitude direction (should be "N" or "S"):
    latitude_direction: Literal["N", "S"] = (
        cast(Literal["N", "S"], match.group(4)) if match.group(4) is not None else "N"
    )

    # Convert the latitude value to decimal degrees:
    latitude = parse_gpcgg_nmea_coordinate(latitude_value, latitude_direction)

    # Extract the longitude value:
    longitude_value = match.group(5) if match.group(5) is not None else "0"

    # Extract the longitude direction (should be "E" or "W"):
    longitude_direction: Literal["E", "W"] = (
        cast(Literal["E", "W"], match.group(6)) if match.group(6) is not None else "E"
    )

    # Convert the longitude value to decimal degrees:
    longitude = parse_gpcgg_nmea_coordinate(longitude_value, longitude_direction)

    # Extract the GPS quality indicator:
    quality_indicator = int(match.group(7))

    # Ensure that it is one of the prescribed values:
    if quality_indicator not in {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}:
        raise ValueError("Quality indicator must be between 0 and 9")

    # Extract the number of satellites in use:
    number_of_satellites = int(match.group(8))

    # Extract the horizontal dilution of precision (HDOP):
    hdop = float(match.group(9))

    # Extract the altitude value in meters:
    altitude = float(match.group(10)) if match.group(10) else inf

    # Extract the geoid separation in meters:
    geoid_separation = float(match.group(11)) if match.group(11) else inf

    # Extract the differential GPS age if provided; otherwise, set to None:
    dgps_age = float(match.group(12)) if match.group(12) else None

    # Extract the reference station ID if provided; otherwise, set to None:
    reference_station_id = match.group(13) if match.group(13) else None

    when = datetime.strptime(utc_time, "%H%M%S.%f")

    # Get the current UTC date:
    now = datetime.now(timezone.utc)

    # Combine the current date with the parsed time to create a complete UTC datetime:
    utc = datetime(
        now.year,
        now.month,
        now.day,
        when.hour,
        when.minute,
        when.second,
        when.microsecond,
        timezone.utc,
    )

    # Return the parsed NMEA sentence as a GPCGGNMEASentence.
    return GPCGGNMEASentence(
        id=f"${id}",
        utc=utc,
        latitude=latitude,
        longitude=longitude,
        altitude=altitude,
        quality_indicator=cast(
            Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], quality_indicator
        ),
        number_of_satellites=number_of_satellites,
        hdop=hdop,
        geoid_separation=geoid_separation,
        dgps_age=dgps_age,
        reference_station_id=reference_station_id,
        checksum=checksum,
    )


# **************************************************************************************
