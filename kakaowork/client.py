# import json
# from datetime import datetime
from typing import Dict, Any, Optional

from urllib3 import PoolManager

from kakaowork.models import UserInfoResponse


class Kakaowork:
    class Users:
        __slots__ = ('outer')

        def __init__(self, outer: 'Kakaowork'):
            self.outer = outer

        def info(self) -> UserInfoResponse:
            # https://api.kakaowork.com/v1/users.info?user_id={USER_ID}
            pass

    __slots__ = ('app_key', 'base_url')

    def __init__(self, *, app_key: str, base_url: Optional[str] = 'api.kakaowork.com'):
        self.app_key = app_key
        self.base_url = base_url
        self._http = PoolManager(headers=self.headers)

    @property
    def headers(self) -> Dict[str, Any]:
        return {
            'Authorization': f'Bearer {self.app_key}',
            'Content-Type': 'application/json;charset=utf-8',
        }

    @property
    def users(self) -> Users:
        return self.Users(self)
