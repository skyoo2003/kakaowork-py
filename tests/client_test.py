import asyncio
from datetime import datetime

import pytest
import urllib3
import aiosonic
from pytz import utc
from pytest_mock import MockerFixture

from kakaowork.client import (Kakaowork, AsyncKakaowork)
from kakaowork.consts import (
    BASE_URL,
    BASE_PATH_USERS,
    BASE_PATH_CONVERSATIONS,
    BASE_PATH_MESSAGES,
    BASE_PATH_DEPARTMENTS,
    BASE_PATH_SPACES,
    BASE_PATH_BOTS,
)
from kakaowork.models import (
    ProfileNameFormat,
    ProfilePositionFormat,
    ConversationType,
    ColorTone,
    BotStatus,
    UserIdentificationField,
    UserField,
    ConversationField,
    MessageField,
    DepartmentField,
    SpaceField,
    BotField,
)
from kakaowork.utils import to_kst


# Workaround: Returns future if Python version less than 3.8, value otherwise.
# See https://stackoverflow.com/a/50031903
def _async_return(value):
    import sys
    if sys.version_info < (3, 8):
        f = asyncio.Future()
        f.set_result(value)
        return f
    else:
        return value


class TestKakaowork:
    def test_kakaowork_properties(self):
        c = Kakaowork(app_key='dummy')

        assert c.app_key == 'dummy'
        assert c.base_url == BASE_URL
        assert isinstance(c.http, urllib3.PoolManager)
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
    headers = {'Content-Type': 'applicaion/json: chartset=utf-8'}
    base_json = '{"success": true, "error": null}'
    user_json = ('{"success": true, "error": null, "user": {"id": 1234, "space_id": 12, "name": "name", '
                 '"identifications": [{"type": "email", "value": "user@localhost"}], "nickname": "nickname", "avatar_url": "http://localhost/image.png", '
                 '"department": "dep", "position": "position", "responsibility": "resp", "tels": [], "mobiles": [], "work_start_time": 1617889170, '
                 '"work_end_time": 1617889170, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}}')
    user_list_json = ('{"success": true, "error": null, "cursor": null, "users": [{"id": 1234, "space_id": 12, "name": "name", '
                      '"identifications": [{"type": "email", "value": "user@localhost"}], "nickname": "nickname", "avatar_url": "http://localhost/image.png", '
                      '"department": "dep", "position": "position", "responsibility": "resp", "tels": [], "mobiles": [], "work_start_time": 1617889170, '
                      '"work_end_time": 1617889170, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}]}')
    user_field = UserField(
        id=1234,
        space_id=12,
        identifications=[UserIdentificationField(type='email', value='user@localhost')],
        name='name',
        nickname='nickname',
        department='dep',
        position=ProfilePositionFormat.POSITION,
        responsibility='resp',
        tels=[],
        mobiles=[],
        avatar_url='http://localhost/image.png',
        work_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        work_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        vacation_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        vacation_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
    )

    def test_kakaowork_users_info(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.user_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.users.info(1)

        req.assert_called_once_with(
            'GET',
            'https://api.kakaowork.com/v1/users.info',
            fields={'user_id': 1},
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.user == self.user_field

    def test_kakaowork_users_find_by_email(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.user_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.users.find_by_email('user@domain.com')

        req.assert_called_once_with(
            'GET',
            'https://api.kakaowork.com/v1/users.find_by_email',
            fields={'email': 'user@domain.com'},
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.user == self.user_field

    def test_kakaowork_users_find_by_phone_number(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.user_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.users.find_by_phone_number('+82-10-1234-1234')

        req.assert_called_once_with(
            'GET',
            'https://api.kakaowork.com/v1/users.find_by_phone_number',
            fields={'phone_number': '+82-10-1234-1234'},
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.user == self.user_field

    def test_kakaowork_users_list(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.user_list_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.users.list(limit=1)

        req.assert_called_once_with(
            'GET',
            'https://api.kakaowork.com/v1/users.list',
            fields={'limit': '1'},
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.cursor is None
        assert ret.users == [self.user_field]

    def test_kakaowork_users_set_work_time(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.base_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.users.set_work_time(
            user_id=1,
            work_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            work_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        )

        req.assert_called_once_with(
            'POST',
            'https://api.kakaowork.com/v1/users.set_work_time',
            body=b'{"user_id": 1, "work_start_time": 1617889170, "work_end_time": 1617889170}',
        )
        assert ret.success is True
        assert ret.error is None

    def test_kakaowork_users_set_vacation_time(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.base_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.users.set_vacation_time(
            user_id=1,
            vacation_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            vacation_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        )

        req.assert_called_once_with(
            'POST',
            'https://api.kakaowork.com/v1/users.set_vacation_time',
            body=b'{"user_id": 1, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}',
        )
        assert ret.success is True
        assert ret.error is None


class TestKakaoworkConversations:
    headers = {'Content-Type': 'applicaion/json: chartset=utf-8'}
    base_json = '{"success": true, "error": null}'
    conversation_json = ('{"success": true, "error": null, "conversation": {"id": "1", "type": "dm", "users_count": 1, '
                         '"avatar_url": "http://localhost/image.png", "name": "name"}}')
    conversation_list_json = ('{"success": true, "error": null, "cursor": null, "conversations": [{"id": "1", "type": "dm", "users_count": 1, '
                              '"avatar_url": "http://localhost/image.png", "name": "name"}]}')
    user_list_json = ('{"success": true, "error": null, "cursor": null, "users": [{"id": 1234, "space_id": 12, "name": "name", '
                      '"identifications": [{"type": "email", "value": "user@localhost"}], "nickname": "nickname", "avatar_url": "http://localhost/image.png", '
                      '"department": "dep", "position": "position", "responsibility": "resp", "tels": [], "mobiles": [], "work_start_time": 1617889170, '
                      '"work_end_time": 1617889170, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}]}')
    conversation_field = ConversationField(
        id='1',
        name='name',
        type=ConversationType.DM,
        users_count=1,
        avatar_url='http://localhost/image.png',
    )
    user_field = UserField(
        id=1234,
        space_id=12,
        identifications=[UserIdentificationField(type='email', value='user@localhost')],
        name='name',
        nickname='nickname',
        department='dep',
        position=ProfilePositionFormat.POSITION,
        responsibility='resp',
        tels=[],
        mobiles=[],
        avatar_url='http://localhost/image.png',
        work_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        work_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        vacation_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        vacation_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
    )

    def test_kakaowork_conversations_open(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.conversation_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.conversations.open(user_ids=[1])

        req.assert_called_once_with('POST', 'https://api.kakaowork.com/v1/conversations.open', body=b'{"user_id": 1}')
        assert ret.success is True
        assert ret.error is None
        assert ret.conversation == self.conversation_field

    def test_kakaowork_conversations_list(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.conversation_list_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.conversations.list(limit=1)

        req.assert_called_once_with(
            'GET',
            'https://api.kakaowork.com/v1/conversations.list',
            fields={'limit': '1'},
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.cursor is None
        assert ret.conversations == [self.conversation_field]

    def test_kakaowork_conversations_users(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.user_list_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.conversations.users(conversation_id=1)

        req.assert_called_once_with(
            'GET',
            'https://api.kakaowork.com/v1/conversations/1/users',
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.users == [self.user_field]

    def test_kakaowork_conversations_invite(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.base_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.conversations.invite(conversation_id=1, user_ids=[1])

        req.assert_called_once_with(
            'POST',
            'https://api.kakaowork.com/v1/conversations/1/invite',
            body=b'{"user_ids": [1]}',
        )
        assert ret.success is True
        assert ret.error is None

    def test_kakaowork_conversations_kick(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.base_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.conversations.kick(conversation_id=1, user_ids=[1])

        req.assert_called_once_with(
            'POST',
            'https://api.kakaowork.com/v1/conversations/1/kick',
            body=b'{"user_ids": [1]}',
        )
        assert ret.success is True
        assert ret.error is None


class TestKakaoworkMessages:
    headers = {'Content-Type': 'applicaion/json: chartset=utf-8'}
    message_json = (
        '{"success": true, "error": null, '
        '"message": {"id": "1", "text": "msg", "user_id": "1", "conversation_id": 1, "send_time": 1617889170, "update_time": 1617889170, "blocks": null}}')
    message_field = MessageField(
        id='1',
        text='msg',
        user_id='1',
        conversation_id=1,
        send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        blocks=[],
    )

    def test_kakaowork_messages_send(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.message_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.messages.send(conversation_id=1, text='msg')

        req.assert_called_once_with(
            'POST',
            'https://api.kakaowork.com/v1/messages.send',
            body=b'{"conversation_id": 1, "text": "msg", "blocks": []}',
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.message == self.message_field


class TestKakaoworkDepartments:
    headers = {'Content-Type': 'applicaion/json: chartset=utf-8'}
    department_list_json = (
        '{"success": true, "error": null, "cursor": null, "departments": [{"id": "1", "ids_path": "1", "parent_id": "0", "space_id": "1", '
        '"name": "name", "code": "code", "user_count": 1, "has_child": false, "depth": 0, "users_ids": [1], "leader_ids": [1], "ancestry": ""}]}')
    department_field = DepartmentField(
        id='1',
        ids_path='1',
        parent_id='0',
        space_id='1',
        name='name',
        code='code',
        user_count=1,
        has_child=False,
        depth=0,
        users_ids=[1],
        leader_ids=[1],
        ancestry='',
    )

    def test_kakaowork_departments_list(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.department_list_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.departments.list(limit=1)

        req.assert_called_once_with(
            'GET',
            'https://api.kakaowork.com/v1/departments.list',
            fields={'limit': '1'},
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.cursor is None
        assert ret.departments == [self.department_field]


class TestKakaoworkSpaces:
    headers = {'Content-Type': 'applicaion/json: chartset=utf-8'}
    space_json = (
        '{"success": true, "error": null, "space": {"id": 1, "kakaoi_org_id": 1, "name": "name", "color_code": "default", "color_tone": "light", '
        '"permitted_ext": ["*"], "profile_name_format": "name_only", "profile_position_format": "position", "logo_url": "http://localhost/image.png"}}')
    space_field = SpaceField(
        id=1,
        kakaoi_org_id=1,
        name='name',
        color_code='default',
        color_tone=ColorTone.LIGHT,
        permitted_ext=['*'],
        profile_name_format=ProfileNameFormat.NAME_ONLY,
        profile_position_format=ProfilePositionFormat.POSITION,
        logo_url='http://localhost/image.png',
    )

    def test_kakaowork_spaces_info(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.space_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.spaces.info()

        req.assert_called_once_with(
            'GET',
            'https://api.kakaowork.com/v1/spaces.info',
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.space == self.space_field


class TestKakaoworkBots:
    headers = {'Content-Type': 'applicaion/json: chartset=utf-8'}
    bot_json = '{"success": true, "error": null, "info": {"bot_id": 1, "title": "bot", "status": "activated"}}'
    bot_field = BotField(
        bot_id=1,
        title='bot',
        status=BotStatus.ACTIVATED,
    )

    def test_kakaowork_bots_info(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.bot_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.bots.info()

        req.assert_called_once_with(
            'GET',
            'https://api.kakaowork.com/v1/bots.info',
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.info == self.bot_field


class TestAsyncKakaowork:
    @pytest.mark.asyncio
    async def test_async_kakaowork_properties(self):
        c = AsyncKakaowork(app_key='dummy')

        assert c.app_key == 'dummy'
        assert c.base_url == BASE_URL
        assert isinstance(c.http, aiosonic.HTTPClient)
        assert c.headers == {
            'Authorization': 'Bearer dummy',
            'Content-Type': 'application/json; charset=utf-8',
        }
        assert isinstance(c.users, AsyncKakaowork.Users)
        assert isinstance(c.conversations, AsyncKakaowork.Conversations)
        assert isinstance(c.messages, AsyncKakaowork.Messages)
        assert isinstance(c.departments, AsyncKakaowork.Departments)
        assert isinstance(c.spaces, AsyncKakaowork.Spaces)
        assert isinstance(c.bots, AsyncKakaowork.Bots)


class TestAsyncKakaoworkUsers:
    headers = {'Content-Type': 'applicaion/json: chartset=utf-8'}
    base_json = '{"success": true, "error": null}'
    user_json = ('{"success": true, "error": null, "user": {"id": 1234, "space_id": 12, "name": "name", '
                 '"identifications": [{"type": "email", "value": "user@localhost"}], "nickname": "nickname", "avatar_url": "http://localhost/image.png", '
                 '"department": "dep", "position": "position", "responsibility": "resp", "tels": [], "mobiles": [], "work_start_time": 1617889170, '
                 '"work_end_time": 1617889170, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}}')
    user_list_json = ('{"success": true, "error": null, "cursor": null, "users": [{"id": 1234, "space_id": 12, "name": "name", '
                      '"identifications": [{"type": "email", "value": "user@localhost"}], "nickname": "nickname", "avatar_url": "http://localhost/image.png", '
                      '"department": "dep", "position": "position", "responsibility": "resp", "tels": [], "mobiles": [], "work_start_time": 1617889170, '
                      '"work_end_time": 1617889170, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}]}')
    user_field = UserField(
        id=1234,
        space_id=12,
        identifications=[UserIdentificationField(type='email', value='user@localhost')],
        name='name',
        nickname='nickname',
        department='dep',
        position=ProfilePositionFormat.POSITION,
        responsibility='resp',
        tels=[],
        mobiles=[],
        avatar_url='http://localhost/image.png',
        work_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        work_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        vacation_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        vacation_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
    )

    @pytest.mark.asyncio
    async def test_async_kakaowork_users_info(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.user_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.users.info(1)

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/users.info',
            method='GET',
            headers=client.headers,
            params={'user_id': 1},
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.user == self.user_field

    @pytest.mark.asyncio
    async def test_async_kakaowork_users_find_by_email(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.user_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.users.find_by_email('user@domain.com')

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/users.find_by_email',
            method='GET',
            headers=client.headers,
            params={'email': 'user@domain.com'},
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.user == self.user_field

    @pytest.mark.asyncio
    async def test_kakaowork_users_find_by_phone_number(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.user_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.users.find_by_phone_number('+82-10-1234-1234')

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/users.find_by_phone_number',
            method='GET',
            headers=client.headers,
            params={'phone_number': '+82-10-1234-1234'},
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.user == self.user_field

    @pytest.mark.asyncio
    async def test_async_kakaowork_users_list(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.user_list_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.users.list(limit=1)

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/users.list',
            method='GET',
            headers=client.headers,
            params={'limit': '1'},
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.cursor is None
        assert ret.users == [self.user_field]

    @pytest.mark.asyncio
    async def test_async_kakaowork_users_set_work_time(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.base_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.users.set_work_time(
            user_id=1,
            work_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            work_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        )

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/users.set_work_time',
            method='POST',
            headers=client.headers,
            data=b'{"user_id": 1, "work_start_time": 1617889170, "work_end_time": 1617889170}',
        )
        assert ret.success is True
        assert ret.error is None

    @pytest.mark.asyncio
    async def test_async_kakaowork_users_set_vacation_time(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.base_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.users.set_vacation_time(
            user_id=1,
            vacation_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            vacation_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        )

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/users.set_vacation_time',
            method='POST',
            headers=client.headers,
            data=b'{"user_id": 1, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}',
        )
        assert ret.success is True
        assert ret.error is None


class TestAsyncKakaoworkConversations:
    headers = {'Content-Type': 'applicaion/json: chartset=utf-8'}
    base_json = '{"success": true, "error": null}'
    conversation_json = ('{"success": true, "error": null, "conversation": {"id": "1", "type": "dm", "users_count": 1, '
                         '"avatar_url": "http://localhost/image.png", "name": "name"}}')
    conversation_list_json = ('{"success": true, "error": null, "cursor": null, "conversations": [{"id": "1", "type": "dm", "users_count": 1, '
                              '"avatar_url": "http://localhost/image.png", "name": "name"}]}')
    user_list_json = ('{"success": true, "error": null, "cursor": null, "users": [{"id": 1234, "space_id": 12, "name": "name", '
                      '"identifications": [{"type": "email", "value": "user@localhost"}], "nickname": "nickname", "avatar_url": "http://localhost/image.png", '
                      '"department": "dep", "position": "position", "responsibility": "resp", "tels": [], "mobiles": [], "work_start_time": 1617889170, '
                      '"work_end_time": 1617889170, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}]}')
    conversation_field = ConversationField(
        id='1',
        name='name',
        type=ConversationType.DM,
        users_count=1,
        avatar_url='http://localhost/image.png',
    )
    user_field = UserField(
        id=1234,
        space_id=12,
        identifications=[UserIdentificationField(type='email', value='user@localhost')],
        name='name',
        nickname='nickname',
        department='dep',
        position=ProfilePositionFormat.POSITION,
        responsibility='resp',
        tels=[],
        mobiles=[],
        avatar_url='http://localhost/image.png',
        work_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        work_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        vacation_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        vacation_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
    )

    @pytest.mark.asyncio
    async def test_async_kakaowork_conversations_open(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.conversation_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.conversations.open(user_ids=[1])

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/conversations.open',
            method='POST',
            headers=client.headers,
            data=b'{"user_id": 1}',
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.conversation == self.conversation_field

    @pytest.mark.asyncio
    async def test_async_kakaowork_conversations_list(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.conversation_list_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.conversations.list(limit=1)

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/conversations.list',
            method='GET',
            headers=client.headers,
            params={'limit': '1'},
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.cursor is None
        assert ret.conversations == [self.conversation_field]

    @pytest.mark.asyncio
    async def test_async_kakaowork_conversations_users(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.user_list_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.conversations.users(conversation_id=1)

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/conversations/1/users',
            method='GET',
            headers=client.headers,
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.users == [self.user_field]

    @pytest.mark.asyncio
    async def test_async_kakaowork_conversations_invite(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.base_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.conversations.invite(conversation_id=1, user_ids=[1])

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/conversations/1/invite',
            method='POST',
            headers=client.headers,
            data=b'{"user_ids": [1]}',
        )
        assert ret.success is True
        assert ret.error is None

    @pytest.mark.asyncio
    async def test_async_kakaowork_conversations_kick(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.base_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.conversations.kick(conversation_id=1, user_ids=[1])

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/conversations/1/kick',
            method='POST',
            headers=client.headers,
            data=b'{"user_ids": [1]}',
        )
        assert ret.success is True
        assert ret.error is None


class TestAsyncKakaoworkMessages:
    headers = {'Content-Type': 'applicaion/json: chartset=utf-8'}
    message_json = (
        '{"success": true, "error": null, '
        '"message": {"id": "1", "text": "msg", "user_id": "1", "conversation_id": 1, "send_time": 1617889170, "update_time": 1617889170, "blocks": null}}')
    message_field = MessageField(
        id='1',
        text='msg',
        user_id='1',
        conversation_id=1,
        send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        blocks=[],
    )

    @pytest.mark.asyncio
    async def test_async_kakaowork_messages_send(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.message_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.messages.send(conversation_id=1, text='msg')

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/messages.send',
            method='POST',
            headers=client.headers,
            data=b'{"conversation_id": 1, "text": "msg", "blocks": []}',
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.message == self.message_field


class TestAsyncKakaoworkDepartments:
    headers = {'Content-Type': 'applicaion/json: chartset=utf-8'}
    department_list_json = (
        '{"success": true, "error": null, "cursor": null, "departments": [{"id": "1", "ids_path": "1", "parent_id": "0", "space_id": "1", '
        '"name": "name", "code": "code", "user_count": 1, "has_child": false, "depth": 0, "users_ids": [1], "leader_ids": [1], "ancestry": ""}]}')
    department_field = DepartmentField(
        id='1',
        ids_path='1',
        parent_id='0',
        space_id='1',
        name='name',
        code='code',
        user_count=1,
        has_child=False,
        depth=0,
        users_ids=[1],
        leader_ids=[1],
        ancestry='',
    )

    @pytest.mark.asyncio
    async def test_async_kakaowork_departments_list(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.department_list_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.departments.list(limit=1)

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/departments.list',
            method='GET',
            headers=client.headers,
            params={'limit': '1'},
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.cursor is None
        assert ret.departments == [self.department_field]


class TestAsyncKakaoworkSpaces:
    headers = {'Content-Type': 'applicaion/json: chartset=utf-8'}
    space_json = (
        '{"success": true, "error": null, "space": {"id": 1, "kakaoi_org_id": 1, "name": "name", "color_code": "default", "color_tone": "light", '
        '"permitted_ext": ["*"], "profile_name_format": "name_only", "profile_position_format": "position", "logo_url": "http://localhost/image.png"}}')
    space_field = SpaceField(
        id=1,
        kakaoi_org_id=1,
        name='name',
        color_code='default',
        color_tone=ColorTone.LIGHT,
        permitted_ext=['*'],
        profile_name_format=ProfileNameFormat.NAME_ONLY,
        profile_position_format=ProfilePositionFormat.POSITION,
        logo_url='http://localhost/image.png',
    )

    @pytest.mark.asyncio
    async def test_async_kakaowork_spaces_info(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.space_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.spaces.info()

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/spaces.info',
            method='GET',
            headers=client.headers,
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.space == self.space_field


class TestAsyncKakaoworkBots:
    headers = {'Content-Type': 'applicaion/json: chartset=utf-8'}
    bot_json = '{"success": true, "error": null, "info": {"bot_id": 1, "title": "bot", "status": "activated"}}'
    bot_field = BotField(
        bot_id=1,
        title='bot',
        status=BotStatus.ACTIVATED,
    )

    @pytest.mark.asyncio
    async def test_async_kakaowork_bots_info(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.bot_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.bots.info()

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/bots.info',
            method='GET',
            headers=client.headers,
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.info == self.bot_field
