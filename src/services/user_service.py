from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from models.service_models.role import Role
from models.service_models.user import User
from models.service_models.users_history import UsersHistory


class AlreadyExistsError(Exception):
    pass


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(
            self, email: str, password: str,
            first_name: str, last_name: str
    ):
        user = User(
            email=email, password=password,
            first_name=first_name, last_name=last_name
        )
        self.db.add(user)
        try:
            await self.db.commit()
        except IntegrityError:
            raise AlreadyExistsError
        await self.db.refresh(user)
        return user

    async def get_user(self, email: str, password: str):
        stmt = select(User).where(User.email == email)
        user = await self.db.execute(stmt)
        user = user.unique().scalar_one_or_none()
        if not user or not user.check_password(password):
            return
        return user

    async def update_user_history(self, user_id: str, action: str):
        record = UsersHistory(user_id=user_id, action=action)
        self.db.add(record)
        await self.db.commit()

    async def get_user_history(
            self, user_id: str,
            page_size: int, page_number: int
    ):
        stmt = select(UsersHistory).where(
            UsersHistory.user_id == user_id
        ).limit(page_size).offset((page_number-1)*page_size)
        result = await self.db.execute(stmt)
        result = result.scalars().all()
        return result

    async def create_role(self, name: str):
        role = Role(name=name)
        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)
        return role

    async def grant_role(self, user_id: str, role_name: str):
        stmt = select(Role).where(Role.name == role_name)
        role = await self.db.execute(stmt)
        role = role.scalar_one()
        stmt = select(User).where(User.id == user_id)
        user = await self.db.execute(stmt)
        user = user.unique().scalar_one()
        user.roles.append(role)
        self.db.add(user)
        await self.db.commit()
        return user

    async def revoke_role(self, user_id: str, role_name: str):
        stmt = select(Role).where(Role.name == role_name)
        role = await self.db.execute(stmt)
        role = role.scalar_one()
        stmt = select(User).where(User.id == user_id)
        user = await self.db.execute(stmt)
        user = user.unique().scalar_one()
        user.roles.remove(role)
        self.db.add(user)
        await self.db.commit()
        return user

    async def update_user(
        self,
        id: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str
    ):
        user = await self.db.get_one(User, id)
        if email:
            user.email = email
        if password:
            user.password = user.hash_password(password)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        self.db.add(user)
        await self.db.commit()
        return user


def get_user_service(db: AsyncSession = Depends(get_session)):
    return UserService(db)
