import json
import time
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List

import urllib3
import aiosonic

from kakaowork.consts import (
    Limit,
    BASE_URL,
    BASE_PATH_USERS,
    BASE_PATH_CONVERSATIONS,
    BASE_PATH_MESSAGES,
    BASE_PATH_DEPARTMENTS,
    BASE_PATH_SPACES,
    BASE_PATH_BOTS,
    BASE_PATH_BATCH,
)
from kakaowork.models import (
    WorkTimeField,
    VacationTimeField,
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
from kakaowork.utils import json_default, drop_none
from kakaowork.ratelimit import RateLimiter


class Kakaowork:
    class Users:
        def __init__(self, client: 'Kakaowork', *, base_path: Optional[str] = BASE_PATH_USERS):
            self.client = client
            self.base_path = base_path

        def info(self, *, user_id: int) -> UserResponse:
            with self.client.limiter:
                r = self.client.http.request(
                    'GET',
                    f'{self.client.base_url}{self.base_path}.info',
                    fields={'user_id': user_id},
                )
            self.client._respect_rate_limit(r)
            return UserResponse.parse_raw(r.data)

        def find_by_email(self, email: str) -> UserResponse:
            with self.client.limiter:
                r = self.client.http.request(
                    'GET',
                    f'{self.client.base_url}{self.base_path}.find_by_email',
                    fields={'email': email},
                )
            self.client._respect_rate_limit(r)
            return UserResponse.parse_raw(r.data)

        def find_by_phone_number(self, phone_number: str) -> UserResponse:
            with self.client.limiter:
                r = self.client.http.request(
                    'GET',
                    f'{self.client.base_url}{self.base_path}.find_by_phone_number',
                    fields={'phone_number': phone_number},
                )
            self.client._respect_rate_limit(r)
            return UserResponse.parse_raw(r.data)

        def list(self, *, cursor: Optional[str] = None, limit: Optional[int] = Limit.DEFAULT) -> UserListResponse:
            fields: Dict[str, Any] = {'cursor': cursor} if cursor else {'limit': str(limit)}
            with self.client.limiter:
                r = self.client.http.request(
                    'GET',
                    f'{self.client.base_url}{self.base_path}.list',
                    fields=fields,
                )
            self.client._respect_rate_limit(r)
            return UserListResponse.parse_raw(r.data)

        def set_work_time(self, *, user_id: int, work_start_time: datetime, work_end_time: datetime) -> BaseResponse:
            payload = {
                'user_id': user_id,
                'work_start_time': int(work_start_time.timestamp()),
                'work_end_time': int(work_end_time.timestamp()),
            }
            with self.client.limiter:
                r = self.client.http.request(
                    'POST',
                    f'{self.client.base_url}{self.base_path}.set_work_time',
                    body=json.dumps(payload).encode('utf-8'),
                )
            self.client._respect_rate_limit(r)
            return BaseResponse.parse_raw(r.data)

        def set_vacation_time(self, *, user_id: int, vacation_start_time: datetime, vacation_end_time: datetime) -> BaseResponse:
            payload = {
                'user_id': user_id,
                'vacation_start_time': int(vacation_start_time.timestamp()),
                'vacation_end_time': int(vacation_end_time.timestamp()),
            }
            with self.client.limiter:
                r = self.client.http.request(
                    'POST',
                    f'{self.client.base_url}{self.base_path}.set_vacation_time',
                    body=json.dumps(payload).encode('utf-8'),
                )
            self.client._respect_rate_limit(r)
            return BaseResponse.parse_raw(r.data)

    class Conversations:
        def __init__(self, client: 'Kakaowork', *, base_path: Optional[str] = BASE_PATH_CONVERSATIONS):
            self.client = client
            self.base_path = base_path

        def open(self, *, user_ids: List[int]) -> ConversationResponse:
            payload: Dict[str, Any] = {'user_id': user_ids[0]} if len(user_ids) == 1 else {'user_ids': user_ids}
            with self.client.limiter:
                r = self.client.http.request(
                    'POST',
                    f'{self.client.base_url}{self.base_path}.open',
                    body=json.dumps(payload).encode('utf-8'),
                )
            self.client._respect_rate_limit(r)
            return ConversationResponse.parse_raw(r.data)

        def list(self, *, cursor: Optional[str] = None, limit: Optional[int] = Limit.DEFAULT) -> ConversationListResponse:
            fields = {'cursor': cursor} if cursor else {'limit': str(limit)}
            with self.client.limiter:
                r = self.client.http.request(
                    'GET',
                    f'{self.client.base_url}{self.base_path}.list',
                    fields=fields,
                )
            self.client._respect_rate_limit(r)
            return ConversationListResponse.parse_raw(r.data)

        def users(self, *, conversation_id: int) -> UserListResponse:
            with self.client.limiter:
                r = self.client.http.request(
                    'GET',
                    f'{self.client.base_url}{self.base_path}/{conversation_id}/users',
                )
            self.client._respect_rate_limit(r)
            return UserListResponse.parse_raw(r.data)

        def invite(self, *, conversation_id: int, user_ids: List[int]) -> BaseResponse:
            payload = {'user_ids': user_ids}
            with self.client.limiter:
                r = self.client.http.request(
                    'POST',
                    f'{self.client.base_url}{self.base_path}/{conversation_id}/invite',
                    body=json.dumps(payload).encode('utf-8'),
                )
            self.client._respect_rate_limit(r)
            return BaseResponse.parse_raw(r.data)

        def kick(self, *, conversation_id: int, user_ids: List[int]) -> BaseResponse:
            payload = {'user_ids': user_ids}
            with self.client.limiter:
                r = self.client.http.request(
                    'POST',
                    f'{self.client.base_url}{self.base_path}/{conversation_id}/kick',
                    body=json.dumps(payload).encode('utf-8'),
                )
            self.client._respect_rate_limit(r)
            return BaseResponse.parse_raw(r.data)

    class Messages:
        def __init__(self, client: 'Kakaowork', *, base_path: Optional[str] = BASE_PATH_MESSAGES):
            self.client = client
            self.base_path = base_path

        def send(self, *, conversation_id: int, text: str, blocks: Optional[List[Block]] = None) -> MessageResponse:
            payload = drop_none({
                'conversation_id': conversation_id,
                'text': text,
                'blocks': blocks,
            })
            with self.client.limiter:
                r = self.client.http.request(
                    'POST',
                    f'{self.client.base_url}{self.base_path}.send',
                    body=json.dumps(payload, default=json_default).encode('utf-8'),
                )
            self.client._respect_rate_limit(r)
            return MessageResponse.parse_raw(r.data)

        def send_by(self, *, text: str, email: Optional[str] = None, key: Optional[str] = None, blocks: Optional[List[Block]] = None) -> MessageResponse:
            if not (email or key):
                raise ValueError("Either 'email' or 'key' must exist.")
            payload = drop_none({
                'email': email,
                'key': key,
                'text': text,
                'blocks': blocks,
            })
            with self.client.limiter:
                r = self.client.http.request(
                    'POST',
                    f'{self.client.base_url}{self.base_path}.send_by',
                    body=json.dumps(payload, default=json_default).encode('utf-8'),
                )
            self.client._respect_rate_limit(r)
            return MessageResponse.parse_raw(r.data)

        def send_by_email(self, email: str, *, text: str, blocks: Optional[List[Block]] = None) -> MessageResponse:
            payload = drop_none({
                'email': email,
                'text': text,
                'blocks': blocks,
            })
            with self.client.limiter:
                r = self.client.http.request(
                    'POST',
                    f'{self.client.base_url}{self.base_path}.send_by_email',
                    body=json.dumps(payload, default=json_default).encode('utf-8'),
                )
            self.client._respect_rate_limit(r)
            return MessageResponse.parse_raw(r.data)

    class Departments:
        def __init__(self, client: 'Kakaowork', *, base_path: Optional[str] = BASE_PATH_DEPARTMENTS):
            self.client = client
            self.base_path = base_path

        def list(self, *, cursor: Optional[str] = None, limit: Optional[int] = Limit.DEFAULT) -> DepartmentListResponse:
            fields = {'cursor': cursor} if cursor else {'limit': str(limit)}
            with self.client.limiter:
                r = self.client.http.request(
                    'GET',
                    f'{self.client.base_url}{self.base_path}.list',
                    fields=fields,
                )
            self.client._respect_rate_limit(r)
            return DepartmentListResponse.parse_raw(r.data)

    class Spaces:
        def __init__(self, client: 'Kakaowork', *, base_path: Optional[str] = BASE_PATH_SPACES):
            self.client = client
            self.base_path = base_path

        def info(self) -> SpaceResponse:
            with self.client.limiter:
                r = self.client.http.request(
                    'GET',
                    f'{self.client.base_url}{self.base_path}.info',
                )
            self.client._respect_rate_limit(r)
            return SpaceResponse.parse_raw(r.data)

    class Bots:
        def __init__(self, client: 'Kakaowork', *, base_path: Optional[str] = BASE_PATH_BOTS):
            self.client = client
            self.base_path = base_path

        def info(self) -> BotResponse:
            with self.client.limiter:
                r = self.client.http.request(
                    'GET',
                    f'{self.client.base_url}{self.base_path}.info',
                )
            self.client._respect_rate_limit(r)
            return BotResponse.parse_raw(r.data)

    def __init__(self, *, app_key: str, base_url: Optional[str] = BASE_URL):
        self.app_key = app_key
        self.base_url = base_url
        self.http = urllib3.PoolManager(headers=self.headers, retries=3, maxsize=5)
        self.limiter = RateLimiter(capacity=0, refill_rate=60.0)

    def _respect_rate_limit(self, response: urllib3.HTTPResponse) -> None:
        if 200 <= response.status < 300 and self.limiter.capacity <= 0:
            capacity = int(response.headers.get('ratelimit-limit', 0))
            self.limiter.reset(capacity=capacity)
        elif response.status == 429:
            capacity = int(response.headers.get('ratelimit-limit', 0))
            wait_time = int(response.headers.get('retry-after', 0))
            time.sleep(wait_time)
            self.limiter.reset(capacity=capacity)

    class Batch:
        def __init__(self, client: 'Kakaowork', *, base_path: Optional[str] = BASE_PATH_BATCH):
            self.client = client
            self.base_path = base_path

        class Users:
            def __init__(self, batch: 'Kakaowork.Batch'):
                self.client = batch.client
                self.base_path = f'{batch.base_path}/users'

            def set_work_time(self, items: List[WorkTimeField]) -> BaseResponse:
                payload = {
                    'user_work_times': [item.dict(exclude_none=True) for item in items],
                }
                with self.client.limiter:
                    r = self.client.http.request(
                        'POST',
                        f'{self.client.base_url}{self.base_path}.set_work_time',
                        body=json.dumps(payload, default=json_default).encode('utf-8'),
                    )
                self.client._respect_rate_limit(r)
                return BaseResponse.parse_raw(r.data)

            def set_vacation_time(self, items: List[VacationTimeField]) -> BaseResponse:
                payload = {
                    'user_vacation_times': [item.dict(exclude_none=True) for item in items],
                }
                with self.client.limiter:
                    r = self.client.http.request(
                        'POST',
                        f'{self.client.base_url}{self.base_path}.set_vacation_time',
                        body=json.dumps(payload, default=json_default).encode('utf-8'),
                    )
                self.client._respect_rate_limit(r)
                return BaseResponse.parse_raw(r.data)

            def reset_work_time(self, *, user_ids: List[int]) -> BaseResponse:
                payload = {
                    'user_ids': user_ids,
                }
                with self.client.limiter:
                    r = self.client.http.request(
                        'POST',
                        f'{self.client.base_url}{self.base_path}.reset_work_time',
                        body=json.dumps(payload).encode('utf-8'),
                    )
                self.client._respect_rate_limit(r)
                return BaseResponse.parse_raw(r.data)

            def reset_vacation_time(self, *, user_ids: List[int]) -> BaseResponse:
                payload = {
                    'user_ids': user_ids,
                }
                with self.client.limiter:
                    r = self.client.http.request(
                        'POST',
                        f'{self.client.base_url}{self.base_path}.reset_vacation_time',
                        body=json.dumps(payload).encode('utf-8'),
                    )
                self.client._respect_rate_limit(r)
                return BaseResponse.parse_raw(r.data)

        @property
        def users(self) -> Users:
            return self.Users(self)

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

    @property
    def batch(self) -> Batch:
        return self.Batch(self)


class AsyncKakaowork:
    class Users:
        def __init__(self, client: 'AsyncKakaowork', *, base_path: Optional[str] = BASE_PATH_USERS):
            self.client = client
            self.base_path = base_path

        async def info(self, *, user_id: int) -> UserResponse:
            async with self.client.limiter:
                r = await self.client.http.request(
                    url=f'{self.client.base_url}{self.base_path}.info',
                    method='GET',
                    headers=self.client.headers,
                    params={'user_id': user_id},
                )
            await self.client._respect_rate_limit(r)
            return UserResponse.parse_raw(await r.content())

        async def find_by_email(self, email: str) -> UserResponse:
            async with self.client.limiter:
                r = await self.client.http.request(
                    url=f'{self.client.base_url}{self.base_path}.find_by_email',
                    method='GET',
                    headers=self.client.headers,
                    params={'email': email},
                )
            await self.client._respect_rate_limit(r)
            return UserResponse.parse_raw(await r.content())

        async def find_by_phone_number(self, phone_number: str) -> UserResponse:
            async with self.client.limiter:
                r = await self.client.http.request(
                    url=f'{self.client.base_url}{self.base_path}.find_by_phone_number',
                    method='GET',
                    headers=self.client.headers,
                    params={'phone_number': phone_number},
                )
            await self.client._respect_rate_limit(r)
            return UserResponse.parse_raw(await r.content())

        async def list(self, *, cursor: Optional[str] = None, limit: Optional[int] = Limit.DEFAULT) -> UserListResponse:
            params: Dict[str, Any] = {'cursor': cursor} if cursor else {'limit': str(limit)}
            async with self.client.limiter:
                r = await self.client.http.request(
                    url=f'{self.client.base_url}{self.base_path}.list',
                    method='GET',
                    headers=self.client.headers,
                    params=params,
                )
            await self.client._respect_rate_limit(r)
            return UserListResponse.parse_raw(await r.content())

        async def set_work_time(self, *, user_id: int, work_start_time: datetime, work_end_time: datetime) -> BaseResponse:
            payload = {
                'user_id': user_id,
                'work_start_time': int(work_start_time.timestamp()),
                'work_end_time': int(work_end_time.timestamp()),
            }
            async with self.client.limiter:
                r = await self.client.http.request(
                    url=f'{self.client.base_url}{self.base_path}.set_work_time',
                    method='POST',
                    headers=self.client.headers,
                    data=json.dumps(payload).encode('utf-8'),
                )
            await self.client._respect_rate_limit(r)
            return BaseResponse.parse_raw(await r.content())

        async def set_vacation_time(self, *, user_id: int, vacation_start_time: datetime, vacation_end_time: datetime) -> BaseResponse:
            payload = {
                'user_id': user_id,
                'vacation_start_time': int(vacation_start_time.timestamp()),
                'vacation_end_time': int(vacation_end_time.timestamp()),
            }
            async with self.client.limiter:
                r = await self.client.http.request(
                    url=f'{self.client.base_url}{self.base_path}.set_vacation_time',
                    method='POST',
                    headers=self.client.headers,
                    data=json.dumps(payload).encode('utf-8'),
                )
            await self.client._respect_rate_limit(r)
            return BaseResponse.parse_raw(await r.content())

    class Conversations:
        def __init__(self, client: 'AsyncKakaowork', *, base_path: Optional[str] = BASE_PATH_CONVERSATIONS):
            self.client = client
            self.base_path = base_path

        async def open(self, *, user_ids: List[int]) -> ConversationResponse:
            payload: Dict[str, Any] = {'user_id': user_ids[0]} if len(user_ids) == 1 else {'user_ids': user_ids}
            async with self.client.limiter:
                r = await self.client.http.request(
                    url=f'{self.client.base_url}{self.base_path}.open',
                    method='POST',
                    headers=self.client.headers,
                    data=json.dumps(payload).encode('utf-8'),
                )
            await self.client._respect_rate_limit(r)
            return ConversationResponse.parse_raw(await r.content())

        async def list(self, *, cursor: Optional[str] = None, limit: Optional[int] = Limit.DEFAULT) -> ConversationListResponse:
            params = {'cursor': cursor} if cursor else {'limit': str(limit)}
            async with self.client.limiter:
                r = await self.client.http.request(
                    url=f'{self.client.base_url}{self.base_path}.list',
                    method='GET',
                    headers=self.client.headers,
                    params=params,
                )
            await self.client._respect_rate_limit(r)
            return ConversationListResponse.parse_raw(await r.content())

        async def users(self, *, conversation_id: int) -> UserListResponse:
            async with self.client.limiter:
                r = await self.client.http.request(
                    url=f'{self.client.base_url}{self.base_path}/{conversation_id}/users',
                    method='GET',
                    headers=self.client.headers,
                )
            await self.client._respect_rate_limit(r)
            return UserListResponse.parse_raw(await r.content())

        async def invite(self, *, conversation_id: int, user_ids: List[int]) -> BaseResponse:
            payload = {'user_ids': user_ids}
            async with self.client.limiter:
                r = await self.client.http.request(
                    url=f'{self.client.base_url}{self.base_path}/{conversation_id}/invite',
                    method='POST',
                    headers=self.client.headers,
                    data=json.dumps(payload).encode('utf-8'),
                )
            await self.client._respect_rate_limit(r)
            return BaseResponse.parse_raw(await r.content())

        async def kick(self, *, conversation_id: int, user_ids: List[int]) -> BaseResponse:
            payload = {'user_ids': user_ids}
            async with self.client.limiter:
                r = await self.client.http.request(
                    url=f'{self.client.base_url}{self.base_path}/{conversation_id}/kick',
                    method='POST',
                    headers=self.client.headers,
                    data=json.dumps(payload).encode('utf-8'),
                )
            await self.client._respect_rate_limit(r)
            return BaseResponse.parse_raw(await r.content())

    class Messages:
        def __init__(self, client: 'AsyncKakaowork', *, base_path: Optional[str] = BASE_PATH_MESSAGES):
            self.client = client
            self.base_path = base_path

        async def send(self, *, conversation_id: int, text: str, blocks: Optional[List[Block]] = None) -> MessageResponse:
            payload = drop_none({
                'conversation_id': conversation_id,
                'text': text,
                'blocks': blocks,
            })
            async with self.client.limiter:
                r = await self.client.http.request(
                    url=f'{self.client.base_url}{self.base_path}.send',
                    method='POST',
                    headers=self.client.headers,
                    data=json.dumps(payload, default=json_default).encode('utf-8'),
                )
            await self.client._respect_rate_limit(r)
            return MessageResponse.parse_raw(await r.content())

        async def send_by(self, *, text: str, email: Optional[str] = None, key: Optional[str] = None, blocks: Optional[List[Block]] = None) -> MessageResponse:
            if not (email or key):
                raise ValueError("Either 'email' or 'key' must exist.")
            payload = drop_none({
                'email': email,
                'key': key,
                'text': text,
                'blocks': blocks,
            })
            async with self.client.limiter:
                r = await self.client.http.request(
                    url=f'{self.client.base_url}{self.base_path}.send_by',
                    method='POST',
                    headers=self.client.headers,
                    data=json.dumps(payload, default=json_default).encode('utf-8'),
                )
            await self.client._respect_rate_limit(r)
            return MessageResponse.parse_raw(await r.content())

        async def send_by_email(self, email: str, *, text: str, blocks: Optional[List[Block]] = None) -> MessageResponse:
            payload = drop_none({
                'email': email,
                'text': text,
                'blocks': blocks,
            })
            async with self.client.limiter:
                r = await self.client.http.request(
                    url=f'{self.client.base_url}{self.base_path}.send_by_email',
                    method='POST',
                    headers=self.client.headers,
                    data=json.dumps(payload, default=json_default).encode('utf-8'),
                )
            await self.client._respect_rate_limit(r)
            return MessageResponse.parse_raw(await r.content())

    class Departments:
        def __init__(self, client: 'AsyncKakaowork', *, base_path: Optional[str] = BASE_PATH_DEPARTMENTS):
            self.client = client
            self.base_path = base_path

        async def list(self, *, cursor: Optional[str] = None, limit: Optional[int] = Limit.DEFAULT) -> DepartmentListResponse:
            params = {'cursor': cursor} if cursor else {'limit': str(limit)}
            async with self.client.limiter:
                r = await self.client.http.request(
                    url=f'{self.client.base_url}{self.base_path}.list',
                    method='GET',
                    headers=self.client.headers,
                    params=params,
                )
            await self.client._respect_rate_limit(r)
            return DepartmentListResponse.parse_raw(await r.content())

    class Spaces:
        def __init__(self, client: 'AsyncKakaowork', *, base_path: Optional[str] = BASE_PATH_SPACES):
            self.client = client
            self.base_path = base_path

        async def info(self) -> SpaceResponse:
            async with self.client.limiter:
                r = await self.client.http.request(
                    url=f'{self.client.base_url}{self.base_path}.info',
                    method='GET',
                    headers=self.client.headers,
                )
            await self.client._respect_rate_limit(r)
            return SpaceResponse.parse_raw(await r.content())

    class Bots:
        def __init__(self, client: 'AsyncKakaowork', *, base_path: Optional[str] = BASE_PATH_BOTS):
            self.client = client
            self.base_path = base_path

        async def info(self) -> BotResponse:
            async with self.client.limiter:
                r = await self.client.http.request(
                    url=f'{self.client.base_url}{self.base_path}.info',
                    method='GET',
                    headers=self.client.headers,
                )
            await self.client._respect_rate_limit(r)
            return BotResponse.parse_raw(await r.content())

    class Batch:
        def __init__(self, client: 'AsyncKakaowork', *, base_path: Optional[str] = BASE_PATH_BATCH):
            self.client = client
            self.base_path = base_path

        class Users:
            def __init__(self, batch: 'AsyncKakaowork.Batch'):
                self.client = batch.client
                self.base_path = f'{batch.base_path}/users'

            async def set_work_time(self, items: List[WorkTimeField]) -> BaseResponse:
                payload = {
                    'user_work_times': [item.dict(exclude_none=True) for item in items],
                }
                async with self.client.limiter:
                    r = await self.client.http.request(
                        url=f'{self.client.base_url}{self.base_path}.set_work_time',
                        method='POST',
                        headers=self.client.headers,
                        data=json.dumps(payload, default=json_default).encode('utf-8'),
                    )
                await self.client._respect_rate_limit(r)
                return BaseResponse.parse_raw(await r.content())

            async def set_vacation_time(self, items: List[VacationTimeField]) -> BaseResponse:
                payload = {
                    'user_vacation_times': [item.dict(exclude_none=True) for item in items],
                }
                async with self.client.limiter:
                    r = await self.client.http.request(
                        url=f'{self.client.base_url}{self.base_path}.set_vacation_time',
                        method='POST',
                        headers=self.client.headers,
                        data=json.dumps(payload, default=json_default).encode('utf-8'),
                    )
                await self.client._respect_rate_limit(r)
                return BaseResponse.parse_raw(await r.content())

            async def reset_work_time(self, *, user_ids: List[int]) -> BaseResponse:
                payload = {
                    'user_ids': user_ids,
                }
                async with self.client.limiter:
                    r = await self.client.http.request(
                        url=f'{self.client.base_url}{self.base_path}.reset_work_time',
                        method='POST',
                        headers=self.client.headers,
                        data=json.dumps(payload).encode('utf-8'),
                    )
                await self.client._respect_rate_limit(r)
                return BaseResponse.parse_raw(await r.content())

            async def reset_vacation_time(self, *, user_ids: List[int]) -> BaseResponse:
                payload = {
                    'user_ids': user_ids,
                }
                async with self.client.limiter:
                    r = await self.client.http.request(
                        url=f'{self.client.base_url}{self.base_path}.reset_vacation_time',
                        method='POST',
                        headers=self.client.headers,
                        data=json.dumps(payload).encode('utf-8'),
                    )
                await self.client._respect_rate_limit(r)
                return BaseResponse.parse_raw(await r.content())

        @property
        def users(self) -> Users:
            return self.Users(self)

    def __init__(self, *, app_key: str, base_url: Optional[str] = BASE_URL):
        self.app_key = app_key
        self.base_url = base_url
        self.http = aiosonic.HTTPClient()
        self.limiter = RateLimiter(capacity=0, refill_rate=60.0)

    async def _respect_rate_limit(self, response: aiosonic.HttpResponse) -> None:
        if 200 <= response.status_code < 300 and self.limiter.capacity <= 0:
            capacity = int(response.headers.get('ratelimit-limit', 0))
            self.limiter.reset(capacity=capacity)
        elif response.status_code == 429:
            capacity = int(response.headers.get('ratelimit-limit', 0))
            wait_time = int(response.headers.get('retry-after', 0))
            await asyncio.sleep(wait_time)
            self.limiter.reset(capacity=capacity)

    @property
    def headers(self) -> Dict[str, Any]:
        return {
            'Authorization': f'Bearer {self.app_key}',
            'Content-Type': 'application/json; charset=utf-8',
            'content-type': 'application/json; charset=utf-8',  # WORKAROUND: aiosonic does not support the Content-Type header camelcase format.
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

    @property
    def batch(self) -> Batch:
        return self.Batch(self)
