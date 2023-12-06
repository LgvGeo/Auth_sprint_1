from http import HTTPStatus

from testdata.user import ADMIN, MODERATOR


class TestGrantRole:
    async def test_revoke_role(self, post_data):
        data = {
            'email': ADMIN.email,
            'password': ADMIN.password
        }
        response = await post_data('/api/v1/users/login', data=data)
        headers = {'auth': response.body['access_token']}
        data = {'user_id': MODERATOR.id, 'role': 'moderator'}
        response = await post_data(
            '/api/v1/roles/revoke', headers=headers, data=data
        )

        assert response.status == HTTPStatus.OK
        assert response.body['id'] == MODERATOR.id
        assert response.body['roles'] == []

    async def test_revoke_role_forbidden(self, post_data):
        data = {
            'email': MODERATOR.email,
            'password': MODERATOR.password
        }
        response = await post_data('/api/v1/users/login', data=data)
        headers = {'auth': response.body['access_token']}
        data = {'user_id': ADMIN.id, 'role': 'moderator'}
        response = await post_data(
            '/api/v1/roles/revoke', headers=headers, data=data
        )

        assert response.status == HTTPStatus.FORBIDDEN
