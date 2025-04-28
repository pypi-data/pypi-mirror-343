# **************************************************************************************

# @package        gnssrtc
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from datetime import datetime, timezone
from math import inf

from gnssrtc.nmea import (
    GPCGGNMEASentence,
    parse_gpcgg_nmea_coordinate,
    parse_gpcgg_nmea_sentence,
)

# **************************************************************************************

messages = [
    "$GPGGA,172814.0,3723.46587704,N,12202.26957864,W,2,6,1.2,18.893,M,-25.669,M,2.0,0031*4F",
    "$GPGGA,202530.00,5109.0262,N,11401.8407,W,5,40,0.5,1097.36,M,-17.00,M,18,TSTR*61",
    "$GPGGA,134658.00,5106.9792,N,11402.3003,W,2,09,1.0,1048.47,M,-16.27,M,08,AAAA*60",
    "$GNGGA,150652.00,5020.28181,N,00446.46277,W,1,06,1.19,70.5,M,51.2,M,,*6D",
    "$GNGGA,175251.48,,,,,0,00,99.99,,,,,,*71",
    "$GNGGA,,,,,,0,00,99.99,,,,,,*56",
]

# **************************************************************************************


class TestParseGPCGGNMEACoordinate(unittest.TestCase):
    def test_north_coordinate(self):
        # NMEA coordinate "4916.45" with 'N' should compute to 49 + (16.45/60)
        value = "4916.45"
        direction = "N"
        expected = 49 + (16.45 / 60.0)
        result = parse_gpcgg_nmea_coordinate(value, direction)
        self.assertAlmostEqual(result, expected, places=6)

    def test_south_coordinate(self):
        # With 'S', the computed value should be negative.
        value = "4916.45"
        direction = "S"
        expected = -(49 + (16.45 / 60.0))
        result = parse_gpcgg_nmea_coordinate(value, direction)
        self.assertAlmostEqual(result, expected, places=6)

    def test_east_coordinate(self):
        # For an east coordinate, e.g. "12311.12", the calculation is 123 + (11.12/60)
        value = "12311.12"
        direction = "E"
        expected = 123 + (11.12 / 60.0)
        result = parse_gpcgg_nmea_coordinate(value, direction)
        self.assertAlmostEqual(result, expected, places=6)

    def test_west_coordinate(self):
        # For a west coordinate, the result should be negative.
        value = "12311.12"
        direction = "W"
        expected = -(123 + (11.12 / 60.0))
        result = parse_gpcgg_nmea_coordinate(value, direction)
        self.assertAlmostEqual(result, expected, places=6)

    def test_zero_coordinate(self):
        # Testing the edge-case where the coordinate value is "0"
        value = "0"
        direction = "N"
        expected = 0.0
        result = parse_gpcgg_nmea_coordinate(value, direction)
        self.assertEqual(result, expected)


# **************************************************************************************


class TestGPCGGNMEASentence(unittest.TestCase):
    def test_parse_gpcgg_nmea_sentence_message_0(self) -> None:
        now = datetime.now(timezone.utc)
        nmea = parse_gpcgg_nmea_sentence(messages[0])
        expected = GPCGGNMEASentence(
            id="$GPGGA",
            utc=datetime(now.year, now.month, now.day, 17, 28, 14, tzinfo=timezone.utc),
            latitude=37.39109795066667,
            longitude=-122.03782631066666,
            altitude=18.893,
            quality_indicator=2,
            number_of_satellites=6,
            hdop=1.2,
            geoid_separation=-25.669,
            dgps_age=2.0,
            reference_station_id="0031",
            checksum="*4F",
        )
        self.assertEqual(nmea, expected)

    def test_parse_gpcgg_nmea_sentence_message_1(self) -> None:
        now = datetime.now(timezone.utc)
        nmea = parse_gpcgg_nmea_sentence(messages[1])
        expected = GPCGGNMEASentence(
            id="$GPGGA",
            utc=datetime(now.year, now.month, now.day, 20, 25, 30, tzinfo=timezone.utc),
            latitude=51.15043666666667,
            longitude=-114.03067833333334,
            altitude=1097.36,
            quality_indicator=5,
            number_of_satellites=40,
            hdop=0.5,
            geoid_separation=-17.0,
            dgps_age=18.0,
            reference_station_id="TSTR",
            checksum="*61",
        )
        self.assertEqual(nmea, expected)

    def test_parse_gpcgg_nmea_sentence_message_2(self) -> None:
        now = datetime.now(timezone.utc)
        nmea = parse_gpcgg_nmea_sentence(messages[2])
        expected = GPCGGNMEASentence(
            id="$GPGGA",
            utc=datetime(now.year, now.month, now.day, 13, 46, 58, tzinfo=timezone.utc),
            latitude=51.116319999999995,
            longitude=-114.03833833333334,
            altitude=1048.47,
            quality_indicator=2,
            number_of_satellites=9,
            hdop=1.0,
            geoid_separation=-16.27,
            dgps_age=8.0,
            reference_station_id="AAAA",
            checksum="*60",
        )
        self.assertEqual(nmea, expected)

    def test_parse_gpcgg_nmea_sentence_message_3(self) -> None:
        now = datetime.now(timezone.utc)
        nmea = parse_gpcgg_nmea_sentence(messages[3])
        expected = GPCGGNMEASentence(
            id="$GNGGA",
            utc=datetime(now.year, now.month, now.day, 15, 6, 52, tzinfo=timezone.utc),
            latitude=50.33803016666668,
            longitude=-4.774379499999999,
            altitude=70.5,
            quality_indicator=1,
            number_of_satellites=6,
            hdop=1.19,
            geoid_separation=51.2,
            dgps_age=None,
            reference_station_id=None,
            checksum="*6D",
        )
        self.assertEqual(nmea, expected)

    def test_parse_gpcgg_nmea_sentence_message_4(self) -> None:
        now = datetime.now(timezone.utc)
        nmea = parse_gpcgg_nmea_sentence(messages[4])
        expected = GPCGGNMEASentence(
            id="$GNGGA",
            utc=datetime(
                now.year, now.month, now.day, 17, 52, 51, 480000, tzinfo=timezone.utc
            ),
            latitude=inf,
            longitude=inf,
            altitude=inf,
            quality_indicator=0,
            number_of_satellites=0,
            hdop=99.99,
            geoid_separation=inf,
            dgps_age=None,
            reference_station_id=None,
            checksum="*71",
        )
        self.assertEqual(nmea, expected)

    def test_parse_gpcgg_nmea_sentence_message_5(self) -> None:
        now = datetime.now(timezone.utc)
        nmea = parse_gpcgg_nmea_sentence(messages[5])
        expected = GPCGGNMEASentence(
            id="$GNGGA",
            utc=nmea["utc"],
            latitude=inf,
            longitude=inf,
            altitude=inf,
            quality_indicator=0,
            number_of_satellites=0,
            hdop=99.99,
            geoid_separation=inf,
            dgps_age=None,
            reference_station_id=None,
            checksum="*56",
        )
        self.assertEqual(nmea, expected)

        # Check that the UTC time is set to the current time +/- 1 second:
        self.assertTrue(abs((nmea["utc"] - now).total_seconds()) < 1)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
