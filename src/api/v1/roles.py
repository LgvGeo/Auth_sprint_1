from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException

from models.request_models.role import (RoleCreateRequestModel,
                                        RoleGrantRevokeRequestModel)
from models.response_models.role import RoleCreateResponseModel
from models.response_models.user import UserResponseModel
from services.jwt_service import (JwtService, PermissionDenied,
                                  TokenValidationError, get_jwt_service)
from services.user_service import UserService, get_user_service

router = APIRouter()


@router.post(
        '',
        response_model=RoleCreateResponseModel,
        summary='Create Role',
        description='Create new role, admin permissions required'
)
async def create(
    Auth: Annotated[str, Header()],
    role: RoleCreateRequestModel,
    user_service: UserService = Depends(get_user_service),
    jwt_service: JwtService = Depends(get_jwt_service)

):
    try:
        await jwt_service.validate_access_token(Auth)
        await jwt_service.check_roles(Auth, ['admin'])
    except TokenValidationError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='bad request')
    except PermissionDenied:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='forbidden')
    role = await user_service.create_role(role.name)
    return RoleCreateResponseModel(id=str(role.id), name=str(role.name))


@router.post(
        '/grant',
        response_model=UserResponseModel,
        summary='Grant',
        description='Grant role to user, admin permissions required'
)
async def grant(
    Auth: Annotated[str, Header()],
    grant: RoleGrantRevokeRequestModel,
    user_service: UserService = Depends(get_user_service),
    jwt_service: JwtService = Depends(get_jwt_service)

):
    try:
        await jwt_service.validate_access_token(Auth)
        await jwt_service.check_roles(Auth, ['admin'])
    except TokenValidationError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='bad request')
    except PermissionDenied:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='forbidden')
    user = await user_service.grant_role(
        user_id=grant.user_id, role_name=grant.role)
    return UserResponseModel(
        id=str(user.id), first_name=user.first_name,
        last_name=user.last_name, email=user.email,
        roles=[x.name for x in user.roles]
    )


@router.post(
        '/revoke',
        response_model=UserResponseModel,
        summary='Revoke',
        description='Revoke role from user, admin permissions required'
)
async def revoke(
    Auth: Annotated[str, Header()],
    grant: RoleGrantRevokeRequestModel,
    user_service: UserService = Depends(get_user_service),
    jwt_service: JwtService = Depends(get_jwt_service)

):
    try:
        await jwt_service.validate_access_token(Auth)
        await jwt_service.check_roles(Auth, ['admin'])
    except TokenValidationError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='bad request')
    except PermissionDenied:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='forbidden')
    user = await user_service.revoke_role(
        user_id=grant.user_id, role_name=grant.role)
    return UserResponseModel(
        id=str(user.id), first_name=user.first_name,
        last_name=user.last_name, email=user.email,
        roles=[x.name for x in user.roles]
    )
