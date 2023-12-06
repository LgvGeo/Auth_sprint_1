from dataclasses import dataclass

PASSWORD = 'user'
PASSWORD_HASH = (
    '$pbkdf2-sha512$25000$ec.ZE6J07l3LWcuZ05qztg$W7U/Lqld'
    'ovRi6xy8vV5QafxZ7QCvWTUBnccWb.GFLxJxu'
    '9IvfCVqv4pqCdhPvERe5AYfeTGenpa.Zhr/P4B/6A'
)


USER_DATA = [
    (
        '2d55bc49-b6e8-45d4-9874-487aefce2d0f',
        'user1@user.user', PASSWORD_HASH, 'user1', 'user1'),
    (
        '5e784a20-6414-4442-aea9-8254fccf98be',
        'user2@user.user', PASSWORD_HASH, 'user2', 'user2'),
    (
        '4118366e-b907-40ec-b19f-0039ffb5e1b5',
        'user3@user.user', PASSWORD_HASH, 'user3', 'user3'),
    (
        'a4f2dcb2-d845-4095-b401-e4dd369e4d26',
        'user4@user.user', PASSWORD_HASH, 'user4', 'user4'),
]


@dataclass
class User:
    id: str
    email: str
    password: str
    first_name: str
    last_name: str


ADMIN = User(
    '2d55bc49-b6e8-45d4-9874-487aefce2d0f',
    'user1@user.user', 'user', 'user1', 'user1')
MODERATOR = User(
    '5e784a20-6414-4442-aea9-8254fccf98be',
    'user2@user.user', 'user', 'user2', 'user2')
