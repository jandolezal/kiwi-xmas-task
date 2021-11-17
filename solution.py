import copy
import csv
from dataclasses import dataclass, field, fields
from datetime import datetime, timedelta
from typing import List, Dict, Set


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


@dataclass
class Route:

    flights: List[Flight] = field(default_factory=List)
    bags_allowed: int = None
    bags_coount: int = None
    destination: str = None
    origin: str = None
    total_price: float = None
    travel_time: str = None

    def visited_airports(self) -> List[str]:
        return [flight.origin for flight in self.flights]

    def reached_destination(self) -> bool:
        return self.last_flight().destination == self.destination

    def last_flight(self) -> Flight:
        return self.flights[-1]

    def update_route(self, flight: Flight):
        self.flights.append(flight)


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


def list_ok_flights(schedule, airport, incoming_route):
    ok_flights = []
    outgoing = [flight for flight in schedule if flight.origin == airport]
    for out in outgoing:
        if incoming_route:
            if is_enough_time(incoming_route.last_flight().arrival, out.departure) and (
                out.destination not in incoming_route.visited_airports()
            ):
                ok_flights.append(out)
        else:
            ok_flights.append(out)
    return ok_flights


def gather_routes(schedule, start, end, incoming_route):
    routes = []

    ok_flights = list_ok_flights(schedule, start, incoming_route)

    for ok in ok_flights:
        if ok.destination == end:
            if incoming_route:
                updated_route = copy.deepcopy(incoming_route)
                updated_route.flights.append(ok)
            else:
                updated_route = Route(flights=[ok], origin=start, destination=end)
            routes.append(updated_route)
        else:
            if incoming_route:
                updated_route = copy.deepcopy(incoming_route)
                updated_route.flights.append(ok)
            else:
                updated_route = Route(flights=[ok], origin=start, destination=end)
            routes.extend(gather_routes(schedule, ok.destination, end, updated_route))

    return routes


def main():
    schedule = flights_from_csv('example/example3.csv')
    # start = 'WIW'
    # end = 'ECV'
    # start = 'DHE'
    # end = 'NIZ'
    # start = 'YOT'
    # end = 'IUQ'
    start = 'WUE'
    end = 'JBN'
    routes = gather_routes(schedule, start, end, None)
    for route in routes:
        print(
            route.origin,
            route.destination,
            len(route.flights),
            route.visited_airports(),
        )

    for flight in routes[2].flights:
        print(flight)


if __name__ == '__main__':
    main()
