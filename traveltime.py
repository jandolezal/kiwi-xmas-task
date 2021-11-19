from datetime import datetime


def calculate_travel_time(departure: datetime, arrival: datetime) -> str:
    td = arrival - departure
    if td.days:
        hours = td.seconds // 3600 + td.days * 24
    else:
        hours = td.seconds // 3600
    minutes = td.seconds // 60 % 60
    seconds = td.seconds % 60
    return f'{str(hours)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}'
