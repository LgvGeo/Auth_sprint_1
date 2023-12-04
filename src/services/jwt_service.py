from datetime import datetime, timedelta

import jwt
from db.cache_storage import RedisCacheStorage, get_cache_storage
from fastapi import Depends
from settings.config import CommonSettings

SETTINGS = CommonSettings()


class TokenValidationError(Exception):
    pass


class PermissionDenied(Exception):
    pass


class JwtService:
    def __init__(self, cache_storage: RedisCacheStorage):
        self.cache_storage = cache_storage

    async def create_token(
            self, data: dict,
            expires_delta: timedelta | None | int = None
    ):
        if isinstance(expires_delta, int):
            expires_delta = timedelta(seconds=expires_delta)
        to_encode = data.copy()
        now = datetime.utcnow()
        if expires_delta:
            expire = now + expires_delta
        else:
            expire = now + timedelta(minutes=15)
        to_encode.update({'exp': expire, 'iat': now})
        encoded_jwt = jwt.encode(to_encode, SETTINGS.secret_key)
        return encoded_jwt

    async def update_refresh_token(self, token) -> str | None:
        payload = await self.get_token_payload(token)
        new_ttl = payload['exp'] - payload['iat']
        roles = payload['roles']
        user = payload['user']
        new_payload = {
            'roles': roles,
            'user': user
        }
        await self.del_refresh_token(token)
        return await self.create_refresh_token(new_payload, new_ttl)

    async def validate_access_token(self, token):
        try:
            payload = jwt.decode(token, SETTINGS.secret_key, algorithms=['HS256'])
            is_token_in_cache = await self.cache_storage.get_from_cache(token)
            if is_token_in_cache or payload['type'] != 'access':
                raise
        except Exception:
            raise TokenValidationError('error')

    async def get_token_payload(self, token):
        payload = jwt.decode(token, SETTINGS.secret_key, algorithms=['HS256'])
        return payload

    async def validate_refresh_token(self, token):
        try:
            payload = jwt.decode(token, SETTINGS.secret_key, algorithms=['HS256'])
            is_token_in_cache = await self.cache_storage.get_from_cache(token)
            if not is_token_in_cache or payload['type'] != 'refresh':
                raise
        except Exception:
            raise TokenValidationError('error')

    async def create_refresh_token(
            self, data,
            expires_time=SETTINGS.refresh_token_ttl
    ):
        data = data.copy()
        data['type'] = 'refresh'
        token = await self.create_token(data, expires_time)
        await self.cache_storage.put_to_cache(token, 1, expires_time)
        return token

    async def create_access_token(
            self, data,
            expires_time=SETTINGS.access_token_ttl
    ):
        data = data.copy()
        data['type'] = 'access'
        token = await self.create_token(data, expires_time)
        return token

    async def del_access_token(self, token):
        await self.cache_storage.put_to_cache(
            token, 1, SETTINGS.access_token_ttl
        )

    async def del_refresh_token(self, token):
        await self.cache_storage.del_from_cache(token)

    async def check_roles(self, token, roles: list[str]):
        user_roles = jwt.decode(
            token, SETTINGS.secret_key,
            algorithms=['HS256']
        )['roles']
        for role in user_roles:
            if role in roles:
                return
        raise PermissionDenied


def get_jwt_service(
        cache_storage: RedisCacheStorage = Depends(get_cache_storage)
):
    return JwtService(cache_storage)
