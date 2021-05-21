import json
from datetime import datetime
from typing import Dict, Any, Optional, List

import aiosonic
from urllib3 import PoolManager

from kakaowork.consts import (
    Limit,
    BASE_URL,
    BASE_PATH_USERS,
    BASE_PATH_CONVERSATIONS,
    BASE_PATH_MESSAGES,
    BASE_PATH_DEPARTMENTS,
    BASE_PATH_SPACES,
    BASE_PATH_BOTS,
)
from kakaowork.models import (
    BaseResponse,
    UserResponse,
    UserListResponse,
    ConversationResponse,
    ConversationListResponse,
    MessageResponse,
    DepartmentListResponse,
    SpaceResponse,
    BotResponse,
)
from kakaowork.blockkit import Block
from kakaowork.utils import json_default


class Kakaowork:
    class Users:
        def __init__(self, client: 'Kakaowork', *, base_path: Optional[str] = BASE_PATH_USERS):
            self.client = client
            self.base_path = base_path

        def info(self, user_id: int) -> UserResponse:
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

        def list(self, *, cursor: Optional[str] = None, limit: Optional[int] = Limit.DEFAULT) -> UserListResponse:
            fields: Dict[str, Any] = {'cursor': cursor} if cursor else {'limit': str(limit)}
            r = self.client.http.request(
                'GET',
                f'{self.client.base_url}{self.base_path}.list',
                fields=fields,
            )
            return UserListResponse.from_json(r.data)

        def set_work_time(self, *, user_id: int, work_start_time: datetime, work_end_time: datetime) -> BaseResponse:
            payload = {
                'user_id': user_id,
                'work_start_time': int(work_start_time.timestamp()),
                'work_end_time': int(work_end_time.timestamp()),
            }
            r = self.client.http.request(
                'POST',
                f'{self.client.base_url}{self.base_path}.set_work_time',
                body=json.dumps(payload).encode('utf-8'),
            )
            return BaseResponse.from_json(r.data)

        def set_vacation_time(self, *, user_id: int, vacation_start_time: datetime, vacation_end_time: datetime) -> BaseResponse:
            payload = {
                'user_id': user_id,
                'vacation_start_time': int(vacation_start_time.timestamp()),
                'vacation_end_time': int(vacation_end_time.timestamp()),
            }
            r = self.client.http.request(
                'POST',
                f'{self.client.base_url}{self.base_path}.set_vacation_time',
                body=json.dumps(payload).encode('utf-8'),
            )
            return BaseResponse.from_json(r.data)

    class Conversations:
        def __init__(self, client: 'Kakaowork', *, base_path: Optional[str] = BASE_PATH_CONVERSATIONS):
            self.client = client
            self.base_path = base_path

        def open(self, *, user_ids: List[int]) -> ConversationResponse:
            payload: Dict[str, Any] = {'user_id': user_ids[0]} if len(user_ids) == 1 else {'user_ids': user_ids}
            r = self.client.http.request(
                'POST',
                f'{self.client.base_url}{self.base_path}.open',
                body=json.dumps(payload).encode('utf-8'),
            )
            return ConversationResponse.from_json(r.data)

        def list(self, *, cursor: Optional[str] = None, limit: Optional[int] = Limit.DEFAULT) -> ConversationListResponse:
            fields = {'cursor': cursor} if cursor else {'limit': str(limit)}
            r = self.client.http.request(
                'GET',
                f'{self.client.base_url}{self.base_path}.list',
                fields=fields,
            )
            return ConversationListResponse.from_json(r.data)

        def users(self, *, conversation_id: int) -> UserListResponse:
            r = self.client.http.request(
                'GET',
                f'{self.client.base_url}{self.base_path}/{conversation_id}/users',
            )
            return UserListResponse.from_json(r.data)

        def invite(self, *, conversation_id: int, user_ids: List[int]) -> BaseResponse:
            payload = {'user_ids': user_ids}
            r = self.client.http.request(
                'POST',
                f'{self.client.base_url}{self.base_path}/{conversation_id}/invite',
                body=json.dumps(payload).encode('utf-8'),
            )
            return BaseResponse.from_json(r.data)

        def kick(self, *, conversation_id: int, user_ids: List[int]) -> BaseResponse:
            payload = {'user_ids': user_ids}
            r = self.client.http.request(
                'POST',
                f'{self.client.base_url}{self.base_path}/{conversation_id}/kick',
                body=json.dumps(payload).encode('utf-8'),
            )
            return BaseResponse.from_json(r.data)

    class Messages:
        def __init__(self, client: 'Kakaowork', *, base_path: Optional[str] = BASE_PATH_MESSAGES):
            self.client = client
            self.base_path = base_path

        def send(self, *, conversation_id: int, text: str, blocks: Optional[List[Block]] = None) -> MessageResponse:
            payload = {
                'conversation_id': conversation_id,
                'text': text,
                'blocks': blocks or [],
            }
            r = self.client.http.request(
                'POST',
                f'{self.client.base_url}{self.base_path}.send',
                body=json.dumps(payload, default=json_default).encode('utf-8'),
            )
            return MessageResponse.from_json(r.data)

    class Departments:
        def __init__(self, client: 'Kakaowork', *, base_path: Optional[str] = BASE_PATH_DEPARTMENTS):
            self.client = client
            self.base_path = base_path

        def list(self, *, cursor: Optional[str] = None, limit: Optional[int] = Limit.DEFAULT) -> DepartmentListResponse:
            fields = {'cursor': cursor} if cursor else {'limit': str(limit)}
            r = self.client.http.request(
                'GET',
                f'{self.client.base_url}{self.base_path}.list',
                fields=fields,
            )
            return DepartmentListResponse.from_json(r.data)

    class Spaces:
        def __init__(self, client: 'Kakaowork', *, base_path: Optional[str] = BASE_PATH_SPACES):
            self.client = client
            self.base_path = base_path

        def info(self) -> SpaceResponse:
            r = self.client.http.request(
                'GET',
                f'{self.client.base_url}{self.base_path}.info',
            )
            return SpaceResponse.from_json(r.data)

    class Bots:
        def __init__(self, client: 'Kakaowork', *, base_path: Optional[str] = BASE_PATH_BOTS):
            self.client = client
            self.base_path = base_path

        def info(self) -> BotResponse:
            r = self.client.http.request(
                'GET',
                f'{self.client.base_url}{self.base_path}.info',
            )
            return BotResponse.from_json(r.data)

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

    @property
    def conversations(self) -> Conversations:
        return self.Conversations(self)

    @property
    def messages(self) -> Messages:
        return self.Messages(self)

    @property
    def departments(self) -> Departments:
        return self.Departments(self)

    @property
    def spaces(self) -> Spaces:
        return self.Spaces(self)

    @property
    def bots(self) -> Bots:
        return self.Bots(self)


