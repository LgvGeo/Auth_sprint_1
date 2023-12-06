from http import HTTPStatus

from testdata.user import ADMIN, MODERATOR


class TestUserHistory:
    async def test_user_history(self, get_data, post_data, postgres):
        await postgres.execute('DELETE from user_history;')
        data = {
            'email': ADMIN.email,
            'password': ADMIN.password
        }
        response = await post_data('/api/v1/users/login', data=data)
        headers = {'auth': response.body['access_token']}
        print(response.body['access_token'])
        response = await get_data(
            f'/api/v1/users/history/{ADMIN.id}', headers=headers
        )

        assert response.status == HTTPStatus.OK
        assert len(response.body) == 1

    async def test_user_history_forbidden(self, get_data, post_data, postgres):
        await postgres.execute('DELETE from user_history')
        data = {
            'email': MODERATOR.email,
            'password': MODERATOR.password
        }
        response = await post_data('/api/v1/users/login', data=data)
        headers = {'auth': response.body['access_token']}
        response = await get_data(
            f'/api/v1/users/history/{ADMIN.id}', headers=headers
        )

        assert response.status == HTTPStatus.FORBIDDEN
