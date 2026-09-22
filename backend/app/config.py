from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── AI APIs ──────────────────────────────────────────────
    gemini_api_key: str

    # ── Bhashini (optional — Hindi translation) ──────────────
    bhashini_api_key: str = ""
    bhashini_user_id: str = ""

    # ── MongoDB Atlas ─────────────────────────────────────────
    # Free forever: mongodb.com/atlas (M0 tier)
    mongodb_url: str = "mongodb://localhost:27017"

    # ── ChromaDB local vector store ───────────────────────────
    chroma_db_path: str = "./chroma_db"

    # ── App ───────────────────────────────────────────────────
    app_env:   str = "development"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
