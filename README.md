# 🛡️ LogSentinel

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Gemini AI](https://img.shields.io/badge/AI-Gemini%20Flash-8E75B2?logo=google&logoColor=white)

**LogSentinel** is a next-generation log management system powered by **RAG (Retrieval-Augmented Generation)**. It not only aggregates logs but automatically diagnoses errors using **Google Gemini AI**.

---

## 🚀 Key Features

- **High-Performance Ingestion**: Asynchronous log ingestion using MongoDB (Motor).
- **Secure Architecture**: JWT Authentication & Project-scoped API Keys.
- **RAG-Powered Analysis**: Ask questions about your logs ("Why did the login fail?") and get AI-driven answers based on actual log context.
- **Modern Dashboard**: Included Single Page Application (SPA) for real-time monitoring and chat.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.11)
- **Database**: 
  - **PostgreSQL**: User/Project management (SQLAlchemy).
  - **MongoDB**: Log storage (Motor AsyncIO).
- **AI Engine**: Google Gemini 1.5 Flash (via `google-generativeai`).
- **Frontend**: Vanilla JS + Bootstrap 5.
- **Infrastructure**: Docker Compose.

---

## 🏗️ Architecture Flow

1. **Ingestion**: Client sends logs via `POST /ingest` with `X-API-Key`.
2. **Storage**: Logs are validated and stored asynchronously in **MongoDB**.
3. **Analysis (RAG)**:
   - User asks a question via Dashboard Chat.
   - System retrieves relevant logs (context) from MongoDB.
   - **Gemini AI** analyzes the context + question.
   - AI returns a diagnostic response.

---

## ⚡ Quick Start

### Prerequisites
- Docker & Docker Compose
- Google Cloud API Key (for Gemini)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/log-sentinel.git
   cd log-sentinel
   ```

2. **Configure Environment**
   Create a `.env` file in the root directory:
   ```env
   # Database Creds (Defaults work for Docker)
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=app
   
   # Security
   SECRET_KEY=your_super_secret_key_here
   
   # AI Configuration
   GOOGLE_API_KEY=your_google_gemini_api_key
   ```

3. **Run with Docker**
   ```bash
   docker compose up --build -d
   ```
   The API and Dashboard will be available at **http://localhost:8000**.

---

## 📖 Basic Usage

### 1. Create a User (Dashboard or API)
Go to the dashboard or use curl:
```bash
curl -X POST "http://localhost:8000/api/v1/signup" \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@example.com", "password": "securepassword"}'
```

### 2. Create a Project & Get API Key
Login to the Dashboard to create a project easily, or use the API. Copy the **API Key** generated.

### 3. Send a Log
Simulate a log entry using your API Key:
```bash
curl -X POST "http://localhost:8000/api/v1/logs/ingest" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: YOUR_API_KEY_HERE" \
     -d '{
           "level": "ERROR",
           "service_name": "auth-service",
           "message": "Connection timeout while reaching auth provider",
           "extra": {"attempt": 3, "latency_ms": 5000}
         }'
```

### 4. Analyze
Go to the **Dashboard Chat**, select your project, and ask:
> "Why is the auth service failing?"

LogSentinel will analyze the error logs and explain the timeout issue.

---

## 📄 License
MIT © 2026 LogSentinel Team
