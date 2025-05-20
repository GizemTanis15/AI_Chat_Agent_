from models import Ticket, Flight
from db_config import db

class TicketService:
    @staticmethod
    def buy_ticket(flight_id, passenger_name):
        flight = Flight.query.get(flight_id)
        if not flight:
            return None, "Flight not found"
        if flight.capacity <= 0:
            return None, "Flight is sold out"

        flight.capacity -= 1
        ticket_number = f"T{Ticket.query.count() + 1:03d}"

        ticket = Ticket(
            ticket_number=ticket_number,
            flight_id=flight_id,
            passenger_name=passenger_name
        )

        db.session.add(ticket)
        db.session.commit()
        return ticket, None

    @staticmethod
    def cancel_ticket(flight_id, passenger_name):
        flight = Flight.query.get(flight_id)
        if not flight:
            return False, "Flight not found"

        ticket = Ticket.query.filter_by(flight_id=flight_id, passenger_name=passenger_name).first()
        if not ticket:
            return False, "Ticket not found"

        db.session.delete(ticket)
        flight.capacity += 1
        db.session.commit()
        return True, None
