import csv
from dataclasses import dataclass, field, fields
from datetime import datetime
from typing import List, Dict


@dataclass(eq=True, frozen=True)
class Airport:

    name: str


@dataclass
class Flight:

    flight_no: str
    origin: Airport
    destination: Airport
    departure: datetime
    arrival: datetime
    base_price: float
    bag_price: int
    bags_allowed: int

    @classmethod
    def get_fieldnames(cls) -> list:
        return [field.name for field in fields(cls)]


@dataclass
class AllFlights:

    flights: Dict[Airport, List[Airport]] = field(default_factory=dict)

    def add_airport(self, node):
        if node in self.flights:
            raise ValueError('Duplicate airport')
        else:
            self.flights[node] = []
    
    def add_flight(self, flight):
        if not (flight.origin in self.flights and flight.destination in self.flights):
            raise ValueError('Airport is not in the graph.')
        else:
            self.flights[flight.origin].append(flight)
    
    def get_airport(self, name):
        for n in self.flights:
            if n.name == name:
                return n


    @classmethod
    def from_csv(cls, filepath: str = 'example/example0.csv'):

        all_flights = cls()

        with open(filepath, newline='') as csvf:
            reader = csv.DictReader(csvf)
            data = [dict(row) for row in reader]

            origins = [row['origin'] for row in data]
            destinations = [row['destination'] for row in data]
            airport_names = list(set(origins + destinations))

            for airport_name in airport_names:
                all_flights.add_airport(Airport(name=airport_name))
            
            for row in data:
                flight = Flight(
                    flight_no=row['flight_no'],
                    origin=all_flights.get_airport(row['origin']),
                    destination=all_flights.get_airport(row['destination']),
                    arrival=datetime.fromisoformat(row['arrival']),
                    departure=datetime.fromisoformat(row['departure']),
                    base_price=float(row['base_price']),
                    bag_price=int(row['bag_price']),
                    bags_allowed=int(row['bags_allowed']),
                )
                all_flights.add_flight(flight)
    
        return all_flights


def main():
    all_flights = AllFlights.from_csv()
    print('Done')


if __name__ == '__main__':
    main()
