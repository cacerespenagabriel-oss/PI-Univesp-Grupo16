from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Se não houver variável de ambiente, ele usa o SQLite local como plano de fundo
    DATABASE_URL: str = "sqlite:///./banco.db"
    
    model_config = SettingsConfigDict(env_file="app/.env", env_file_encoding="utf-8")

settings = Settings()