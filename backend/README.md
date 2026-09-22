# IP-SAKTI — Backend

FastAPI + LangChain + PostgreSQL + ChromaDB

---

## Setup (Local)

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp .env.example .env           # Fill GEMINI_API_KEY + DATABASE_URL
python main.py
```

Swagger docs: `http://localhost:8000/docs`

---

## Database Setup

### Local PostgreSQL
```sql
CREATE DATABASE ipsakti;
```
Tables are auto-created on first startup via SQLAlchemy.

### AWS RDS (Production)
1. Create RDS PostgreSQL instance (Free tier: db.t3.micro)
2. Set `DATABASE_URL` in `.env` to RDS endpoint
3. Tables auto-create on startup

---

## Build Corpus (Run ONCE before demo)

```bash
# 1. Download PDFs into these folders:
#    backend/data/raw_pdfs/india/       ← Indian laws
#    backend/data/raw_pdfs/international/ ← WIPO treaties

# 2. Build ChromaDB vector store
python -m app.services.corpus_builder

# Output: backend/chroma_db/ folder created
```

## Seed Demo Alerts (Run ONCE before demo)

```bash
curl -X POST http://localhost:8000/api/alerts/seed
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET  | `/api/health` | Health check |
| POST | `/api/chat` | Main RAG chat |
| GET  | `/api/chat/history/{session_id}` | Session history |
| POST | `/api/classify` | Formulation classifier |
| GET  | `/api/alerts` | Biopiracy alerts list |
| GET  | `/api/alerts/{id}` | Single alert |
| PATCH| `/api/alerts/{id}/read` | Mark as read |
| POST | `/api/alerts/seed` | Seed demo data |

---

## Folder Structure

```
backend/
├── main.py                      # App entry, lifespan, routes
├── requirements.txt
├── .env.example
├── Dockerfile
├── app/
│   ├── config.py                # All env vars
│   ├── database.py              # SQLAlchemy async engine (AWS RDS)
│   ├── models.py                # DB tables: sessions, messages, audit, alerts
│   ├── routes/
│   │   ├── health.py            # GET /api/health
│   │   ├── chat.py              # POST /api/chat + GET history
│   │   ├── classify.py          # POST /api/classify
│   │   └── alerts.py            # GET/PATCH /api/alerts
│   └── services/
│       ├── rag_engine.py        # LangChain + ChromaDB + Gemini
│       ├── translation.py       # Bhashini Hindi↔English
│       ├── chat_history.py      # PostgreSQL session/message ops
│       ├── audit_logger.py      # DPDP compliant audit logs
│       └── corpus_builder.py    # PDF → ChromaDB pipeline
└── data/
    └── raw_pdfs/
        ├── india/               # Indian law PDFs here
        └── international/       # WIPO treaty PDFs here
```
