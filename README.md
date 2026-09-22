# IP-SAKTI — Intelligent IP & Regulatory Assistant for Ayurveda

> **SIH 2026 | Ministry of Ayush | PS ID: SIH26045**

IP-SAKTI is a multilingual, RAG-based AI assistant that helps Ayurveda practitioners,
startups, and researchers navigate Indian and international IP laws — with source
citations, in Hindi and English, for free.

---

## Project Structure

```
IP-SAKTI/
├── frontend/     → React + Vite web application
├── backend/      → Python FastAPI + LangChain RAG engine
└── docker-compose.yml
```

---

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env         # Fill in API keys
python main.py
```
Backend runs at: `http://localhost:8000`

### Frontend
```bash
cd frontend
npm install
cp .env.example .env.local   # Set VITE_API_URL
npm run dev
```
Frontend runs at: `http://localhost:5173`

---

## Team

| Role | Name |
|------|------|
| Backend (RAG + AI) | Vaibhav Sharma |
| Frontend (UI/UX) | [Friend's Name] |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, Tailwind CSS |
| Backend | Python 3.11, FastAPI |
| AI / RAG | LangChain, ChromaDB, Gemini API |
| Multilingual | Bhashini API (Govt of India) |
| Embeddings | sentence-transformers |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Main chat query |
| POST | `/api/classify` | Formulation classifier |
| GET | `/api/prices` | Current buyback rates |
| GET | `/api/health` | Health check |

> Full API docs at `http://localhost:8000/docs` (Swagger UI)
