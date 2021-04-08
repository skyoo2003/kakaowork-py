from urllib3 import PoolManager

from kakaowork.client import Kakaowork
from kakaowork.consts import (
    BASE_URL,
    BASE_PATH_USERS,
    BASE_PATH_CONVERSATIONS,
    BASE_PATH_MESSAGES,
    BASE_PATH_DEPARTMENTS,
    BASE_PATH_SPACES,
    BASE_PATH_BOTS,
)


class TestKakaowork:
    def test_kakaowork_properties(self):
        c = Kakaowork(app_key='dummy')

        assert c.app_key == 'dummy'
        assert c.base_url == BASE_URL
        assert isinstance(c.http, PoolManager)
        assert c.headers == {
            'Authorization': 'Bearer dummy',
            'Content-Type': 'application/json; charset=utf-8',
        }
        assert isinstance(c.users, Kakaowork.Users)
        assert isinstance(c.conversations, Kakaowork.Conversations)
        assert isinstance(c.messages, Kakaowork.Messages)
        assert isinstance(c.departments, Kakaowork.Departments)
        assert isinstance(c.spaces, Kakaowork.Spaces)
        assert isinstance(c.bots, Kakaowork.Bots)


class TestKakaoworkUsers:
    def test_kakaowork_users_properties(self):
        c = Kakaowork(app_key='dummy')
        api = Kakaowork.Users(c)

        assert api.client == c
        assert api.base_path == BASE_PATH_USERS
