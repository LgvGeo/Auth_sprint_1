from pydantic_settings import BaseSettings, SettingsConfigDict

ELASIC_INDEXES = ['movies', 'genres', 'persons']


class RedisSettings(BaseSettings):
    host: str = '127.0.0.1'
    port: int = 6379
    model_config = SettingsConfigDict(env_prefix='redis_')


class ElasticsearchSettings(BaseSettings):
    host: str = '127.0.0.1'
    port: int = 9200
    model_config = SettingsConfigDict(env_prefix='elastic_')


class PostgresSettings(BaseSettings):
    host: str = '127.0.0.1'
    port: int = 5432
    user: str = 'postgres'
    password: str = 'postgres'
    db: str = 'postgres'
    model_config = SettingsConfigDict(env_prefix='postgres_')


class CommonSettings(BaseSettings):
    api_url: str = 'http://api:8000'
