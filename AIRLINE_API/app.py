from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from models import Flight, Ticket, Checkin
from db_config import db
from services.ticket_service import TicketService
from services.flight_service import FlightService
from services.checkin_service import CheckinService
from datetime import timedelta
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# JWT config
app.config["JWT_SECRET_KEY"] = "super-secret-key"  
jwt = JWTManager(app)

# Swagger config
app.config['SWAGGER'] = {
    'uiversion': 3
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Airline API",
        "description": "API for managing flights, tickets, check-ins, and more.",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer {token}'"
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}
swagger = Swagger(app, template=swagger_template)

@app.route('/api/v1/flights', methods=['POST'])
@jwt_required()
def add_flight():
    data = request.get_json()
    try:
        required_fields = ["date_from", "date_to", "airport_from", "airport_to", "duration", "capacity"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"'{field}' field is required"}), 400

        new_flight = FlightService.create_flight(data)

        return jsonify({
            "message": "Flight added successfully!",
            "data": {
                "id": new_flight.id,
                "airport_from": new_flight.airport_from,
                "airport_to": new_flight.airport_to,
                "date_from": new_flight.date_from,
                "date_to": new_flight.date_to,
                "duration": new_flight.duration,
                "capacity": new_flight.capacity
            }
        }), 201
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route('/api/v1/flights', methods=['GET'])
@jwt_required(optional=True)
def get_flights():
    page = request.args.get('page', default=1, type=int)
    per_page = 10

    flights = FlightService.get_all_flights(page, per_page)

    data = [{
        "id": f.id,
        "airport_from": f.airport_from,
        "airport_to": f.airport_to,
        "date_from": f.date_from,
        "date_to": f.date_to,
        "duration": f.duration,
        "capacity": f.capacity
    } for f in flights.items]

    return jsonify({
        "page": page,
        "total_pages": flights.pages,
        "total_flights": flights.total,
        "flights": data
    })


@app.route('/api/v1/tickets', methods=['POST'])
@jwt_required()
def buy_ticket():
    """
    Buy a ticket for a flight
    ---
    tags:
      - Tickets
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - flight_id
            - passenger_name
          properties:
            flight_id:
              type: integer
              example: 1
            passenger_name:
              type: string
              example: Gizem Tanis
    responses:
      201:
        description: Ticket purchased successfully
      400:
        description: Invalid input or flight not found
      409:
        description: Flight is sold out
    """
    data = request.get_json()
    flight_id = data.get("flight_id")
    passenger_name = data.get("passenger_name")

    if not isinstance(passenger_name, str) or len(passenger_name.strip()) == 0 or len(passenger_name) > 100:
        return jsonify({"error": "Invalid passenger name"}), 400
    if flight_id is None or not isinstance(flight_id, int):
        return jsonify({"error": "Invalid flight ID"}), 400

    ticket, error = TicketService.buy_ticket(flight_id, passenger_name)
    if error:
        return jsonify({"error": error}), 400 if error == "Flight not found" else 409

    return jsonify({
        "message": "Ticket purchased successfully!",
        "ticket": {
            "ticket_number": ticket.ticket_number,
            "flight_id": flight_id,
            "passenger_name": passenger_name
        }
    }), 201

@app.route('/api/v1/tickets/cancel', methods=['POST'])
@jwt_required()
def cancel_ticket():
    """
    Cancel a purchased ticket
    ---
    tags:
      - Tickets
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - flight_id
            - passenger_name
          properties:
            flight_id:
              type: integer
              example: 1
            passenger_name:
              type: string
              example: Gizem Tanis
    responses:
      200:
        description: Ticket cancelled successfully
      400:
        description: Invalid input or flight ID
      404:
        description: Ticket not found
    """
    data = request.get_json()
    flight_id = data.get("flight_id")
    passenger_name = data.get("passenger_name")


    if not isinstance(passenger_name, str) or not passenger_name.strip():
        return jsonify({"error": "Invalid passenger name"}), 400
    if not isinstance(flight_id, int):
        return jsonify({"error": "Invalid flight ID"}), 400

    success, error = TicketService.cancel_ticket(flight_id, passenger_name)
    if not success:
        return jsonify({"error": error}), 404 if error == "Ticket not found" else 400

    return jsonify({"message": "Ticket cancelled successfully"}), 200


@app.route('/api/v1/checkin', methods=['POST'])
@jwt_required()
def check_in():
    """
    Perform check-in for a passenger
    ---
    tags:
      - Check-in
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - flight_id
            - passenger_name
          properties:
            flight_id:
              type: integer
              example: 1
            passenger_name:
              type: string
              example: Gizem Tanis
    responses:
      200:
        description: Check-in successful
      400:
        description: Invalid input or flight ID
      404:
        description: No valid ticket found for passenger
    """
    data = request.get_json()
    flight_id = data.get("flight_id")
    passenger_name = data.get("passenger_name")

    if not isinstance(flight_id, int) or not isinstance(passenger_name, str) or not passenger_name.strip():
        return jsonify({"error": "Invalid input"}), 400

    from services.checkin_service import CheckinService
    response, status = CheckinService.perform_checkin(flight_id, passenger_name)
    return jsonify(response), status


@app.route('/api/v1/passengers', methods=['GET'])
@jwt_required()
def get_passenger_list():
    """
    Get passenger list for a flight
    ---
    tags:
      - Passengers
    security:
      - Bearer: []
    parameters:
      - name: flight_id
        in: query
        type: integer
        required: true
        description: ID of the flight
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Page number for pagination
    responses:
      200:
        description: List of checked-in passengers for the flight
      400:
        description: Invalid flight ID
    """
    flight_id = request.args.get("flight_id", type=int)
    page = request.args.get("page", default=1, type=int)

    if flight_id is None or flight_id <= 0:
        return jsonify({"error": "Invalid flight ID"}), 400

    from services.checkin_service import CheckinService
    response, status = CheckinService.get_passenger_list(flight_id, page)
    return jsonify(response), status



@app.route('/login', methods=['POST'])
def login():
    """
    User login to receive JWT token
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: credentials
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: 1234
    responses:
      200:
        description: JWT token returned
        schema:
          type: object
          properties:
            access_token:
              type: string
              example: "eyJ0eXAiOiJKV1QiLCJh..."
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")


    if username == "admin" and password == "1234":
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(days=180)  # 🔒 Token 6 ay geçerli!
        )
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 401
    
    
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, port=5000)