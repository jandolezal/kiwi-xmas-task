from datetime import datetime
import unittest

from traveltime import calculate_travel_time


class TestTravelTime(unittest.TestCase):
    def test_calculate_travel_time_btw_rej_with_transfer(self):
        departure = datetime(2021, 9, 2, 5, 50)
        arrival = datetime(2021, 9, 2, 12, 45)
        travel_time = calculate_travel_time(departure, arrival)
        self.assertEqual(travel_time, '6:55:00')

    def test_calculate_travel_time_btw_rej(self):
        departure = datetime(2021, 9, 1, 17, 35)
        arrival = datetime(2021, 9, 1, 21, 5)
        travel_time = calculate_travel_time(departure, arrival)
        self.assertEqual(travel_time, '3:30:00')

    def test_calculate_travel_time_btw_rej_days_travel_time(self):
        departure = datetime(2021, 9, 1, 17, 35)
        arrival = datetime(2021, 9, 2, 18, 40)
        travel_time = calculate_travel_time(departure, arrival)
        self.assertEqual(travel_time, '25:05:00')


if __name__ == '__main__':
    unittest.main()
