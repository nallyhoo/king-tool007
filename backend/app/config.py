
from pydantic import BaseSettings

class Settings(BaseSettings):
    ELASTICSEARCH_URL: str = "http://elasticsearch:9200"

settings = Settings()
