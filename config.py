from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_ID: int
    API_HASH: str
    BOT_TOKEN: str
    CHANNEL_ID: str
    CHANNEL_JOIN_LINK: str
    GROUP_ID: int
    ADMIN_ID: int

    class Config:
        env_file = '.env'


settings = Settings()
