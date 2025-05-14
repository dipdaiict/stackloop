from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    postgres_hostname: str
    postgres_port: str
    postgres_password: str
    postgres_dbname: str
    postgres_username: str

    model_config = ConfigDict(env_file=".env", extra="ignore")


class RedisSettings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_username: str
    redis_password: str
    redis_db: int = 0  # Default DB 0

    model_config = ConfigDict(env_file=".env", extra="ignore")


class OpenTelemetrySettings(BaseSettings):
    service_name: str = "fastapi-service"
    otlp_endpoint: str = "http://localhost:4318/v1/traces"
    
    model_config = ConfigDict(env_file=".env", extra="ignore")


# Instantiate
redis_settings = RedisSettings()
postgres_settings = PostgresSettings()
otel_settings = OpenTelemetrySettings()