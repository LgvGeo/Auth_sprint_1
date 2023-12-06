from http import HTTPStatus

from testdata.user import ADMIN


class TestSignin:
    async def test_signin(self, post_data):
        data = {
            'email': 'user@example.com',
            'password': 'string',
            "first_name": 'string',
            "last_name": 'string'
        }
        response = await post_data('/api/v1/users/signin', data=data)
        assert response.status == HTTPStatus.OK

    async def test_signin_already_exists(self, post_data):
        data = {
            'email': ADMIN.email,
            'password': 'string',
            "first_name": 'string',
            "last_name": 'string'
        }
        response = await post_data('/api/v1/users/signin', data=data)
        assert response.status == HTTPStatus.BAD_REQUEST
