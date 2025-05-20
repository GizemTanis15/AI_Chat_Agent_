# agent_service/llm_service.py

import json
import urllib.request

API_KEY = "sk-a923aa50ed1b439d8dbdc5c01b39fad4"  # OpenRouter API Key


def ask_llm(message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    prompt = (
        "You are a helpful assistant in an airline chatbot. Based on the user's message, "
        "identify the intended operation and extract parameters.\n\n"
        "Return ONLY a JSON object like:\n"
        "{\n"
        "  \"intent\": \"buy_ticket\",\n"
        "  \"flight_id\": 1,\n"
        "  \"passenger_name\": \"Ali\"\n"
        "}\n\n"
        f"User message: {message}"
    )

    data = json.dumps({
        "model": "mistralai/mistral-7b-instruct",  # OpenRouter uyumlu model ID
        "messages": [
            {"role": "system", "content": "You are an airline assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as res:
            res_data = json.load(res)
            reply = res_data["choices"][0]["message"]["content"]
            return json.loads(reply)  # JSON string döndü varsayımı
    except Exception as e:
        return {"error": f"LLM Error: {str(e)}"}