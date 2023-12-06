import asyncio
import json
from typing import NamedTuple

import asyncpg
import pytest_asyncio
from aiohttp import ClientSession
from redis.asyncio import Redis

from tests.settings import (CommonSettings, PostgresSettings,
                            RedisSettings)
from tests.testdata.role import ROLE_DATA
from tests.testdata.user import USER_DATA
from tests.testdata.user_role import USER_ROLE_DATA


class Response(NamedTuple):
    body: dict
    headers: dict
    status: int


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session', name='postgres')
async def postgres_connection():
    pg_settings = PostgresSettings()
    dsn = (
        f'postgresql://{pg_settings.user}:{pg_settings.password}'
        f'@{pg_settings.host}:{pg_settings.port}/{pg_settings.db}'
    )
    connection = await asyncpg.connect(dsn)
    yield connection
    await connection.close()


@pytest_asyncio.fixture(scope='session', name='redis')
async def get_redis_connection():
    redis_conf = RedisSettings()
    redis_conn = Redis(host=redis_conf.host, port=redis_conf.port)
    yield redis_conn
    await redis_conn.close()


@pytest_asyncio.fixture(autouse=True)
async def clear_cahce(redis):
    await redis.flushall()


@pytest_asyncio.fixture(scope='session', name='client')
async def get_client():
    common_settings = CommonSettings()
    session = ClientSession(common_settings.api_url)
    yield session
    await session.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def generate_user_data(postgres: asyncpg.Connection):
    await postgres.executemany(
        'INSERT INTO public.user (id, email, password, first_name, last_name) '
        'VALUES ($1, $2, $3, $4, $5);', USER_DATA
    )
    yield
    await postgres.execute('delete from public.user;')


@pytest_asyncio.fixture(scope='session', autouse=True)
async def generate_role_data(postgres: asyncpg.Connection):
    await postgres.executemany(
        'INSERT INTO public.role (id, name) '
        'VALUES ($1, $2);', ROLE_DATA
    )
    yield
    await postgres.execute('delete from public.role;')


@pytest_asyncio.fixture(scope='session', autouse=True)
async def generate_user_role_data(postgres: asyncpg.Connection):
    await postgres.executemany(
        'INSERT INTO public.user_role (id, user_id, role_id) '
        'VALUES ($1, $2, $3);', USER_ROLE_DATA
    )
    yield
    await postgres.execute('delete from public.user_role;')


@pytest_asyncio.fixture(scope='session', autouse=True)
async def get_data(client: ClientSession):
    async def inner(url, params=None, headers=None):
        params = params or {}
        headers = headers or {}
        print(headers)
        async with client.get(url, params=params, headers=headers) as response:
            headers = response.headers
            if (
                'content-type' in headers
                and headers['content-type'] == 'application/json'
            ):
                body = await response.json()
            else:
                body = await response.text()
            status = response.status
            return Response(body, headers, status)
    return inner


@pytest_asyncio.fixture(scope='session', autouse=True)
async def post_data(client: ClientSession):
    async def inner(url, data=None, params=None, headers=None):
        params = params or {}
        headers = headers or {}
        headers['content-type'] = 'application/json'
        async with client.post(
            url, json=data, params=params, headers=headers
        ) as response:
            headers = response.headers
            if (
                'content-type' in headers
                and headers['content-type'] == 'application/json'
            ):
                body = await response.json()
            else:
                body = await response.text()
            status = response.status
            return Response(body, headers, status)
    return inner


@pytest_asyncio.fixture(scope='session', autouse=True)
async def get_data_from_cache(redis: Redis):
    async def inner(key):
        data = json.loads(await redis.get(key))
        return data
    return inner
