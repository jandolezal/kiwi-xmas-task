import argparse
import copy
import csv
from dataclasses import asdict, dataclass, field, fields
from datetime import datetime, timedelta
import json
import sys
from typing import List, Dict


@dataclass
class Flight:

    flight_no: str
    origin: str
    destination: str
    departure: datetime
    arrival: datetime
    base_price: float
    bag_price: int
    bags_allowed: int

    @classmethod
    def get_fieldnames(cls) -> list:
        return [field.name for field in fields(cls)]

    def print_schedule(self) -> None:
        print(
            f'{self.flight_no}: {self.origin} ({self.departure.isoformat()}) -> ({self.arrival.isoformat()}) {self.destination} (allowed {self.bags_allowed} bag(s))'
        )


@dataclass
class Route:

    flights: List[Flight] = field(default_factory=List)
    bags_allowed: int = None
    bags_count: int = None
    destination: str = None
    origin: str = None
    total_price: float = None
    travel_time: str = None

    def visited_airports(self) -> List[str]:
        return [flight.origin for flight in self.flights]

    def last_flight(self) -> Flight:
        return self.flights[-1]

    def add_flight(self, flight: Flight) -> None:
        self.flights.append(flight)

    def print_itinerary(self) -> None:
        print(self.origin, self.destination, len(self.flights), self.visited_airports())

    def calculate_bags_allowed(self) -> None:
        self.bags_allowed = min(flight.bags_allowed for flight in self.flights)

    def calculate_total_price(self) -> None:
        total_base_price = sum(flight.base_price for flight in self.flights)
        total_bags_price = (
            sum(flight.bag_price for flight in self.flights) * self.bags_count
        )
        self.total_price = total_base_price + total_bags_price

    def calculate_travel_time(self) -> None:
        departure = self.flights[0].departure
        arrival = self.flights[-1].arrival
        td = arrival - departure
        if td.days:
            hours = td.seconds // 3600 + td.days * 24
        else:
            hours = td.seconds // 3600
        minutes = td.seconds // 60 % 60
        seconds = td.seconds % 60
        self.travel_time = (
            f'{str(hours)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}'
        )

    def calculate(self) -> None:
        self.calculate_bags_allowed()
        self.calculate_total_price()
        self.calculate_travel_time()


def flights_from_csv(filepath: str = 'example/example0.csv') -> Dict[str, List[Flight]]:

    all_flights = []

    with open(filepath, newline='') as csvf:
        reader = csv.DictReader(csvf)
        data = [dict(row) for row in reader]
        # Prepare a dictionary mapping from airport name to list of outgoing flights
        for row in data:
            flight = Flight(
                flight_no=row['flight_no'],
                origin=row['origin'],
                destination=row['destination'],
                arrival=datetime.fromisoformat(row['arrival']),
                departure=datetime.fromisoformat(row['departure']),
                base_price=float(row['base_price']),
                bag_price=int(row['bag_price']),
                bags_allowed=int(row['bags_allowed']),
            )
            all_flights.append(flight)

    return all_flights


def is_enough_time(arrival, departure):
    return ((departure - arrival) / timedelta(hours=1) > 1) and (
        (departure - arrival) / timedelta(hours=1) < 6
    )


def list_ok_flights(
    schedule: List[Flight], airport: str, incoming_route: Route, bags_count: int
):
    ok_flights = []
    outgoing = [flight for flight in schedule if flight.origin == airport]
    for out in outgoing:
        if incoming_route:
            if (
                is_enough_time(incoming_route.last_flight().arrival, out.departure)
                and (out.destination not in incoming_route.visited_airports())
                and (out.bags_allowed >= bags_count)
            ):
                ok_flights.append(out)
        else:
            if out.bags_allowed >= bags_count:
                ok_flights.append(out)
    return ok_flights


def gather_routes(
    schedule: List[Flight], start: str, end: str, incoming_route: Route, bags_count: int
) -> List[Route]:

    routes = []

    ok_flights = list_ok_flights(schedule, start, incoming_route, bags_count)

    # One incoming route is multiplicated for each outgoing flight which is ok
    # Ok means: airport not visited, there is enough time for transfer
    for ok_flight in ok_flights:
        # This is the base condition. We reached the final destination.
        if ok_flight.destination == end:
            # First ever call of this function does not have incoming route
            if incoming_route:
                new_route = copy.deepcopy(incoming_route)
                new_route.add_flight(ok_flight)
            else:
                new_route = Route(
                    flights=[ok_flight],
                    origin=start,
                    destination=end,
                    bags_count=bags_count,
                )
            routes.append(new_route)
        # Recursive option which explores routes with the (transit) destination as new start
        else:
            if incoming_route:
                new_route = copy.deepcopy(incoming_route)
                new_route.add_flight(ok_flight)
            else:
                new_route = Route(
                    flights=[ok_flight],
                    origin=start,
                    destination=end,
                    bags_count=bags_count,
                )
            routes.extend(
                gather_routes(
                    schedule, ok_flight.destination, end, new_route, bags_count
                )
            )

    return routes


def main():
    parser = argparse.ArgumentParser(
        prog='kiwi-xmas-task',
        description='finds all possible routes between origin and destination based on number of bags.',
    )

    parser.add_argument(
        'filename', help='specify name of a CSV file which contains flights data.'
    )
    parser.add_argument('origin', help='set origin.')
    parser.add_argument('destination', help='set destination.')
    parser.add_argument(
        '-b', '--bags', help='set number of bags (default: 0).', type=int, default=0
    )

    # Gather arguments for the search
    args = parser.parse_args()
    try:
        schedule = flights_from_csv(args.filename)
    except FileNotFoundError as err:
        print(err)
        sys.exit()
    if len(args.origin) != 3 or len(args.destination) != 3:
        print('Origin and destination should be tree letter codes.')
        sys.exit()
    routes = gather_routes(
        schedule, args.origin.upper(), args.destination.upper(), None, args.bags
    )

    # Calculate travel_time, total_price and bags_allowed
    if routes:
        for route in routes:
            route.calculate()

        # Convert each Route to dict and dump json
        routes = [asdict(route) for route in routes]
        # Sort by total_price
        routes_sorted = sorted(routes, key=lambda x: x['total_price'])
        print(json.dumps(routes_sorted, default=str, indent=4))
    else:
        print(
            f'There are no options for such a journey from {args.origin} to {args.destination}'
        )


if __name__ == '__main__':
    main()
