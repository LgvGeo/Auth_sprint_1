from http import HTTPStatus

from testdata.user import ADMIN, MODERATOR


class TestCreateRole:
    async def test_create_role(self, post_data):
        data = {
            'email': ADMIN.email,
            'password': ADMIN.password
        }
        response = await post_data('/api/v1/users/login', data=data)
        headers = {'auth': response.body['access_token']}
        data = {'name': 'new_role'}
        response = await post_data('/api/v1/roles', headers=headers, data=data)

        assert response.status == HTTPStatus.OK

    async def test_create_role_forbidden(self, post_data):
        data = {
            'email': MODERATOR.email,
            'password': MODERATOR.password
        }
        response = await post_data('/api/v1/users/login', data=data)
        headers = {'auth': response.body['access_token']}
        data = {'name': 'new_role'}
        response = await post_data('/api/v1/roles', headers=headers, data=data)

        assert response.status == HTTPStatus.FORBIDDEN
