import asyncio
from datetime import datetime
from contextlib import ExitStack as does_not_raise

import pytest
import urllib3
import aiosonic
from pytz import utc
from pytest_mock import MockerFixture

from kakaowork.client import (Kakaowork, AsyncKakaowork)
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
    WorkTimeField,
    VacationTimeField,
)
from kakaowork.utils import to_kst
from tests import _async_return


class TestKakaowork:
    def test_properties(self):
        c = Kakaowork(app_key='dummy')

        assert c.app_key == 'dummy'
        assert c.base_url == 'https://api.kakaowork.com'
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
        assert isinstance(c.batch, Kakaowork.Batch)


class TestKakaoworkUsers:
    headers = {'Content-Type': 'applicaion/json: chartset=utf-8'}
    base_json = '{"success": true, "error": null}'
    user_json = ('{"success": true, "error": null, "user": {"id": "1234", "space_id": "12", "name": "name", '
                 '"identifications": [{"type": "email", "value": "user@localhost"}], "nickname": "nickname", "avatar_url": "http://localhost/image.png", '
                 '"department": "dep", "position": "position", "responsibility": "resp", "tels": [], "mobiles": [], "work_start_time": 1617889170, '
                 '"work_end_time": 1617889170, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}}')
    user_list_json = ('{"success": true, "error": null, "cursor": null, "users": [{"id": "1234", "space_id": "12", "name": "name", '
                      '"identifications": [{"type": "email", "value": "user@localhost"}], "nickname": "nickname", "avatar_url": "http://localhost/image.png", '
                      '"department": "dep", "position": "position", "responsibility": "resp", "tels": [], "mobiles": [], "work_start_time": 1617889170, '
                      '"work_end_time": 1617889170, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}]}')
    user_field = UserField(
        id="1234",
        space_id="12",
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

    def test_properties(self):
        client = Kakaowork(app_key='dummy')
        assert client.users.client is client
        assert client.users.base_path == '/v1/users'

    def test_info(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.user_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.users.info(user_id=1)

        req.assert_called_once_with(
            'GET',
            'https://api.kakaowork.com/v1/users.info',
            fields={'user_id': 1},
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.user == self.user_field

    def test_find_by_email(self, mocker: MockerFixture):
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

    def test_find_by_phone_number(self, mocker: MockerFixture):
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

    @pytest.mark.parametrize(
        'kwargs,fields',
        [
            (dict(), {
                'limit': '10'
            }),
            (dict(limit=1), {
                'limit': '1'
            }),
            (dict(cursor='curr'), {
                'cursor': 'curr'
            }),
        ],
    )
    def test_list(self, kwargs, fields, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.user_list_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.users.list(**kwargs)

        req.assert_called_once_with(
            'GET',
            'https://api.kakaowork.com/v1/users.list',
            fields=fields,
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.cursor is None
        assert ret.users == [self.user_field]

    def test_set_work_time(self, mocker: MockerFixture):
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

    def test_set_vacation_time(self, mocker: MockerFixture):
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
    user_list_json = ('{"success": true, "error": null, "cursor": null, "users": [{"id": "1234", "space_id": "12", "name": "name", '
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
        id='1234',
        space_id='12',
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

    def test_properties(self):
        client = Kakaowork(app_key='dummy')
        assert client.conversations.client is client
        assert client.conversations.base_path == '/v1/conversations'

    @pytest.mark.parametrize(
        'kwargs,body',
        [
            (dict(user_ids=[1]), b'{"user_id": 1}'),
            (dict(user_ids=[1, 2]), b'{"user_ids": [1, 2]}'),
        ],
    )
    def test_open(self, kwargs, body, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.conversation_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.conversations.open(**kwargs)

        req.assert_called_once_with('POST', 'https://api.kakaowork.com/v1/conversations.open', body=body)
        assert ret.success is True
        assert ret.error is None
        assert ret.conversation == self.conversation_field

    @pytest.mark.parametrize(
        'kwargs,fields',
        [
            (dict(), {
                'limit': '10'
            }),
            (dict(limit=1), {
                'limit': '1'
            }),
            (dict(cursor='curr'), {
                'cursor': 'curr'
            }),
        ],
    )
    def test_list(self, kwargs, fields, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.conversation_list_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.conversations.list(**kwargs)

        req.assert_called_once_with(
            'GET',
            'https://api.kakaowork.com/v1/conversations.list',
            fields=fields,
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.cursor is None
        assert ret.conversations == [self.conversation_field]

    def test_users(self, mocker: MockerFixture):
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

    def test_invite(self, mocker: MockerFixture):
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

    def test_kick(self, mocker: MockerFixture):
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
        '"message": {"id": "1", "text": "msg", "user_id": "1", "conversation_id": 1, "send_time": 1617889170, "update_time": 1617889170, "blocks": []}}')
    message_field = MessageField(
        id='1',
        text='msg',
        user_id='1',
        conversation_id=1,
        send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        blocks=[],
    )

    def test_properties(self):
        client = Kakaowork(app_key='dummy')
        assert client.messages.client is client
        assert client.messages.base_path == '/v1/messages'

    @pytest.mark.parametrize(
        'kwargs,body',
        [
            (dict(conversation_id=1, text='msg'), b'{"conversation_id": 1, "text": "msg"}'),
            (dict(conversation_id=1, text='msg', blocks=[]), b'{"conversation_id": 1, "text": "msg", "blocks": []}'),
        ],
    )
    def test_send(self, kwargs, body, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.message_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.messages.send(**kwargs)

        req.assert_called_once_with(
            'POST',
            'https://api.kakaowork.com/v1/messages.send',
            body=body,
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.message == self.message_field

    @pytest.mark.parametrize(
        'kwargs,body,raises',
        [
            (dict(text='msg'), b'{"text": "msg"}', pytest.raises(ValueError)),
            (dict(text='msg', email='nobody@email.com'), b'{"email": "nobody@email.com", "text": "msg"}', does_not_raise()),
            (dict(text='msg', email='nobody@email.com', blocks=[]), b'{"email": "nobody@email.com", "text": "msg", "blocks": []}', does_not_raise()),
            (dict(text='msg', key='mykey'), b'{"key": "mykey", "text": "msg"}', does_not_raise()),
            (dict(text='msg', key='mykey', blocks=[]), b'{"key": "mykey", "text": "msg", "blocks": []}', does_not_raise()),
        ],
    )
    def test_send_by(self, kwargs, body, raises, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.message_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)

        with raises:
            ret = client.messages.send_by(**kwargs)

        if isinstance(raises, does_not_raise):
            req.assert_called_once_with(
                'POST',
                'https://api.kakaowork.com/v1/messages.send_by',
                body=body,
            )
            assert ret.success is True
            assert ret.error is None
            assert ret.message == self.message_field
        else:
            req.assert_not_called()

    @pytest.mark.parametrize(
        'kwargs,body',
        [
            (dict(text='msg', email='nobody@email.com'), b'{"email": "nobody@email.com", "text": "msg"}'),
            (dict(text='msg', email='nobody@email.com', blocks=[]), b'{"email": "nobody@email.com", "text": "msg", "blocks": []}'),
        ],
    )
    def test_send_by_email(self, kwargs, body, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.message_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.messages.send_by_email(**kwargs)

        req.assert_called_once_with(
            'POST',
            'https://api.kakaowork.com/v1/messages.send_by_email',
            body=body,
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

    def test_properties(self):
        client = Kakaowork(app_key='dummy')
        assert client.departments.client is client
        assert client.departments.base_path == '/v1/departments'

    @pytest.mark.parametrize(
        'kwargs,fields',
        [
            (dict(), {
                'limit': '10'
            }),
            (dict(limit=1), {
                'limit': '1'
            }),
            (dict(cursor='curr'), {
                'cursor': 'curr'
            }),
        ],
    )
    def test_list(self, kwargs, fields, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.department_list_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.departments.list(**kwargs)

        req.assert_called_once_with(
            'GET',
            'https://api.kakaowork.com/v1/departments.list',
            fields=fields,
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

    def test_properties(self):
        client = Kakaowork(app_key='dummy')
        assert client.spaces.client is client
        assert client.spaces.base_path == '/v1/spaces'

    def test_info(self, mocker: MockerFixture):
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

    def test_properties(self):
        client = Kakaowork(app_key='dummy')
        assert client.bots.client is client
        assert client.bots.base_path == '/v1/bots'

    def test_info(self, mocker: MockerFixture):
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


class TestKakaoworkBatch:
    headers = {'Content-Type': 'applicaion/json: chartset=utf-8'}
    base_json = '{"success": true}'

    def test_properties(self):
        client = Kakaowork(app_key='dummy')
        assert client.batch.client is client
        assert client.batch.base_path == '/v1/batch'

    def test_users_set_work_time(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.base_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.batch.users.set_work_time([
            WorkTimeField(
                user_id=1,
                work_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
                work_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            ),
        ])

        req.assert_called_once_with(
            'POST',
            'https://api.kakaowork.com/v1/batch/users.set_work_time',
            body=b'{"user_work_times": [{"user_id": 1, "work_start_time": 1617889170, "work_end_time": 1617889170}]}',
        )
        assert ret.success is True
        assert ret.error is None

    def test_users_set_vacation_time(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.base_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.batch.users.set_vacation_time([
            VacationTimeField(
                user_id=1,
                vacation_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
                vacation_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            ),
        ])

        req.assert_called_once_with(
            'POST',
            'https://api.kakaowork.com/v1/batch/users.set_vacation_time',
            body=b'{"user_vacation_times": [{"user_id": 1, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}]}',
        )
        assert ret.success is True
        assert ret.error is None

    def test_users_reset_work_time(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.base_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.batch.users.reset_work_time(user_ids=[1])

        req.assert_called_once_with(
            'POST',
            'https://api.kakaowork.com/v1/batch/users.reset_work_time',
            body=b'{"user_ids": [1]}',
        )
        assert ret.success is True
        assert ret.error is None

    def test_users_reset_vacation_time(self, mocker: MockerFixture):
        client = Kakaowork(app_key='dummy')
        resp = urllib3.HTTPResponse(
            body=self.base_json,
            status=200,
            headers=self.headers,
        )
        req = mocker.patch('urllib3.PoolManager.request', return_value=resp)
        ret = client.batch.users.reset_vacation_time(user_ids=[1])

        req.assert_called_once_with(
            'POST',
            'https://api.kakaowork.com/v1/batch/users.reset_vacation_time',
            body=b'{"user_ids": [1]}',
        )
        assert ret.success is True
        assert ret.error is None


class TestAsyncKakaowork:
    @pytest.mark.asyncio
    async def test_async_kakaowork_properties(self):
        c = AsyncKakaowork(app_key='dummy')

        assert c.app_key == 'dummy'
        assert c.base_url == 'https://api.kakaowork.com'
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
        assert isinstance(c.batch, AsyncKakaowork.Batch)


class TestAsyncKakaoworkUsers:
    headers = {'Content-Type': 'applicaion/json: chartset=utf-8'}
    base_json = '{"success": true, "error": null}'
    user_json = ('{"success": true, "error": null, "user": {"id": "1234", "space_id": "12", "name": "name", '
                 '"identifications": [{"type": "email", "value": "user@localhost"}], "nickname": "nickname", "avatar_url": "http://localhost/image.png", '
                 '"department": "dep", "position": "position", "responsibility": "resp", "tels": [], "mobiles": [], "work_start_time": 1617889170, '
                 '"work_end_time": 1617889170, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}}')
    user_list_json = ('{"success": true, "error": null, "cursor": null, "users": [{"id": "1234", "space_id": "12", "name": "name", '
                      '"identifications": [{"type": "email", "value": "user@localhost"}], "nickname": "nickname", "avatar_url": "http://localhost/image.png", '
                      '"department": "dep", "position": "position", "responsibility": "resp", "tels": [], "mobiles": [], "work_start_time": 1617889170, '
                      '"work_end_time": 1617889170, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}]}')
    user_field = UserField(
        id='1234',
        space_id='12',
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

    def test_properties(self):
        client = AsyncKakaowork(app_key='dummy')
        assert client.users.client is client
        assert client.users.base_path == '/v1/users'

    @pytest.mark.asyncio
    async def test_info(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.user_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.users.info(user_id=1)

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
    async def test_find_by_email(self, mocker: MockerFixture):
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
    async def test_find_by_phone_number(self, mocker: MockerFixture):
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
    @pytest.mark.parametrize(
        'kwargs,params',
        [
            (dict(), {
                'limit': '10'
            }),
            (dict(limit=1), {
                'limit': '1'
            }),
            (dict(cursor='curr'), {
                'cursor': 'curr'
            }),
        ],
    )
    async def test_list(self, kwargs, params, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.user_list_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.users.list(**kwargs)

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/users.list',
            method='GET',
            headers=client.headers,
            params=params,
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.cursor is None
        assert ret.users == [self.user_field]

    @pytest.mark.asyncio
    async def test_set_work_time(self, mocker: MockerFixture):
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
    async def test_set_vacation_time(self, mocker: MockerFixture):
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
    user_list_json = ('{"success": true, "error": null, "cursor": null, "users": [{"id": "1234", "space_id": "12", "name": "name", '
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
        id='1234',
        space_id='12',
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

    def test_properties(self):
        client = AsyncKakaowork(app_key='dummy')
        assert client.conversations.client is client
        assert client.conversations.base_path == '/v1/conversations'

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'kwargs,data',
        [
            (dict(user_ids=[1]), b'{"user_id": 1}'),
            (dict(user_ids=[1, 2]), b'{"user_ids": [1, 2]}'),
        ],
    )
    async def test_open(self, kwargs, data, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.conversation_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.conversations.open(**kwargs)

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/conversations.open',
            method='POST',
            headers=client.headers,
            data=data,
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.conversation == self.conversation_field

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'kwargs,params',
        [
            (dict(), {
                'limit': '10'
            }),
            (dict(limit=1), {
                'limit': '1'
            }),
            (dict(cursor='curr'), {
                'cursor': 'curr'
            }),
        ],
    )
    async def test_list(self, kwargs, params, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.conversation_list_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.conversations.list(**kwargs)

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/conversations.list',
            method='GET',
            headers=client.headers,
            params=params,
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.cursor is None
        assert ret.conversations == [self.conversation_field]

    @pytest.mark.asyncio
    async def test_users(self, mocker: MockerFixture):
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
    async def test_invite(self, mocker: MockerFixture):
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
    async def test_kick(self, mocker: MockerFixture):
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
        '"message": {"id": "1", "text": "msg", "user_id": "1", "conversation_id": 1, "send_time": 1617889170, "update_time": 1617889170, "blocks": []}}')
    message_field = MessageField(
        id='1',
        text='msg',
        user_id='1',
        conversation_id=1,
        send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        blocks=[],
    )

    def test_properties(self):
        client = AsyncKakaowork(app_key='dummy')
        assert client.messages.client is client
        assert client.messages.base_path == '/v1/messages'

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'kwargs,data',
        [
            (dict(conversation_id=1, text='msg'), b'{"conversation_id": 1, "text": "msg"}'),
            (dict(conversation_id=1, text='msg', blocks=[]), b'{"conversation_id": 1, "text": "msg", "blocks": []}'),
        ],
    )
    async def test_send(self, kwargs, data, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.message_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.messages.send(**kwargs)

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/messages.send',
            method='POST',
            headers=client.headers,
            data=data,
        )
        assert ret.success is True
        assert ret.error is None
        assert ret.message == self.message_field

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'kwargs,data,raises',
        [
            (dict(text='msg'), b'{"text": "msg"}', pytest.raises(ValueError)),
            (dict(text='msg', email='nobody@email.com'), b'{"email": "nobody@email.com", "text": "msg"}', does_not_raise()),
            (dict(text='msg', email='nobody@email.com', blocks=[]), b'{"email": "nobody@email.com", "text": "msg", "blocks": []}', does_not_raise()),
            (dict(text='msg', key='mykey'), b'{"key": "mykey", "text": "msg"}', does_not_raise()),
            (dict(text='msg', key='mykey', blocks=[]), b'{"key": "mykey", "text": "msg", "blocks": []}', does_not_raise()),
        ],
    )
    async def test_send_by(self, kwargs, data, raises, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.message_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))

        with raises:
            ret = await client.messages.send_by(**kwargs)

        if isinstance(raises, does_not_raise):
            req.assert_called_once_with(
                url='https://api.kakaowork.com/v1/messages.send_by',
                method='POST',
                headers=client.headers,
                data=data,
            )
            assert ret.success is True
            assert ret.error is None
            assert ret.message == self.message_field
        else:
            req.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'kwargs,data',
        [
            (dict(text='msg', email='nobody@email.com'), b'{"email": "nobody@email.com", "text": "msg"}'),
            (dict(text='msg', email='nobody@email.com', blocks=[]), b'{"email": "nobody@email.com", "text": "msg", "blocks": []}'),
        ],
    )
    async def test_send_by_email(self, kwargs, data, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.message_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.messages.send_by_email(**kwargs)

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/messages.send_by_email',
            method='POST',
            headers=client.headers,
            data=data,
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

    def test_properties(self):
        client = AsyncKakaowork(app_key='dummy')
        assert client.departments.client is client
        assert client.departments.base_path == '/v1/departments'

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'kwargs,params',
        [
            (dict(), {
                'limit': '10'
            }),
            (dict(limit=1), {
                'limit': '1'
            }),
            (dict(cursor='curr'), {
                'cursor': 'curr'
            }),
        ],
    )
    async def test_list(self, kwargs, params, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.department_list_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.departments.list(**kwargs)

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/departments.list',
            method='GET',
            headers=client.headers,
            params=params,
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

    def test_properties(self):
        client = AsyncKakaowork(app_key='dummy')
        assert client.spaces.client is client
        assert client.spaces.base_path == '/v1/spaces'

    @pytest.mark.asyncio
    async def test_info(self, mocker: MockerFixture):
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

    def test_properties(self):
        client = AsyncKakaowork(app_key='dummy')
        assert client.bots.client is client
        assert client.bots.base_path == '/v1/bots'

    @pytest.mark.asyncio
    async def test_info(self, mocker: MockerFixture):
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


class TestAsyncKakaoworkBatch:
    headers = {'Content-Type': 'applicaion/json: chartset=utf-8'}
    base_json = '{"success": true}'

    def test_properties(self):
        client = AsyncKakaowork(app_key='dummy')
        assert client.batch.client is client
        assert client.batch.base_path == '/v1/batch'

    @pytest.mark.asyncio
    async def test_users_set_work_time(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.base_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.batch.users.set_work_time([
            WorkTimeField(
                user_id=1,
                work_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
                work_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            ),
        ])

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/batch/users.set_work_time',
            method='POST',
            headers=client.headers,
            data=b'{"user_work_times": [{"user_id": 1, "work_start_time": 1617889170, "work_end_time": 1617889170}]}',
        )
        assert ret.success is True
        assert ret.error is None

    @pytest.mark.asyncio
    async def test_users_set_vacation_time(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.base_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.batch.users.set_vacation_time([
            VacationTimeField(
                user_id=1,
                vacation_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
                vacation_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            ),
        ])

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/batch/users.set_vacation_time',
            method='POST',
            headers=client.headers,
            data=b'{"user_vacation_times": [{"user_id": 1, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}]}',
        )
        assert ret.success is True
        assert ret.error is None

    @pytest.mark.asyncio
    async def test_users_reset_work_time(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.base_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.batch.users.reset_work_time(user_ids=[1])

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/batch/users.reset_work_time',
            method='POST',
            headers=client.headers,
            data=b'{"user_ids": [1]}',
        )
        assert ret.success is True
        assert ret.error is None

    @pytest.mark.asyncio
    async def test_users_reset_vacation_time(self, mocker: MockerFixture):
        client = AsyncKakaowork(app_key='dummy')
        resp = aiosonic.HttpResponse()
        resp.body = self.base_json.encode('utf-8')
        resp.response_initial = {'version': 1.1, 'code': 200, 'reason': 'OK'}
        resp.headers.update(self.headers)
        req = mocker.patch('aiosonic.HTTPClient.request', return_value=_async_return(resp))
        ret = await client.batch.users.reset_vacation_time(user_ids=[1])

        req.assert_called_once_with(
            url='https://api.kakaowork.com/v1/batch/users.reset_vacation_time',
            method='POST',
            headers=client.headers,
            data=b'{"user_ids": [1]}',
        )
        assert ret.success is True
        assert ret.error is None
