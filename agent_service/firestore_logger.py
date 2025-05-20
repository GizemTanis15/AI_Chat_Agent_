# agent_service/firestore_logger.py

import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# 🔴 Bu dosya adı senin indirdiğin service account dosyan
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def log_message(sender, content):
    doc_ref = db.collection("messages").document()
    doc_ref.set({
        "sender": sender,
        "content": content,
        "timestamp": datetime.datetime.utcnow()
    })

def get_chat_history(limit=20):
    messages = db.collection("messages").order_by("timestamp").limit(limit).stream()
    return [{"sender": doc.to_dict()["sender"], "content": doc.to_dict()["content"]} for doc in messages]
