from urllib3 import PoolManager

from kakaowork.client import Kakaowork
from kakaowork.consts import BASE_URL


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
