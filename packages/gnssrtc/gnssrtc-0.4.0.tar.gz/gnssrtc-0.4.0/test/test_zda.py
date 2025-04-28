# **************************************************************************************

# @package        gnssrtc
# @license        MIT License Copyright (c) 2025 Michael J. Roberts

# **************************************************************************************

import unittest
from datetime import datetime, timezone

from gnssrtc.zda import (
    GPZDANMEASentence,
    parse_gpzda_nmea_sentence,
)

# **************************************************************************************

messages = [
    "$GPZDA,123519.00,25,03,2025,00,00*65",
    "$GNZDA,235959.99,31,12,2020,-05,30*1C",
    "$GNZDA,000000.00,01,01,2000,+00,00*7A",
]

# **************************************************************************************


class TestGPZDANMEASentence(unittest.TestCase):
    def test_parse_gpzda_nmea_sentence_message_0(self) -> None:
        nmea = parse_gpzda_nmea_sentence(messages[0])
        expected = GPZDANMEASentence(
            id="$GPZDA",
            utc=datetime(2025, 3, 25, 12, 35, 19, 0, timezone.utc),
            local_zone_offset_hours=0,
            local_zone_offset_minutes=0,
            checksum="*65",
        )
        self.assertEqual(nmea, expected)

    def test_parse_gpzda_nmea_sentence_message_1(self) -> None:
        nmea = parse_gpzda_nmea_sentence(messages[1])
        expected = GPZDANMEASentence(
            id="$GNZDA",
            utc=datetime(2020, 12, 31, 23, 59, 59, 990000, timezone.utc),
            local_zone_offset_hours=-5,
            local_zone_offset_minutes=30,
            checksum="*1C",
        )
        self.assertEqual(nmea, expected)

    def test_parse_gpzda_nmea_sentence_message_2(self) -> None:
        nmea = parse_gpzda_nmea_sentence(messages[2])
        expected = GPZDANMEASentence(
            id="$GNZDA",
            utc=datetime(2000, 1, 1, 0, 0, 0, 0, timezone.utc),
            local_zone_offset_hours=0,
            local_zone_offset_minutes=0,
            checksum="*7A",
        )
        self.assertEqual(nmea, expected)


# **************************************************************************************

if __name__ == "__main__":
    unittest.main()

# **************************************************************************************
