from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, classify, health

app = FastAPI(
    title="IP-SAKTI API",
    description="RAG-based AI assistant for Ayurveda IP & Regulatory Guidance",
    version="1.0.0"
)

# CORS — allow frontend (localhost:5173) to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://ip-sakti.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router, prefix="/api")
app.include_router(chat.router,   prefix="/api")
app.include_router(classify.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
