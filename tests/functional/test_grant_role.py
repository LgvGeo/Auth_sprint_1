from http import HTTPStatus

from testdata.user import ADMIN, MODERATOR


class TestGrantRole:
    async def test_grant_role(self, post_data):
        data = {
            'email': ADMIN.email,
            'password': ADMIN.password
        }
        response = await post_data('/api/v1/users/login', data=data)
        headers = {'auth': response.body['access_token']}
        data = {'user_id': ADMIN.id, 'role': 'moderator'}
        response = await post_data(
            '/api/v1/roles/grant', headers=headers, data=data
        )

        assert response.status == HTTPStatus.OK
        assert response.body['id'] == ADMIN.id
        assert response.body['roles'] == ['admin', 'moderator']

    async def test_grant_role_forbidden(self, post_data):
        data = {
            'email': MODERATOR.email,
            'password': MODERATOR.password
        }
        response = await post_data('/api/v1/users/login', data=data)
        headers = {'auth': response.body['access_token']}
        data = {'user_id': ADMIN.id, 'role': 'moderator'}
        response = await post_data(
            '/api/v1/roles/grant', headers=headers, data=data
        )

        assert response.status == HTTPStatus.FORBIDDEN
