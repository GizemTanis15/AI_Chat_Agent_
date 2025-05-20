# AI Chat Agent

AI Chat Agent is a smart web-based assistant that allows users to perform airline operations such as searching flights, buying/cancelling tickets, and checking in using natural language queries. The system uses LLM (OpenRouter), Flask APIs, Firebase Firestore for message logging, and a responsive HTML/CSS frontend.

## 📁 Project Structure
AI_Chat_Agent/
├── AIRLINE_API/ # Flask REST API for managing flights, tickets, check-ins
├── agent_service/ # AI-based message processing and intent handling
├── api_gateway/ # Acts as a proxy between frontend and agent service
├── README.md
├── .gitignore

Features

-  Flight operations: search, book, cancel, check-in
-  LLM-based command parsing (OpenRouter API)
-  JWT-secured backend
-  Real-time message logging with Firebase Firestore
-  Light/Dark theme toggle support
-  Chat history loading from Firestore on page load

Technologies Used

- Python (Flask)
- HTML + CSS + JS
- Firebase (Firestore, SDK)
- OpenRouter (LLM API)
- PostgreSQL + SQLAlchemy
- JWT Authentication
- Flasgger for Swagger UI

  Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/GizemTanis15/AI_Chat_Agent.git
   cd AI_Chat_Agent

2. Install backend dependencies (in each service folder):
   pip install -r requirements.txt
3. Set up environment variables:
Create a .env file in both agent_service and AIRLINE_API:
# agent_service/.env
AIRLINE_API_URL=http://localhost:5000
https://airline-api-51of.onrender.com/apidocs/#/Authentication/post_login --> deploy 
JWT_TOKEN=Bearer  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NzY4Nzg1MCwianRpIjoiNzU1YmE1NmItMGZiYS00NDgwLThlZTctYzE1MWI1ODNmYjJkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzQ3Njg3ODUwLCJjc3JmIjoiMjNmODc5ZWEtMjAwZS00ODdlLTk1YmEtODBhOGJmYzc2NDBhIiwiZXhwIjoxNzQ3Njg4NzUwfQ.MHhTUWIlqun8JWtpiHelB2iY_I_cVFBGCiImEVl_tIA
# AIRLINE_API/.env
SQLALCHEMY_DATABASE_URI=postgresql://user:pass@localhost:5432/airline_api_db

4. Add Firebase credentials:
Place the firebase_key.json file inside agent_service/.

5. Run services (in separate terminals):
   # Run backend
cd AIRLINE_API
python app.py

# Run AI agent
cd agent_service
python app.py

# Run gateway
cd api_gateway
python app.py

6. Open frontend:
Open frontend/index.html in a browser.
WEB LİNK :
https://gizemtanis15.github.io/ai-chat-agent-frontend/
This link provides direct access to the user interface (chat screen) of the project. It also displays past messages retrieved from Firebase Firestore.

Önemli Notlar
Bu projede güvenlik nedeniyle .env ve firebase_key.json gibi hassas dosyalar .gitignore dosyası aracılığıyla versiyon kontrolüne dahil edilmemiştir.
Ancak bu dosyalar yerel ortamda bulunduğu sürece uygulama sorunsuz şekilde çalışmaktadır.
Projede Firebase Firestore kullanılarak:
Kullanıcı ve bot mesajları kayıt altına alınır (loglanır),
Sohbet geçmişi, sayfa yüklendiğinde otomatik olarak yüklenir.

agent_service/.env:
OPENROUTER_API_KEY=ssk-or-v1-d097a6f6bd93ad748d02feffc6218ffe17568f0377329f99cdd783a3f408ed1b
AIRLINE_API_URL=http://localhost:5000
JWT_TOKEN=Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NzY4Nzg1MCwianRpIjoiNzU1YmE1NmItMGZiYS00NDgwLThlZTctYzE1MWI1ODNmYjJkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzQ3Njg3ODUwLCJjc3JmIjoiMjNmODc5ZWEtMjAwZS00ODdlLTk1YmEtODBhOGJmYzc2NDBhIiwiZXhwIjoxNzQ3Njg4NzUwfQ.MHhTUWIlqun8JWtpiHelB2iY_I_cVFBGCiImEVl_tIA
AIRLINE_API/.env:
SQLALCHEMY_DATABASE_URI=postgresql://airline_db_xvmm_user:jWArm2hSAQDCAfPBTIi4LbwiWIpyDirv@dpg-d043462li9vc738b34c0-a.oregon-postgres.render.com:5432/airline_db_xvmm

firebase_key.json İçeriği:
{
  "type": "service_account",
  "project_id": "ai-chat-agent-ce63e",
  "private_key_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BA...",
  "client_email": "firebase-adminsdk-xyz@ai-chat-agent-ce63e.iam.gserviceaccount.com",
  "client_id": "12345678901234567890",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xyz%40ai-chat-agent-ce63e.iam.gserviceaccount.com"
}
firebase_key.json dosyası agent_service klasörü içerisine yerleştirilmelidir.

Below is the YouTube link of the assignment where I explained this assignment.
https://youtu.be/YanqBoPI5_M
