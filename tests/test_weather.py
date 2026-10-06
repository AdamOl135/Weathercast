import sys
import unittest
from datetime import date, datetime, timezone
from pathlib import Path
from unittest.mock import Mock, patch

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import weather


class WeatherTests(unittest.TestCase):
    def test_empty_or_short_city_does_not_make_requests(self):
        with patch("weather.requests.get") as request:
            for city in ("", "   ", "a"):
                with self.subTest(city=city), self.assertRaises(ValueError):
                    weather.get_city(city)
            request.assert_not_called()

    def test_unknown_city_does_not_request_forecast(self):
        with patch("weather.requests.get") as request, patch("weather.openmeteo", autospec=True) as client:
            request.return_value.json.return_value = {"generationtime_ms": 0.1}
            with self.assertRaisesRegex(ValueError, "City not found"):
                weather.get_city("Unknown city")
            client.weather_api.assert_not_called()

    def test_geocoding_http_errors_are_not_treated_as_missing_cities(self):
        with patch("weather.requests.get") as request:
            request.return_value.raise_for_status.side_effect = requests.HTTPError("503")
            with self.assertRaises(requests.HTTPError):
                weather.get_city("Berlin")
            request.return_value.json.assert_not_called()

    def test_forecast_dates_uv_and_temperature_precision(self):
        start = int(datetime(2026, 10, 5, 22, tzinfo=timezone.utc).timestamp())

        def variable(value):
            item = Mock()
            item.Value.return_value = value
            item.ValuesAsNumpy.return_value = value
            item.ValuesInt64AsNumpy.return_value = value
            return item

        daily = Mock()
        daily.Time.return_value = start
        daily.TimeEnd.return_value = start + 7 * 86400
        daily.Interval.return_value = 86400
        daily.Variables.side_effect = [
            variable([start + 7 * 3600]), variable([start + 18 * 3600]),
            variable([19.9] * 7), variable([-2.7] * 7),
            variable([3, 45, 61, 71, 95, 0, 2]), variable([0, 0, 5, 2, 4, 0, 0]),
        ].__getitem__
        current = Mock()
        current.Time.return_value = start + 12 * 3600 + 45 * 60
        current.Variables.side_effect = [variable(v) for v in [16, 75, 15, 1, 0, 0, 5, 0, 0, 49, 2]].__getitem__
        hourly = Mock()
        hourly.Time.return_value = start
        hourly.Interval.return_value = 3600
        uv = [0] * 168
        uv[12] = 3.7
        hourly.Variables.side_effect = [variable([16] * 168), variable([0] * 168), variable(uv)].__getitem__
        response = Mock()
        response.Current.return_value = current
        response.Hourly.return_value = hourly
        response.Daily.return_value = daily
        response.UtcOffsetSeconds.return_value = 7200
        response.Minutely15.return_value.Variables.return_value = variable([0])

        with patch("weather.requests.get") as request, patch("weather.openmeteo", autospec=True) as client:
            client.weather_api.return_value = [response]
            request.return_value.json.return_value = {"results": [{"latitude": 52.5, "longitude": 13.4, "timezone": "Europe/Berlin"}]}
            result = weather.get_city("  New York  ")
            self.assertEqual(request.call_args.kwargs["params"]["name"], "New York")
            self.assertEqual(result[2:4], [19.9, -2.7])
            self.assertEqual(result[16], 3.7)
            self.assertEqual(len(result[20]), 7)
            self.assertEqual(result[20][0]["date"], date(2026, 10, 6))
            self.assertEqual(result[20][-1]["date"], date(2026, 10, 12))
            self.assertEqual(result[20][2]["precipitation"], 5)
            self.assertEqual(result[21], 2)
            client.weather_api.assert_called_once()
            self.assertEqual(client.weather_api.call_args.kwargs["timeout"], 10)

    def test_all_weather_icons_exist_including_unknown_codes(self):
        root = Path(__file__).resolve().parents[1]
        codes = [0, 1, 2, 3, 45, 48, 51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 71, 73, 75, 77, 80, 81, 82, 85, 86, 95, 96, 97, 99, 999, float("nan")]
        for code in codes:
            for is_day in (0, 1):
                with self.subTest(code=code, is_day=is_day):
                    icon, description = weather.get_weather_icon(code, is_day)
                    self.assertTrue((root / icon).is_file())
                    self.assertTrue(description)
        self.assertEqual(weather.get_weather_icon(61)[1], "Rain")
        self.assertEqual(weather.get_weather_icon(71)[1], "Snow")


if __name__ == "__main__":
    unittest.main()
