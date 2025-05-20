from flask import Flask, request, jsonify
import os
import urllib.request, urllib.error, json
from dotenv import load_dotenv
from llm_service import ask_llm
from flask import send_from_directory
from firestore_logger import log_message, get_chat_history
load_dotenv()


app = Flask(__name__)

# .env'den alınan ortam değişkenleri
AIRLINE_API_URL = os.getenv("AIRLINE_API_URL", "http://localhost:5000")
JWT_TOKEN = os.getenv("JWT_TOKEN")  # .env dosyasında "Bearer ..." şeklinde yaz

# API endpointleri
FLIGHT_API_URL     = f"{AIRLINE_API_URL}/api/v1/flights"
BUY_TICKET_URL     = f"{AIRLINE_API_URL}/api/v1/tickets"
CANCEL_TICKET_URL  = f"{AIRLINE_API_URL}/api/v1/tickets/cancel"
CHECKIN_URL        = f"{AIRLINE_API_URL}/api/v1/checkin"

# POST istekleri için yardımcı fonksiyon
def post_to_airline_api(url, payload):
    data = json.dumps(payload).encode('utf-8')

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': JWT_TOKEN
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req) as res:
            return json.load(res), 200
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "body": e.read().decode()}, e.code

# GET istekleri için yardımcı fonksiyon
def get_from_airline_api(url):
    req = urllib.request.Request(
        url,
        headers={'Authorization': JWT_TOKEN},
        method='GET'
    )
    try:
        with urllib.request.urlopen(req) as res:
            return json.load(res), 200
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "body": e.read().decode()}, e.code

# Ana endpoint
@app.route('/agent', methods=['POST'])
def agent():
    data = request.get_json(silent=True) or {}
    msg = data.get("message", "").lower().strip()

    if not msg:
        return jsonify({"error": "Message is required"}), 400

    # 1. Kullanıcı mesajını Firestore'a kaydet
    log_message("user", msg)

    parsed = ask_llm(msg)

    if "error" in parsed:
        log_message("bot", parsed["error"])  # Hata mesajını da kaydet
        return jsonify({"error": parsed["error"]}), 500

    intent = parsed.get("intent")
    flight_id = parsed.get("flight_id")
    passenger_name = parsed.get("passenger_name", "")

    response = {}

    if intent == "query_flights":
        response, status = get_from_airline_api(FLIGHT_API_URL)

    elif intent == "buy_ticket":
        response, status = post_to_airline_api(BUY_TICKET_URL, {
            "flight_id": flight_id,
            "passenger_name": passenger_name
        })

    elif intent == "cancel_ticket":
        response, status = post_to_airline_api(CANCEL_TICKET_URL, {
            "flight_id": flight_id,
            "passenger_name": passenger_name
        })

    elif intent == "check_in":
        response, status = post_to_airline_api(CHECKIN_URL, {
            "flight_id": flight_id,
            "passenger_name": passenger_name
        })

    else:
        response = {
            "reply": (
                "Üzgünüm, anlayamadım. Lütfen birini deneyin:\n"
                "- query flights\n"
                "- buy ticket flight_id=1 passenger_name=Ali\n"
                "- cancel ticket flight_id=1 passenger_name=Ali\n"
                "- check in flight_id=1 passenger_name=Ali"
            )
        }
        status = 200

    # 2. Bot mesajını Firestore'a kaydet
    bot_reply = response.get("reply") or response.get("message") or json.dumps(response)
    log_message("bot", bot_reply)

    return jsonify(response), status

@app.route('/history', methods=['GET'])
def history():
    try:
        messages = get_chat_history()
        return jsonify(messages), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def serve_index():
    return send_from_directory('chat_ui', 'index.html')

if __name__ == '__main__':
    app.run(port=5002, debug=True)
