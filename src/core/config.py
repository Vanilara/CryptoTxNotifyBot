from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


APP_DIR: Path = Path(__file__).parent.parent
BASE_DIR: Path = APP_DIR.parent

class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env", extra='ignore')

class DBSettings(BaseConfig):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

class IntegrationsSettings(BaseConfig):
    QUICKNODE_API_KEY: str
    TRONSCAN_API_KEY: str
    QUICKNODE_ENDPOINT_URL: str

    QUICKNODE_API_URL: str = 'https://api.quicknode.com'
    TRONSCAN_API_URL: str = 'https://apilist.tronscanapi.com/api'

class AppSettings(BaseConfig):
    MODE: str
    WEBHOOK_BASE_URL: str

    @property
    def WEBHOOK_URL(self):
        return f'{self.WEBHOOK_BASE_URL}/new_transaction'

class Bot(BaseConfig):
    TOKEN: str

class Paths(BaseModel):
    QUICKNODE_STATE_FILE: str = f'{BASE_DIR}/data/quicknode_state.json'
    LOGS_PATH: str = f'{BASE_DIR}/logs'

class Settings(BaseModel):
    db: DBSettings = DBSettings() #type: ignore
    integrations: IntegrationsSettings = IntegrationsSettings() #type: ignore
    app: AppSettings = AppSettings() #type: ignore
    bot: Bot = Bot() #type: ignore
    paths: Paths = Paths()



settings = Settings()