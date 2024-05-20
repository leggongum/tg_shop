from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_PORT: str

    SECRET_KEY: str
    DEBUG: bool

    
    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()