from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str
    bhashini_api_key: str = ""
    bhashini_user_id: str = ""
    chroma_db_path:   str = "./chroma_db"
    db_path:          str = "./ipsakti.db"
    app_env:          str = "development"
    log_level:        str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
