from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    date_from = db.Column(db.String, nullable=False)
    date_to = db.Column(db.String, nullable=False)
    airport_from = db.Column(db.String, nullable=False)
    airport_to = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(10), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    passenger_name = db.Column(db.String(100), nullable=False)

class Checkin(db.Model):
    __tablename__ = 'checkins'
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    passenger_name = db.Column(db.String(100), nullable=False)
    seat_number = db.Column(db.Integer)
