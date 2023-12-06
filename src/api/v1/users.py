from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from fastapi.responses import ORJSONResponse, Response

from models.request_models.user import (UserLogInRequestModel,
                                        UserSignInRequestModel,
                                        UserUpdateRequestModel)
from models.response_models.user import (UserSignInResponseModel,
                                         UserUpdateResponseModel)
from models.response_models.user_history import UserHistoryResponseModel
from services.jwt_service import (JwtService, PermissionDenied,
                                  TokenValidationError, get_jwt_service)
from services.user_service import (AlreadyExistsError, UserService,
                                   get_user_service)

router = APIRouter()


@router.put(
        '',
        response_model=UserUpdateResponseModel,
        summary='update user',
        description='update user info, auth required',
)
async def update_user(
    Auth: Annotated[str, Header()],
    user: UserUpdateRequestModel,
    user_service: UserService = Depends(get_user_service),
    jwt_service: JwtService = Depends(get_jwt_service)
):
    try:
        await jwt_service.validate_access_token(Auth)
    except TokenValidationError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='bad request')
    auth_user_id = await jwt_service.get_token_payload(Auth)
    if auth_user_id != user.id:
        try:
            await jwt_service.check_roles(Auth, ['admin'])
        except PermissionDenied:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail='forbidden')
    result = await user_service.update_user(
        user.id,
        user.email,
        user.password,
        user.first_name,
        user.last_name
    )
    return UserUpdateResponseModel(
        id=result.id,
        first_name=result.first_name,
        last_name=result.last_name,
        email=result.email
    )


@router.post(
        '/signin',
        response_model=UserSignInResponseModel,
        summary='sign in',
        description='create user',
)
async def create_user(
    user: UserSignInRequestModel,
    user_service: UserService = Depends(get_user_service)
) -> UserSignInResponseModel:
    try:
        result = await user_service.create_user(
            user.email,
            user.password,
            user.first_name,
            user.last_name
        )
    except AlreadyExistsError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='already exists')
    return UserSignInResponseModel(
        id=result.id,
        first_name=result.first_name,
        last_name=result.last_name,
        email=result.email
    )


@router.post(
        '/login',
        response_class=ORJSONResponse,
        summary='log in',
        description='log user',
)
async def login_user(
    user: UserLogInRequestModel,
    user_service: UserService = Depends(get_user_service),
    jwt_service: JwtService = Depends(get_jwt_service),
):
    user_result = await user_service.get_user(
        user.email,
        user.password
    )
    if not user_result:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='bad email or password')
    roles = [x.name for x in user_result.roles]
    user_claims = {
        'user': str(user_result.id),
        'roles': roles
    }
    access_token = await jwt_service.create_access_token(data=user_claims)
    refresh_token = await jwt_service.create_refresh_token(data=user_claims)
    await user_service.update_user_history(str(user_result.id), 'login')
    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.post(
        '/refresh',
        response_class=ORJSONResponse,
        summary='refresh',
        description='refresh refresh token and get new access token',
)
async def refresh(
    Auth: Annotated[str, Header()],
    jwt_service: JwtService = Depends(get_jwt_service)
):
    try:
        await jwt_service.validate_refresh_token(Auth)
    except TokenValidationError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='bad request')
    new_refresh_token = await jwt_service.update_refresh_token(Auth)
    payload = await jwt_service.get_token_payload(Auth)
    if not new_refresh_token:
        return HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='bad request')
    access_token = await jwt_service.create_access_token(payload)
    return ORJSONResponse(
        {'access_token': access_token, 'refresh_token': new_refresh_token}
    )


@router.post(
        '/logout',
        response_class=Response,
        summary='log out',
        description='logout user, auth required',
)
async def logout_user(
    Auth: Annotated[str, Header()],
    jwt_service: JwtService = Depends(get_jwt_service),
    user_service: UserService = Depends(get_user_service)
):
    try:
        await jwt_service.validate_access_token(Auth)
    except TokenValidationError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='bad request')
    await jwt_service.del_access_token(Auth)
    payload = await jwt_service.get_token_payload(Auth)
    user_id = payload['user']
    await user_service.update_user_history(user_id, 'logout')
    return Response()


@router.get(
        '/history/{user_id}',
        response_model=list[UserHistoryResponseModel],
        summary='user history',
        description='get user history',
)
async def get_user_history(
    Auth: Annotated[str, Header()],
    user_id: str,
    page_size: Annotated[
        int, Query(description='Pagination page size', ge=1)] = 10,
    page_number: Annotated[int, Query(description='Page number', ge=1)] = 1,
    jwt_service: JwtService = Depends(get_jwt_service),
    user_service: UserService = Depends(get_user_service)
):
    try:
        await jwt_service.validate_access_token(Auth)
    except TokenValidationError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='bad request')
    auth_user_id = (await jwt_service.get_token_payload(Auth))['user']
    if auth_user_id != user_id:
        try:
            await jwt_service.check_roles(Auth, ['admin'])
        except PermissionDenied:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail='forbidden')
    result = await user_service.get_user_history(
        user_id, page_size, page_number)
    return [
        UserHistoryResponseModel(
            created_at=x.created_at,
            action=x.action
        ) for x in result
    ]
