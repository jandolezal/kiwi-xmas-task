import unittest
import datetime

from solution import Flight, flights_from_csv, is_enough_time, is_enough_time
import solution


class TestSolution(unittest.TestCase):
    def test_is_enough_time(self):
        incoming = Flight(
            flight_no='ZH214',
            origin='WIW',
            destination='RFZ',
            departure=datetime.datetime(2021, 9, 1, 23, 20),
            arrival=datetime.datetime(2021, 9, 2, 3, 50),
            base_price=168.0,
            bag_price=12,
            bags_allowed=2,
        )
        outgoing = Flight(
            flight_no='ZH665',
            origin='RFZ',
            destination='ECV',
            departure=datetime.datetime(2021, 9, 2, 17, 40),
            arrival=datetime.datetime(2021, 9, 2, 20, 10),
            base_price=58.0,
            bag_price=12,
            bags_allowed=2,
        )
        arrival = incoming.arrival
        departure = outgoing.departure
        self.assertFalse(is_enough_time(arrival, departure))

    def test_flights_from_csv(self):
        flights = flights_from_csv()
        some_flight = Flight(
            flight_no='ZH214',
            origin='WIW',
            destination='RFZ',
            departure=datetime.datetime(2021, 9, 1, 23, 20),
            arrival=datetime.datetime(2021, 9, 2, 3, 50),
            base_price=168.0,
            bag_price=12,
            bags_allowed=2,
        )
        self.assertIn(some_flight, flights)


if __name__ == '__main__':
    unittest.main()
