import unittest
import datetime

from solution import (
    Flight,
    flights_from_csv,
    is_enough_time,
    Route,
)
import solution


class TestSolution(unittest.TestCase):

    test_route = solution.Route(
        flights=[
            Flight(
                flight_no='XC233',
                origin='BTW',
                destination='WTF',
                departure=datetime.datetime.fromisoformat('2021-09-02T05:50:00'),
                arrival=datetime.datetime.fromisoformat('2021-09-02T08:20:00'),
                base_price=67.0,
                bag_price=7.0,
                bags_allowed=2,
            ),
            Flight(
                flight_no='VJ832',
                origin='WTF',
                destination='REJ',
                departure=datetime.datetime.fromisoformat('2021-09-02T11:05:00'),
                arrival=datetime.datetime.fromisoformat('2021-09-02T12:45:00'),
                base_price=31.0,
                bag_price=5.0,
                bags_allowed=1,
            ),
        ],
        # bags_allowed=1,
        bags_count=1,
        destination='REJ',
        origin='BTW',
        # total_price=110.0,
        # travel_time='6:55:00',
    )

    def test_is_enough_time_more_than_6_hours(self):
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

    def test_is_enough_time_is_less_then_1_hour(self):
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
            departure=datetime.datetime(2021, 9, 2, 3, 55),
            arrival=datetime.datetime(2021, 9, 2, 20, 10),
            base_price=58.0,
            bag_price=12,
            bags_allowed=2,
        )
        arrival = incoming.arrival
        departure = outgoing.departure
        self.assertFalse(is_enough_time(arrival, departure))

    def test_is_enough_time_is_true(self):
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
            departure=datetime.datetime(2021, 9, 2, 4, 55),
            arrival=datetime.datetime(2021, 9, 2, 20, 10),
            base_price=58.0,
            bag_price=12,
            bags_allowed=2,
        )
        arrival = incoming.arrival
        departure = outgoing.departure
        self.assertTrue(is_enough_time(arrival, departure))

    def test_flights_from_csv(self):
        flights = flights_from_csv('example0.csv')
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

    def test_calculate_bags_allowed(self):
        self.assertEqual(self.test_route.bags_allowed, None)
        calculated_bags_allowed = self.test_route.calculate_bags_allowed()
        self.assertEqual(self.test_route.bags_allowed, 1)

    def test_calculate_total_price(self):
        self.assertEqual(self.test_route.total_price, None)
        calculated_total_price = self.test_route.calculate_total_price()
        self.assertEqual(self.test_route.total_price, 110.0)

    def test_calculate_travel_time(self):
        self.assertEqual(self.test_route.travel_time, None)
        calculated_travel_time = self.test_route.calculate_travel_time()
        self.assertEqual(self.test_route.travel_time, '6:55:00')


if __name__ == '__main__':
    unittest.main()
