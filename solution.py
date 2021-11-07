import csv
from dataclasses import dataclass, field, fields
from datetime import datetime
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


@dataclass
class Option:

    transfers: List[str]
    flights: List[Flight]


@dataclass
class AllFlights:

    airports: List[str] = field(default_factory=list)
    flights: Dict[str, List[Flight]] = field(default_factory=dict)
    
    @classmethod
    def from_csv(cls, filepath: str = 'example/example0.csv'):

        all_flights = cls()

        with open(filepath, newline='') as csvf:
            reader = csv.DictReader(csvf)
            data = [dict(row) for row in reader]

            # Obtain list of all airports
            origins = [row['origin'] for row in data]
            destinations = [row['destination'] for row in data]
            all_flights.airports.extend(list(set(origins + destinations)))

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
                all_flights.flights.setdefault(flight.origin, []).append(flight)            
    
        return all_flights


def find_all_options(all_flights, start: str, end: str) -> List[List[Flight]]:
    relevant = []
    outgoing = all_flights.flights[start]
    
    for out in outgoing:
        if out.destination == end:
            if out not in relevant:
                relevant.append(out)
    
    return relevant


def main():
    all_flights = AllFlights.from_csv()
    relevant = find_all_options(all_flights, 'WIW', 'ECV')
    print(relevant)


if __name__ == '__main__':
    main()
