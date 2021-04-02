import json
from datetime import datetime
from typing import Dict, Any, Optional

from urllib3 import PoolManager

from kakaowork.consts import (
    BASE_URL,
    BASE_PATH_USERS,
)
from kakaowork.models import (
    BaseResponse,
    UserResponse,
    UserListResponse,
)


class Kakaowork:
    class Users:
        def __init__(self, client: 'Kakaowork', base_path: Optional[str] = BASE_PATH_USERS):
            self.client = client
            self.base_path = base_path

        def info(self, user_id: str) -> UserResponse:
            r = self.client.http.request(
                'GET',
                f'{self.client.base_url}{self.base_path}.info',
                fields={'user_id': user_id},
            )
            return UserResponse.from_json(r.data)

        def find_by_email(self, email: str) -> UserResponse:
            r = self.client.http.request(
                'GET',
                f'{self.client.base_url}{self.base_path}.find_by_email',
                fields={'email': email},
            )
            return UserResponse.from_json(r.data)

        def find_by_phone_number(self, phone_number: str) -> UserResponse:
            r = self.client.http.request(
                'GET',
                f'{self.client.base_url}{self.base_path}.find_by_phone_number',
                fields={'phone_number': phone_number},
            )
            return UserResponse.from_json(r.data)

        def list(self, *, cursor: Optional[str] = None, limit: Optional[int] = 10) -> UserListResponse:
            fields = {'cursor': cursor} if cursor else {'limit': limit}
            r = self.client.http.request(
                'GET',
                f'{self.client.base_url}{self.base_path}.list',
                fields=fields,
            )
            return UserListResponse.from_json(r.data)

        def set_work_time(self, user_id: str, work_start_time: datetime, work_end_time: datetime) -> BaseResponse:
            payload = {
                'user_id': user_id,
                'work_start_time': work_start_time.strftime('%s'),
                'work_end_time': work_end_time.strftime('%s'),
            }
            r = self.client.http.request(
                'POST',
                f'{self.client.base_url}{self.base_path}.set_work_time',
                body=json.dumps(payload).encode('utf-8'),
            )
            return BaseResponse.from_json(r.data)

        def set_vacation_time(self, user_id: str, vacation_start_time: datetime, vacation_end_time: datetime) -> BaseResponse:
            payload = {
                'user_id': user_id,
                'vacation_start_time': vacation_start_time.strftime('%s'),
                'vacation_end_time': vacation_end_time.strftime('%s'),
            }
            r = self.client.http.request(
                'POST',
                f'{self.client.base_url}{self.base_path}.set_vacation_time',
                body=json.dumps(payload).encode('utf-8'),
            )
            return BaseResponse.from_json(r.data)

    def __init__(self, *, app_key: str, base_url: Optional[str] = BASE_URL):
        self.app_key = app_key
        self.base_url = base_url
        self.http = PoolManager(headers=self.headers, retries=3, maxsize=5)

    @property
    def headers(self) -> Dict[str, Any]:
        return {
            'Authorization': f'Bearer {self.app_key}',
            'Content-Type': 'application/json; charset=utf-8',
        }

    @property
    def users(self) -> Users:
        return self.Users(self)
