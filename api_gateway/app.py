# api_gateway/app.py

from flask import Flask, request, jsonify
import urllib.request, json

app = Flask(__name__)

# Agent servisini dinleyen URL
# Agent servisini dinleyen URL
AGENT_SERVICE_URL = "http://localhost:5002/agent"

@app.route('/message', methods=['POST'])
def message():
    payload = request.get_json(silent=True) or {}
    user_input = payload.get("message", "").strip()
    if not user_input:
        return jsonify({"error": "Message is required"}), 400

    try:
        data = json.dumps({"message": user_input}).encode('utf-8')
        req = urllib.request.Request(
            AGENT_SERVICE_URL,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req) as res:
            response = json.load(res)
        return jsonify(response), 200
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        return jsonify({"error": f"AgentService error {e.code}", "details": error_body}), e.code
    except Exception as e:
        return jsonify({"error": f"Gateway Exception: {str(e)}"}), 500

if __name__=='__main__':
    app.run(port=5001, debug=True)
