from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_QUEUE: str

    MQTT_HOST: str
    MQTT_PORT: int
    MQTT_LOGIN: str
    MQTT_PASS: str

    CLIENT_ID_PREFIX: str

    class Config:
        env_file = '../.env'
