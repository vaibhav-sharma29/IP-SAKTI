from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── AI APIs ──────────────────────────────────────────────
    gemini_api_key:    str

    # ── Translation (Bhashini — Govt of India FREE) ──────────
    bhashini_api_key:  str = ""
    bhashini_user_id:  str = ""

    # ── AWS PostgreSQL (RDS) ──────────────────────────────────
    # Local:  postgresql+asyncpg://postgres:password@localhost:5432/ipsakti
    # AWS:    postgresql+asyncpg://user:pass@<endpoint>.rds.amazonaws.com:5432/ipsakti
    database_url:      str = "postgresql+asyncpg://postgres:password@localhost:5432/ipsakti"

    # ── ChromaDB local vector store ───────────────────────────
    chroma_db_path:    str = "./chroma_db"

    # ── App ───────────────────────────────────────────────────
    app_env:           str = "development"
    log_level:         str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
