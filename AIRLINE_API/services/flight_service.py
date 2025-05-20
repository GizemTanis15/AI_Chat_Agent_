from models import Flight
from db_config import db

class FlightService:
    @staticmethod
    def get_all_flights(page, per_page=10):
        """
        Sayfalı uçuş listesini getirir.
        """
        return Flight.query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def create_flight(data):
        """
        Yeni uçuş oluşturur.
        """
        new_flight = Flight(
            date_from=data["date_from"],
            date_to=data["date_to"],
            airport_from=data["airport_from"],
            airport_to=data["airport_to"],
            duration=data["duration"],
            capacity=data["capacity"]
        )
        db.session.add(new_flight)
        db.session.commit()
        return new_flight
