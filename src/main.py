import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from uvicorn.workers import UvicornWorker

from api.v1 import roles, users
from db import redis
from settings import config
from settings.logger import LOGGING


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_conf = config.RedisSettings()
    redis.redis = Redis(host=redis_conf.host, port=redis_conf.port)
    yield
    await redis.redis.close()


app = FastAPI(
    title=config.CommonSettings().project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

app.include_router(users.router, prefix='/api/v1/users', tags=['users'])
app.include_router(roles.router, prefix='/api/v1/roles', tags=['roles'])


class CustomUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        'log_config': LOGGING,
        'log_level': logging.DEBUG
    }
