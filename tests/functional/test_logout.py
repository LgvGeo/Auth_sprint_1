from http import HTTPStatus

from testdata.user import ADMIN


class TestLogout:
    async def test_logout(self, post_data):
        data = {
            'email': ADMIN.email,
            'password': ADMIN.password
        }
        response = await post_data('/api/v1/users/login', data=data)
        headers = {'auth': response.body['access_token']}
        response = await post_data('/api/v1/users/logout', headers=headers)
        assert response.status == HTTPStatus.OK

    async def test_logout_only_ones_with_token(self, post_data):
        data = {
            'email': ADMIN.email,
            'password': ADMIN.password
        }
        response = await post_data('/api/v1/users/login', data=data)
        headers = {'auth': response.body['access_token']}
        await post_data('/api/v1/users/logout', headers=headers)
        response = await post_data('/api/v1/users/logout', headers=headers)
        assert response.status == HTTPStatus.BAD_REQUEST