class AsyncKakaowork:
    class Users:
        def __init__(self, client: 'AsyncKakaowork', *, base_path: Optional[str] = BASE_PATH_USERS):
            self.client = client
            self.base_path = base_path

        async def info(self, user_id: int) -> UserResponse:
            r = await self.client.http.request(
                url=f'{self.client.base_url}{self.base_path}.info',
                method='GET',
                headers=self.client.headers,
                params={'user_id': user_id},
            )
            return UserResponse.from_json(await r.content())

        async def find_by_email(self, email: str) -> UserResponse:
            r = await self.client.http.request(
                url=f'{self.client.base_url}{self.base_path}.find_by_email',
                method='GET',
                headers=self.client.headers,
                params={'email': email},
            )
            return UserResponse.from_json(await r.content())

        async def find_by_phone_number(self, phone_number: str) -> UserResponse:
            r = await self.client.http.request(
                url=f'{self.client.base_url}{self.base_path}.find_by_phone_number',
                method='GET',
                headers=self.client.headers,
                params={'phone_number': phone_number},
            )
            return UserResponse.from_json(await r.content())

        async def list(self, *, cursor: Optional[str] = None, limit: Optional[int] = Limit.DEFAULT) -> UserListResponse:
            params: Dict[str, Any] = {'cursor': cursor} if cursor else {'limit': str(limit)}
            r = await self.client.http.request(
                url=f'{self.client.base_url}{self.base_path}.list',
                method='GET',
                headers=self.client.headers,
                params=params,
            )
            return UserListResponse.from_json(await r.content())

        async def set_work_time(self, *, user_id: int, work_start_time: datetime, work_end_time: datetime) -> BaseResponse:
            payload = {
                'user_id': user_id,
                'work_start_time': int(work_start_time.timestamp()),
                'work_end_time': int(work_end_time.timestamp()),
            }
            r = await self.client.http.request(
                url=f'{self.client.base_url}{self.base_path}.set_work_time',
                method='POST',
                headers=self.client.headers,
                data=json.dumps(payload).encode('utf-8'),
            )
            return BaseResponse.from_json(await r.content())

        async def set_vacation_time(self, *, user_id: int, vacation_start_time: datetime, vacation_end_time: datetime) -> BaseResponse:
            payload = {
                'user_id': user_id,
                'vacation_start_time': int(vacation_start_time.timestamp()),
                'vacation_end_time': int(vacation_end_time.timestamp()),
            }
            r = await self.client.http.request(
                url=f'{self.client.base_url}{self.base_path}.set_vacation_time',
                method='POST',
                headers=self.client.headers,
                data=json.dumps(payload).encode('utf-8'),
            )
            return BaseResponse.from_json(await r.content())

    class Conversations:
        def __init__(self, client: 'AsyncKakaowork', *, base_path: Optional[str] = BASE_PATH_CONVERSATIONS):
            self.client = client
            self.base_path = base_path

        async def open(self, *, user_ids: List[int]) -> ConversationResponse:
            payload: Dict[str, Any] = {'user_id': user_ids[0]} if len(user_ids) == 1 else {'user_ids': user_ids}
            r = await self.client.http.request(
                url=f'{self.client.base_url}{self.base_path}.open',
                method='POST',
                headers=self.client.headers,
                data=json.dumps(payload).encode('utf-8'),
            )
            return ConversationResponse.from_json(await r.content())

        async def list(self, *, cursor: Optional[str] = None, limit: Optional[int] = Limit.DEFAULT) -> ConversationListResponse:
            params = {'cursor': cursor} if cursor else {'limit': str(limit)}
            r = await self.client.http.request(
                url=f'{self.client.base_url}{self.base_path}.list',
                method='GET',
                headers=self.client.headers,
                params=params,
            )
            return ConversationListResponse.from_json(await r.content())

        async def users(self, *, conversation_id: int) -> UserListResponse:
            r = await self.client.http.request(
                url=f'{self.client.base_url}{self.base_path}/{conversation_id}/users',
                method='GET',
                headers=self.client.headers,
            )
            return UserListResponse.from_json(await r.content())

        async def invite(self, *, conversation_id: int, user_ids: List[int]) -> BaseResponse:
            payload = {'user_ids': user_ids}
            r = await self.client.http.request(
                url=f'{self.client.base_url}{self.base_path}/{conversation_id}/invite',
                method='POST',
                headers=self.client.headers,
                data=json.dumps(payload).encode('utf-8'),
            )
            return BaseResponse.from_json(await r.content())

        async def kick(self, *, conversation_id: int, user_ids: List[int]) -> BaseResponse:
            payload = {'user_ids': user_ids}
            r = await self.client.http.request(
                url=f'{self.client.base_url}{self.base_path}/{conversation_id}/kick',
                method='POST',
                headers=self.client.headers,
                data=json.dumps(payload).encode('utf-8'),
            )
            return BaseResponse.from_json(await r.content())

    class Messages:
        def __init__(self, client: 'AsyncKakaowork', *, base_path: Optional[str] = BASE_PATH_MESSAGES):
            self.client = client
            self.base_path = base_path

        async def send(self, *, conversation_id: int, text: str, blocks: Optional[List[Block]] = None) -> MessageResponse:
            payload = {
                'conversation_id': conversation_id,
                'text': text,
                'blocks': blocks or [],
            }
            r = await self.client.http.request(
                url=f'{self.client.base_url}{self.base_path}.send',
                method='POST',
                headers=self.client.headers,
                data=json.dumps(payload, default=json_default).encode('utf-8'),
            )
            return MessageResponse.from_json(await r.content())

    class Departments:
        def __init__(self, client: 'AsyncKakaowork', *, base_path: Optional[str] = BASE_PATH_DEPARTMENTS):
            self.client = client
            self.base_path = base_path

        async def list(self, *, cursor: Optional[str] = None, limit: Optional[int] = Limit.DEFAULT) -> DepartmentListResponse:
            params = {'cursor': cursor} if cursor else {'limit': str(limit)}
            r = await self.client.http.request(
                url=f'{self.client.base_url}{self.base_path}.list',
                method='GET',
                headers=self.client.headers,
                params=params,
            )
            return DepartmentListResponse.from_json(await r.content())

    class Spaces:
        def __init__(self, client: 'AsyncKakaowork', *, base_path: Optional[str] = BASE_PATH_SPACES):
            self.client = client
            self.base_path = base_path

        async def info(self) -> SpaceResponse:
            r = await self.client.http.request(
                url=f'{self.client.base_url}{self.base_path}.info',
                method='GET',
                headers=self.client.headers,
            )
            return SpaceResponse.from_json(await r.content())

    class Bots:
        def __init__(self, client: 'AsyncKakaowork', *, base_path: Optional[str] = BASE_PATH_BOTS):
            self.client = client
            self.base_path = base_path

        async def info(self) -> BotResponse:
            r = await self.client.http.request(
                url=f'{self.client.base_url}{self.base_path}.info',
                method='GET',
                headers=self.client.headers,
            )
            return BotResponse.from_json(await r.content())

    def __init__(self, *, app_key: str, base_url: Optional[str] = BASE_URL):
        self.app_key = app_key
        self.base_url = base_url
        self.http = aiosonic.HTTPClient()

    @property
    def headers(self) -> Dict[str, Any]:
        return {
            'Authorization': f'Bearer {self.app_key}',
            'Content-Type': 'application/json; charset=utf-8',
        }

    @property
    def users(self) -> Users:
        return self.Users(self)

    @property
    def conversations(self) -> Conversations:
        return self.Conversations(self)

    @property
    def messages(self) -> Messages:
        return self.Messages(self)

    @property
    def departments(self) -> Departments:
        return self.Departments(self)

    @property
    def spaces(self) -> Spaces:
        return self.Spaces(self)

    @property
    def bots(self) -> Bots:
        return self.Bots(self)
