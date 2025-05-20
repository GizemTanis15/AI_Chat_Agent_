from models import Checkin, Ticket, Flight
from db_config import db

class CheckinService:
    @staticmethod
    def perform_checkin(flight_id, passenger_name):
        # Uçuş kontrolü
        flight = Flight.query.get(flight_id)
        if not flight:
            return {"error": "Invalid flight ID"}, 400

        # Bilet kontrolü
        ticket = Ticket.query.filter_by(flight_id=flight_id, passenger_name=passenger_name).first()
        if not ticket:
            return {"error": "No valid ticket found for passenger"}, 404

        # Zaten check-in yapılmış mı?
        existing = Checkin.query.filter_by(flight_id=flight_id, passenger_name=passenger_name).first()
        if existing:
            return {
                "message": "Passenger already checked in",
                "seat_number": existing.seat_number
            }, 200

        # Koltuk numarası ataması
        seat_number = Checkin.query.filter_by(flight_id=flight_id).count() + 1

        checkin = Checkin(
            flight_id=flight_id,
            passenger_name=passenger_name,
            seat_number=seat_number
        )
        db.session.add(checkin)
        db.session.commit()

        return {
            "message": "Check-in successful!",
            "seat_number": seat_number
        }, 200

    @staticmethod
    def get_passenger_list(flight_id, page, per_page=10):
        flight = Flight.query.get(flight_id)
        if not flight:
            return {"error": "Flight not found"}, 400

        checkins = Checkin.query.filter_by(flight_id=flight_id).paginate(page=page, per_page=per_page, error_out=False)

        passenger_list = [
            {
                "passenger_name": c.passenger_name,
                "seat_number": c.seat_number
            }
            for c in checkins.items
        ]

        return {
            "flight_id": flight_id,
            "page": page,
            "total_pages": checkins.pages,
            "total_passengers": checkins.total,
            "passengers": passenger_list
        }, 200
