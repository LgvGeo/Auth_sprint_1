from http import HTTPStatus
from tests.testdata.user import ADMIN


class TestLogin:
    async def test_user_login(self, post_data):
        data = {
            'email': ADMIN.email,
            'password': ADMIN.password
        }
        response = await post_data('/api/v1/users/login', data=data)
        assert response.status == HTTPStatus.OK
        assert 'access_token' in response.body
        assert 'refresh_token' in response.body

    async def test_user_login_invalid_username(self, post_data):
        data = {
            'email': 'plpl@lplp.lplpl',
            'password': 's'
        }
        response = await post_data('/api/v1/users/login', data=data)
        assert response.status == HTTPStatus.BAD_REQUEST

    async def test_user_login_valid_username_invalid_password(self, post_data):
        data = {
            'email': ADMIN.email,
            'password': 's'
        }
        response = await post_data('/api/v1/users/login', data=data)
        assert response.status == HTTPStatus.BAD_REQUEST

    async def test_refrsh_token(self, post_data):
        data = {
            'email': ADMIN.email,
            'password': ADMIN.password
        }
        response = await post_data('/api/v1/users/login', data=data)
        headers = {'auth': response.body['refresh_token']}
        response = await post_data(
            '/api/v1/users/login', data=data, headers=headers
        )
        assert response.status == HTTPStatus.OK
        assert 'access_token' in response.body
        assert 'refresh_token' in response.body
