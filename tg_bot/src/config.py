from pydantic_settings import BaseSettings, SettingsConfigDict

from typing import Literal

class Settings(BaseSettings):
    DB_MODE: Literal['dev', 'prod'] = 'dev'

    BOT_TOKEN: str
    WEBAPP_URL: str = '127.0.0.1:3000'
    GROUP_ID: str
    CHANNEL_ID: str

    DB_HOST: str = 'localhost'
    DB_USER: str | None = None
    DB_PASS: str | None = None
    DB_NAME: str = 'test'

    @property
    def DB_URL(self):
        psql_url = f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME}'
        #sqlite_url = f'sqlite+aiosqlite:///./{self.DB_NAME}.db'
        return psql_url 
    
    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
