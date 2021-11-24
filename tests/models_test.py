import warnings
from datetime import datetime, timezone

import pytest
from pytz import utc
from pydantic import ValidationError

from kakaowork.blockkit import (
    BlockType,
    TextBlock,
)
from kakaowork.models import (
    ErrorCode,
    ConversationType,
    ColorTone,
    ProfileNameFormat,
    ProfilePositionFormat,
    BotStatus,
    ErrorField,
    UserIdentificationField,
    UserField,
    ConversationField,
    MessageField,
    DepartmentField,
    SpaceField,
    BotField,
    ReactiveType,
    BaseReactiveBody,
    SubmitActionReactiveBody,
    SubmitModalReactiveBody,
    RequestModalReactiveBody,
    ModalReactiveView,
    RequestModalReactiveResponse,
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
from kakaowork.utils import to_kst


class TestErrorCode:
    def test_missing(self):
        assert ErrorCode('####') == ErrorCode.UNKNOWN


class TestErrorField:
    def test_to_dict(self):
        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert error.dict(exclude_none=True) == {'code': 'api_not_found', 'message': 'api not found'}

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            ErrorField(**{})

        with pytest.raises(ValidationError):
            ErrorField(**{'code': 'api_not_found'})

        with pytest.raises(ValidationError):
            ErrorField(**{'message': 'api not found'})

        assert ErrorField(**{
            'code': 'api_not_found',
            'message': 'api not found',
        }) == ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')

        assert ErrorField(**{
            'code': '???',
            'message': 'unknown error',
        }) == ErrorField(code=ErrorCode.UNKNOWN, message='unknown error')


class TestUserIdentificationField:
    def test_to_dict(self):
        uid = UserIdentificationField(type='gmail', value='user@localhost')
        assert uid.dict(exclude_none=True) == {'type': 'gmail', 'value': 'user@localhost'}

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            UserIdentificationField(**{})

        with pytest.raises(ValidationError):
            UserIdentificationField(**{'type': 'gmail'})

        with pytest.raises(ValidationError):
            UserIdentificationField(**{'value': 'user@localhost'})

        assert UserIdentificationField(**{
            'type': 'gmail',
            'value': 'user@localhost',
        }) == UserIdentificationField(type='gmail', value='user@localhost')


class TestUserField:
    def test_to_dict(self):
        user = UserField(
            id='1234',
            space_id='123',
            name='noname',
            display_name='dpname',
            identifications=[UserIdentificationField(type='email', value='user@localhost')],
            nickname='nm',
            avatar_url='http://localhost/image.png',
            department='dp',
            position='ps',
            responsibility='leader',
            tels=['123-123-123'],
            mobiles=['123-123-123'],
            work_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            work_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            vacation_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            vacation_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        )
        assert user.dict(exclude_none=True) == {
            'id': '1234',
            'space_id': '123',
            'name': 'noname',
            'display_name': 'dpname',
            'identifications': [{
                'type': 'email',
                'value': 'user@localhost'
            }],
            'nickname': 'nm',
            'avatar_url': 'http://localhost/image.png',
            'department': 'dp',
            'position': 'ps',
            'responsibility': 'leader',
            'tels': ['123-123-123'],
            'mobiles': ['123-123-123'],
            'work_start_time': to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            'work_end_time': to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            'vacation_start_time': to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            'vacation_end_time': to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        }

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            UserField(**{})

        data = {
            'avatar_url': None,
            'department': 'test',
            'id': '1234',
            'identifications': [{
                'type': 'email',
                'value': 'user@localhost'
            }],
            'mobiles': [],
            'name': 'noname',
            'nickname': None,
            'position': None,
            'responsibility': 'leader',
            'space_id': '123',
            'tels': [],
            'vacation_end_time': 1617889170,
            'vacation_start_time': 1617889170,
            'work_end_time': 1617889170,
            'work_start_time': 1617889170,
        }
        assert UserField(**data) == UserField(
            avatar_url=None,
            department='test',
            id='1234',
            identifications=[UserIdentificationField(type='email', value='user@localhost')],
            mobiles=[],
            name='noname',
            nickname=None,
            position=None,
            responsibility='leader',
            space_id='123',
            tels=[],
            vacation_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            vacation_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            work_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            work_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        )

        data = {
            'avatar_url': None,
            'department': 'test',
            'id': '1234',
            'identifications': [{
                'type': 'email',
                'value': 'user@localhost'
            }],
            'mobiles': [],
            'name': 'noname',
            'nickname': None,
            'position': None,
            'responsibility': 'leader',
            'space_id': '123',
            'tels': [],
            'vacation_end_time': '2021-04-08T22:39:30+09:00',
            'vacation_start_time': '2021-04-08T22:39:30+09:00',
            'work_end_time': '2021-04-08T22:39:30+09:00',
            'work_start_time': '2021-04-08T22:39:30+09:00',
        }
        assert UserField(**data) == UserField(
            avatar_url=None,
            department='test',
            id='1234',
            identifications=[UserIdentificationField(type='email', value='user@localhost')],
            mobiles=[],
            name='noname',
            nickname=None,
            position=None,
            responsibility='leader',
            space_id='123',
            tels=[],
            vacation_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            vacation_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            work_end_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            work_start_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
        )


class TestConversationField:
    def test_to_dict(self):
        conversation = ConversationField(
            id='1',
            type=ConversationType.DM,
            users_count=2,
            avatar_url='http://localhost/image.png',
            name='noname',
        )
        assert conversation.dict(exclude_none=True) == {
            'id': '1',
            'type': 'dm',
            'users_count': 2,
            'avatar_url': 'http://localhost/image.png',
            'name': 'noname',
        }

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            ConversationField(**{})

        assert ConversationField(**{
            'id': '1',
            'type': 'dm',
            'users_count': 2,
            'avatar_url': None,
            'name': 'noname',
        }) == ConversationField(
            id='1',
            type=ConversationType.DM,
            users_count=2,
            avatar_url=None,
            name='noname',
        )


class TestMessageField:
    def test_to_dict(self):
        message = MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )
        assert message.dict(exclude_none=True) == {
            'id': '123',
            'text': 'msg',
            'user_id': '1',
            'conversation_id': 1,
            'send_time': to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            'update_time': to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            'blocks': [{
                'type': 'text',
                'text': 'block',
                'markdown': False,
            }]
        }

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            MessageField(**{})

        data = {
            'id': '123',
            'text': 'msg',
            'user_id': '1',
            'conversation_id': 1,
            'send_time': 1617889170,
            'update_time': 1617889170,
            'blocks': [{
                'type': 'text',
                'text': 'block',
                'markdown': False,
            }],
        }
        assert MessageField(**data) == MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )

        data = {
            'id': '123',
            'text': 'msg',
            'user_id': '1',
            'conversation_id': 1,
            'send_time': '2021-04-08T22:39:30+09:00',
            'update_time': '2021-04-08T22:39:30+09:00',
            'blocks': [{
                'type': 'text',
                'text': 'block',
                'markdown': False,
            }],
        }
        assert MessageField(**data) == MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )


class TestDepartmentField:
    def test_to_dict(self):
        department = DepartmentField(
            id='1',
            ids_path='1',
            parent_id='',
            space_id='1',
            name='dep',
            code='depcode',
            user_count=1,
            has_child=False,
            depth=0,
            users_ids=[1],
            leader_ids=[1],
            ancestry='',
        )
        assert department.dict(exclude_none=True) == {
            'id': '1',
            'ids_path': '1',
            'parent_id': '',
            'space_id': '1',
            'name': 'dep',
            'code': 'depcode',
            'user_count': 1,
            'has_child': False,
            'depth': 0,
            'users_ids': [1],
            'leader_ids': [1],
            'ancestry': '',
        }

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            DepartmentField(**{})

        data = {
            'id': '1',
            'ids_path': '1',
            'parent_id': '',
            'space_id': '1',
            'name': 'dep',
            'code': 'depcode',
            'user_count': 1,
            'has_child': False,
            'depth': 0,
            'users_ids': [1],
            'leader_ids': [1],
            'ancestry': '',
        }
        assert DepartmentField(**data) == DepartmentField(
            id='1',
            ids_path='1',
            parent_id='',
            space_id='1',
            name='dep',
            code='depcode',
            user_count=1,
            has_child=False,
            depth=0,
            users_ids=[1],
            leader_ids=[1],
            ancestry='',
        )


class TestSpaceField:
    def test_to_dict(self):
        space = SpaceField(
            id=1,
            kakaoi_org_id=1,
            name='space',
            color_code='default',
            color_tone=ColorTone.LIGHT,
            permitted_ext=['*'],
            profile_name_format=ProfileNameFormat.NAME_ONLY,
            profile_position_format=ProfilePositionFormat.POSITION,
            logo_url='http://localhost/image.png',
        )
        assert space.dict(exclude_none=True) == {
            'id': 1,
            'kakaoi_org_id': 1,
            'name': 'space',
            'color_code': 'default',
            'color_tone': 'light',
            'permitted_ext': ['*'],
            'profile_name_format': 'name_only',
            'profile_position_format': 'position',
            'logo_url': 'http://localhost/image.png',
        }

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            SpaceField(**{})

        data = {
            'id': 1,
            'kakaoi_org_id': 1,
            'name': 'space',
            'color_code': 'default',
            'color_tone': 'light',
            'permitted_ext': ['*'],
            'profile_name_format': 'name_only',
            'profile_position_format': 'position',
            'logo_url': 'http://localhost/image.png',
        }
        assert SpaceField(**data) == SpaceField(
            id=1,
            kakaoi_org_id=1,
            name='space',
            color_code='default',
            color_tone=ColorTone.LIGHT,
            permitted_ext=['*'],
            profile_name_format=ProfileNameFormat.NAME_ONLY,
            profile_position_format=ProfilePositionFormat.POSITION,
            logo_url='http://localhost/image.png',
        )


class TestBotField:
    def test_to_dict(self):
        bot = BotField(
            bot_id=1,
            title='bot',
            status=BotStatus.ACTIVATED,
        )
        assert bot.dict(exclude_none=True) == {
            'bot_id': 1,
            'title': 'bot',
            'status': 'activated',
        }

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            BotField(**{})

        assert BotField(**{
            'bot_id': 1,
            'title': 'bot',
            'status': 'activated',
        }) == BotField(
            bot_id=1,
            title='bot',
            status=BotStatus.ACTIVATED,
        )


class TestBaseReactiveBody:
    def test_properties(self):
        message = MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )
        body = BaseReactiveBody(type=ReactiveType.SUBMIT_MODAL, action_time="2021-01-01", message=message, value='value')
        assert body.type == ReactiveType.SUBMIT_MODAL
        assert body.action_time == '2021-01-01'
        assert body.message == message
        assert body.value == 'value'

    def test_to_json(self):
        message = MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )
        body = BaseReactiveBody(type=ReactiveType.SUBMIT_MODAL, action_time="2021-01-01", message=message, value='value')
        assert body.json(exclude_none=True) == ('{"type": "submission", "action_time": "2021-01-01", "message": {"id": "123", "text": "msg", "user_id": "1"'
                                                ', "conversation_id": 1, "send_time": 1617889170, "update_time": 1617889170, "blocks": [{"type": "text", '
                                                '"text": "block", "markdown": false}]}, "value": "value"}')

    def test_to_dict(self):
        message = MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )
        body = BaseReactiveBody(type=ReactiveType.SUBMIT_MODAL, action_time="2021-01-01", message=message, value='value')
        assert body.dict(exclude_none=True) == {
            'type': ReactiveType.SUBMIT_MODAL,
            'action_time': '2021-01-01',
            'message': {
                'id': '123',
                'text': 'msg',
                'user_id': '1',
                'conversation_id': 1,
                'send_time': to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
                'update_time': to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
                'blocks': [{
                    'type': BlockType.TEXT,
                    'text': 'block',
                    'markdown': False
                }],
            },
            'value': 'value'
        }

    def test_from_json(self):
        json_str = ('{"type": "submission", "action_time": "2021-01-01", "message": {"id": "123", "text": "msg", "user_id": "1"'
                    ', "conversation_id": 1, "send_time": 1617889170, "update_time": 1617889170, "blocks": [{"type": "text", '
                    '"text": "block", "markdown": false}]}, "value": "value"}')
        message = MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )
        body = BaseReactiveBody(type=ReactiveType.SUBMIT_MODAL, action_time="2021-01-01", message=message, value='value')
        assert BaseReactiveBody.parse_raw(json_str) == body


class TestSubmitActionReactiveBody:
    def test_properties(self):
        message = MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )
        body = SubmitActionReactiveBody(action_time="2021-01-01", message=message, value='value', action_name='name', react_user_id=1)
        assert body.type == ReactiveType.SUBMIT_ACTION
        assert body.action_time == '2021-01-01'
        assert body.message == message
        assert body.value == 'value'
        assert body.action_name == 'name'
        assert body.react_user_id == 1

    def test_to_json(self):
        message = MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )
        body = SubmitActionReactiveBody(action_time="2021-01-01", message=message, value='value', action_name='name', react_user_id=1)
        assert body.json(exclude_none=True) == ('{"type": "submit_action", "action_time": "2021-01-01", "message": {"id": "123", "text": "msg", "user_id": '
                                                '"1", "conversation_id": 1, "send_time": 1617889170, "update_time": 1617889170, "blocks": [{"type": "text", '
                                                '"text": "block", "markdown": false}]}, "value": "value", "action_name": "name", "react_user_id": 1}')

    def test_to_dict(self):
        message = MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )
        body = SubmitActionReactiveBody(action_time="2021-01-01", message=message, value='value', action_name='name', react_user_id=1)
        assert body.dict(exclude_none=True) == {
            'type': ReactiveType.SUBMIT_ACTION,
            'action_time': '2021-01-01',
            'message': {
                'id': '123',
                'text': 'msg',
                'user_id': '1',
                'conversation_id': 1,
                'send_time': to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
                'update_time': to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
                'blocks': [{
                    'type': BlockType.TEXT,
                    'text': 'block',
                    'markdown': False
                }]
            },
            'value': 'value',
            'action_name': 'name',
            'react_user_id': 1
        }

    def test_from_json(self):
        json_str = ('{"type": "submit_action", "action_time": "2021-01-01", "message": {"id": "123", "text": "msg", "user_id": '
                    '"1", "conversation_id": 1, "send_time": 1617889170, "update_time": 1617889170, "blocks": [{"type": "text",'
                    '"text": "block", "markdown": false}]}, "value": "value", "action_name": "name", "react_user_id": 1}')
        message = MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )
        body = SubmitActionReactiveBody(action_time="2021-01-01", message=message, value='value', action_name='name', react_user_id=1)
        assert SubmitActionReactiveBody.parse_raw(json_str) == body


class TestSubmitModalReactiveBody:
    def test_properties(self):
        message = MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )
        body = SubmitModalReactiveBody(action_time="2021-01-01", message=message, value='value', actions={'key': 'value'}, react_user_id=1)
        assert body.type == ReactiveType.SUBMIT_MODAL
        assert body.action_time == '2021-01-01'
        assert body.message == message
        assert body.value == 'value'
        assert body.actions == {'key': 'value'}
        assert body.react_user_id == 1

    def test_to_json(self):
        message = MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )
        body = SubmitModalReactiveBody(action_time="2021-01-01", message=message, value='value', actions={'key': 'value'}, react_user_id=1)
        assert body.json(exclude_none=True) == ('{"type": "submission", "action_time": "2021-01-01", "message": {"id": "123", "text": "msg", "user_id": "1"'
                                                ', "conversation_id": 1, "send_time": 1617889170, "update_time": 1617889170, "blocks": [{"type": "text", '
                                                '"text": "block", "markdown": false}]}, "value": "value", "actions": {"key": "value"}, "react_user_id": 1}')

    def test_to_dict(self):
        message = MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )
        body = SubmitModalReactiveBody(action_time="2021-01-01", message=message, value='value', actions={'key': 'value'}, react_user_id=1)
        assert body.dict(exclude_none=True) == {
            'type': ReactiveType.SUBMIT_MODAL,
            'action_time': '2021-01-01',
            'message': {
                'id': '123',
                'text': 'msg',
                'user_id': '1',
                'conversation_id': 1,
                'send_time': to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
                'update_time': to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
                'blocks': [{
                    'type': BlockType.TEXT,
                    'text': 'block',
                    'markdown': False,
                }]
            },
            'value': 'value',
            'actions': {
                'key': 'value',
            },
            'react_user_id': 1,
        }

    def test_from_json(self):
        json_str = ('{"type": "submission", "action_time": "2021-01-01", "message": {"id": "123", "text": "msg", "user_id": "1"'
                    ', "conversation_id": 1, "send_time": 1617889170, "update_time": 1617889170, "blocks": [{"type": "text", '
                    '"text": "block", "markdown": false}]}, "value": "value", "actions": {"key": "value"}, "react_user_id": 1}')
        message = MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )
        body = SubmitModalReactiveBody(action_time="2021-01-01", message=message, value='value', actions={'key': 'value'}, react_user_id=1)
        assert SubmitModalReactiveBody.parse_raw(json_str) == body


class TestRequestModalReactiveBody:
    def test_properties(self):
        message = MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )
        body = RequestModalReactiveBody(action_time="2021-01-01", message=message, value='value', react_user_id=1)
        assert body.type == ReactiveType.REQUEST_MODAL
        assert body.action_time == '2021-01-01'
        assert body.message == message
        assert body.value == 'value'
        assert body.react_user_id == 1

    def test_to_json(self):
        message = MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )
        body = RequestModalReactiveBody(action_time="2021-01-01", message=message, value='value', react_user_id=1)
        assert body.json(exclude_none=True) == ('{"type": "request_modal", "action_time": "2021-01-01", "message": {"id": "123", "text": "msg", "user_id": '
                                                '"1", "conversation_id": 1, "send_time": 1617889170, "update_time": 1617889170, "blocks": [{"type": "text", '
                                                '"text": "block", "markdown": false}]}, "value": "value", "react_user_id": 1}')

    def test_to_dict(self):
        message = MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )
        body = RequestModalReactiveBody(action_time="2021-01-01", message=message, value='value', react_user_id=1)
        assert body.dict(exclude_none=True) == {
            'type': ReactiveType.REQUEST_MODAL,
            'action_time': '2021-01-01',
            'message': {
                'id': '123',
                'text': 'msg',
                'user_id': '1',
                'conversation_id': 1,
                'send_time': to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
                'update_time': to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
                'blocks': [{
                    'type': BlockType.TEXT,
                    'text': 'block',
                    'markdown': False,
                }]
            },
            'value': 'value',
            'react_user_id': 1,
        }

    def test_from_json(self):
        json_str = ('{"type": "request_modal", "action_time": "2021-01-01", "message": {"id": "123", "text": "msg", "user_id": '
                    '"1", "conversation_id": 1, "send_time": 1617889170, "update_time": 1617889170, "blocks": [{"type": "text", '
                    '"text": "block", "markdown": false}]}, "value": "value", "react_user_id": 1}')
        message = MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )
        body = RequestModalReactiveBody(action_time="2021-01-01", message=message, value='value', react_user_id=1)
        assert RequestModalReactiveBody.parse_raw(json_str) == body


class TestRequestModalReactiveResponse:
    def test_properties(self):
        view = ModalReactiveView(
            title='title',
            accept='accept',
            decline='decline',
            blocks=[TextBlock(text='block', markdown=False)],
            value='value',
        )
        res = RequestModalReactiveResponse(view=view)
        assert res.view == view

    def test_to_json(self):
        view = ModalReactiveView(
            title='title',
            accept='accept',
            decline='decline',
            blocks=[TextBlock(text='block', markdown=False)],
            value='value',
        )
        res = RequestModalReactiveResponse(view=view)
        assert res.json(exclude_none=True) == ('{"view": {"title": "title", "accept": "accept", "decline": "decline", "blocks": [{"type": "text", "text": '
                                               '"block", "markdown": false}], "value": "value"}}')

    def test_to_dict(self):
        view = ModalReactiveView(
            title='title',
            accept='accept',
            decline='decline',
            blocks=[TextBlock(text='block', markdown=False)],
            value='value',
        )
        res = RequestModalReactiveResponse(view=view)
        assert res.dict(exclude_none=True) == {
            'view': {
                'title': 'title',
                'accept': 'accept',
                'decline': 'decline',
                'blocks': [{
                    'type': 'text',
                    'text': 'block',
                    'markdown': False,
                }],
                'value': 'value',
            }
        }

    def test_from_json(self):
        json_str = ('{"view": {"title": "title", "accept": "accept", "decline": "decline", "blocks": [{"type": "text", "text": '
                    '"block", "markdown": false}], "value": "value"}}')
        view = ModalReactiveView(
            title='title',
            accept='accept',
            decline='decline',
            blocks=[TextBlock(text='block', markdown=False)],
            value='value',
        )
        res = RequestModalReactiveResponse(view=view)
        assert RequestModalReactiveResponse.parse_raw(json_str) == res


class TestBaseResponse:
    def test_properties(self):
        r = BaseResponse()
        assert r.success is True
        assert r.error is None

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = BaseResponse(success=False, error=error)
        assert r.success is False
        assert r.error == error

        r = BaseResponse(success=True)
        assert r.success is True
        assert r.error is None

    def test_to_json(self):
        r = BaseResponse()
        assert r.json(exclude_none=True) == '{"success": true}'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = BaseResponse(success=False, error=error)
        assert r.json(exclude_none=True) == '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}'

        r = BaseResponse(success=True)
        assert r.json(exclude_none=True) == '{"success": true}'

    def test_to_plain(self):
        r = BaseResponse()
        assert r.plain() == 'OK'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = BaseResponse(success=True, error=error)
        assert r.plain() == 'Error code:\tapi_not_found\nMessage:\tapi not found'

        r = BaseResponse(success=True)
        assert r.plain() == 'OK'

    def test_from_json(self):
        assert BaseResponse.parse_raw('{"success": true}') == BaseResponse(success=True, error=None)

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert BaseResponse.parse_raw('{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}') == BaseResponse(success=False,
                                                                                                                                            error=error)


class TestUserResponse:
    def test_properties(self):
        r = UserResponse()
        assert r.success is True
        assert r.error is None
        assert r.user is None

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = UserResponse(success=False, error=error)
        assert r.success is False
        assert r.error == error
        assert r.user is None

        user = UserField(
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
        r = UserResponse(success=True, user=user)
        assert r.success is True
        assert r.error is None
        assert r.user == user

    def test_to_json(self):
        r = UserResponse()
        assert r.json(exclude_none=True) == '{"success": true}'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = UserResponse(success=False, error=error)
        assert r.json(exclude_none=True) == '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}'

        user = UserField(
            id=1234,
            space_id=12,
            identifications=[UserIdentificationField(type='email', value='user@localhost')],
            name='name',
            display_name='dp',
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
        r = UserResponse(success=True, user=user)
        assert r.json(exclude_none=True) == (
            '{"success": true, "user": {"id": "1234", "space_id": "12", "name": "name", "display_name": "dp", '
            '"identifications": [{"type": "email", "value": "user@localhost"}], "nickname": "nickname", "avatar_url": "http://localhost/image.png", '
            '"department": "dep", "position": "position", "responsibility": "resp", "tels": [], "mobiles": [], "work_start_time": 1617889170, '
            '"work_end_time": 1617889170, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}}')

    def test_to_plain(self):
        r = UserResponse()
        assert r.plain() == 'OK'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = UserResponse(success=False, error=error)
        assert r.plain() == 'Error code:\tapi_not_found\nMessage:\tapi not found'

        user = UserField(
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
        r = UserResponse(success=True, user=user)
        assert r.plain() == (
            "ID:\t1234\nName:\tname\nNickname:\tnickname\nDepartment:\tdep\nPosition:\tposition\nResponsibility:\tresp\nTels:\t[]\nMobiles:\t[]\n"
            "Work start time:\t2021-04-08 22:39:30+09:00\nWork end time:\t2021-04-08 22:39:30+09:00\n"
            "Vacation start time:\t2021-04-08 22:39:30+09:00\nVacation end time:\t2021-04-08 22:39:30+09:00")

    def test_from_json(self):
        assert UserResponse.parse_raw('{"success": false, "error": null, "user": null}') == UserResponse(success=False, error=None, user=None)

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert UserResponse.parse_raw('{"success": true, "error": {"code": "api_not_found", "message": "api not found"}}') == UserResponse(success=True,
                                                                                                                                           error=error,
                                                                                                                                           user=None)

        user = UserField(
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
        json_str = ('{"success": true, "error": null, "user": {"id": 1234, "space_id": 12, "name": "name", '
                    '"identifications": [{"type": "email", "value": "user@localhost"}], "nickname": "nickname", "avatar_url": "http://localhost/image.png", '
                    '"department": "dep", "position": "position", "responsibility": "resp", "tels": [], "mobiles": [], "work_start_time": 1617889170, '
                    '"work_end_time": 1617889170, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}}')
        assert UserResponse.parse_raw(json_str) == UserResponse(success=True, error=None, user=user)


class TestUserListResponse:
    def test_properties(self):
        r = UserListResponse()
        assert r.success is True
        assert r.error is None
        assert r.cursor is None
        assert r.users is None

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = UserListResponse(success=False, error=error)
        assert r.success is False
        assert r.error == error
        assert r.cursor is None
        assert r.users is None

        user = UserField(
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
        r = UserListResponse(success=True, users=[user])
        assert r.success is True
        assert r.error is None
        assert r.cursor is None
        assert r.users == [user]

    def test_to_json(self):
        r = UserListResponse()
        assert r.json(exclude_none=True) == '{"success": true}'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = UserListResponse(success=False, error=error)
        assert r.json(exclude_none=True) == '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}'

        user = UserField(
            id='1234',
            space_id='12',
            identifications=[UserIdentificationField(type='email', value='user@localhost')],
            name='name',
            display_name='dp',
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
        r = UserListResponse(success=True, users=[user])
        assert r.json(exclude_none=True) == (
            '{"success": true, "users": [{"id": "1234", "space_id": "12", "name": "name", "display_name": "dp", '
            '"identifications": [{"type": "email", "value": "user@localhost"}], "nickname": "nickname", "avatar_url": "http://localhost/image.png", '
            '"department": "dep", "position": "position", "responsibility": "resp", "tels": [], "mobiles": [], "work_start_time": 1617889170, '
            '"work_end_time": 1617889170, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}]}')

    def test_to_plain(self):
        r = UserListResponse()
        assert r.plain() == 'OK'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = UserListResponse(success=False, error=error)
        assert r.plain() == 'Error code:\tapi_not_found\nMessage:\tapi not found'

        user = UserField(
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
        r = UserListResponse(success=True, users=[user])
        assert r.plain() == (
            "ID:\t1234\nName:\tname\nNickname:\tnickname\nDepartment:\tdep\nPosition:\tposition\nResponsibility:\tresp\nTels:\t[]\nMobiles:\t[]\n"
            "Work start time:\t2021-04-08 22:39:30+09:00\nWork end time:\t2021-04-08 22:39:30+09:00\n"
            "Vacation start time:\t2021-04-08 22:39:30+09:00\nVacation end time:\t2021-04-08 22:39:30+09:00")

    def test_from_json(self):
        assert UserListResponse.parse_raw('{"success": true}') == UserListResponse(success=True, error=None, cursor=None, users=None)

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert UserListResponse.parse_raw('{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}') == UserListResponse(
            success=False, error=error, cursor=None, users=None)

        user = UserField(
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
        json_str = ('{"success": true, "users": [{"id": 1234, "space_id": 12, "name": "name", '
                    '"identifications": [{"type": "email", "value": "user@localhost"}], "nickname": "nickname", "avatar_url": "http://localhost/image.png", '
                    '"department": "dep", "position": "position", "responsibility": "resp", "tels": [], "mobiles": [], "work_start_time": 1617889170, '
                    '"work_end_time": 1617889170, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}]}')
        assert UserListResponse.parse_raw(json_str) == UserListResponse(success=True, error=None, cursor=None, users=[user])


class TestConversationResponse:
    def test_properties(self):
        r = ConversationResponse()
        assert r.success is True
        assert r.error is None
        assert r.conversation is None

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = ConversationResponse(success=False, error=error)
        assert r.success is False
        assert r.error == error
        assert r.conversation is None

        conversation = ConversationField(
            id='1',
            name='name',
            type=ConversationType.DM,
            users_count=1,
            avatar_url='http://localhost/image.png',
        )
        r = ConversationResponse(success=True, conversation=conversation)
        assert r.success is True
        assert r.error is None
        assert r.conversation == conversation

    def test_to_json(self):
        r = ConversationResponse()
        assert r.json(exclude_none=True) == '{"success": true}'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = ConversationResponse(success=False, error=error)
        assert r.json(exclude_none=True) == '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}'

        conversation = ConversationField(
            id='1',
            name='name',
            type=ConversationType.DM,
            users_count=1,
            avatar_url='http://localhost/image.png',
        )
        r = ConversationResponse(success=True, conversation=conversation)
        assert r.json(exclude_none=True) == ('{"success": true, "conversation": {"id": "1", "type": "dm", "users_count": 1, '
                                             '"avatar_url": "http://localhost/image.png", "name": "name"}}')

    def test_to_plain(self):
        r = ConversationResponse()
        assert r.plain() == 'OK'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = ConversationResponse(success=False, error=error)
        assert r.plain() == 'Error code:\tapi_not_found\nMessage:\tapi not found'

        conversation = ConversationField(
            id='1',
            name='name',
            type=ConversationType.DM,
            users_count=1,
            avatar_url='http://localhost/image.png',
        )
        r = ConversationResponse(success=True, conversation=conversation)
        assert r.plain() == 'ID:\t1\nType:\tdm\nName:\tname\nAvatar URL:\thttp://localhost/image.png'

    def test_from_json(self):
        assert ConversationResponse.parse_raw('{"success": true}') == ConversationResponse(success=True, error=None, conversation=None)

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert ConversationResponse.parse_raw('{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}') == ConversationResponse(
            success=False, error=error, conversation=None)

        conversation = ConversationField(
            id='1',
            name='name',
            type=ConversationType.DM,
            users_count=1,
            avatar_url='http://localhost/image.png',
        )
        json_str = ('{"success": true, "conversation": {"id": "1", "type": "dm", "users_count": 1, '
                    '"avatar_url": "http://localhost/image.png", "name": "name"}}')
        assert ConversationResponse.parse_raw(json_str) == ConversationResponse(success=True, error=None, conversation=conversation)


class TestConversationListResponse:
    def test_properties(self):
        r = ConversationListResponse()
        assert r.success is True
        assert r.error is None
        assert r.conversations is None

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = ConversationListResponse(success=False, error=error)
        assert r.success is False
        assert r.error == error
        assert r.conversations is None

        conversation = ConversationField(
            id='1',
            name='name',
            type=ConversationType.DM,
            users_count=1,
            avatar_url='http://localhost/image.png',
        )
        r = ConversationListResponse(success=True, conversations=[conversation])
        assert r.success is True
        assert r.error is None
        assert r.conversations == [conversation]

    def test_to_json(self):
        r = ConversationListResponse()
        assert r.json(exclude_none=True) == '{"success": true}'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = ConversationListResponse(success=False, error=error)
        assert r.json(exclude_none=True) == '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}'

        conversation = ConversationField(
            id='1',
            name='name',
            type=ConversationType.DM,
            users_count=1,
            avatar_url='http://localhost/image.png',
        )
        r = ConversationListResponse(success=True, conversations=[conversation])
        assert r.json(exclude_none=True) == ('{"success": true, "conversations": [{"id": "1", "type": "dm", "users_count": 1, '
                                             '"avatar_url": "http://localhost/image.png", "name": "name"}]}')

    def test_to_plain(self):
        r = ConversationListResponse()
        assert r.plain() == 'OK'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = ConversationListResponse(success=False, error=error)
        assert r.plain() == 'Error code:\tapi_not_found\nMessage:\tapi not found'

        conversation = ConversationField(
            id='1',
            name='name',
            type=ConversationType.DM,
            users_count=1,
            avatar_url='http://localhost/image.png',
        )
        r = ConversationListResponse(success=True, conversations=[conversation])
        assert r.plain() == 'ID:\t1\nType:\tdm\nName:\tname\nAvatar URL:\thttp://localhost/image.png'

    def test_from_json(self):
        assert ConversationListResponse.parse_raw('{"success": true}') == ConversationListResponse(success=True, error=None, cursor=None, conversations=None)

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert ConversationListResponse.parse_raw(
            '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}') == ConversationListResponse(success=False,
                                                                                                                              error=error,
                                                                                                                              cursor=None,
                                                                                                                              conversations=None)

        conversation = ConversationField(
            id='1',
            name='name',
            type=ConversationType.DM,
            users_count=1,
            avatar_url='http://localhost/image.png',
        )
        json_str = ('{"success": true, "conversations": [{"id": "1", "type": "dm", "users_count": 1, '
                    '"avatar_url": "http://localhost/image.png", "name": "name"}]}')
        assert ConversationListResponse.parse_raw(json_str) == ConversationListResponse(success=True, error=None, cursor=None, conversations=[conversation])


class TestMessageResponse:
    def test_properties(self):
        r = MessageResponse()
        assert r.success is True
        assert r.error is None
        assert r.message is None

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = MessageResponse(success=False, error=error)
        assert r.success is False
        assert r.error == error
        assert r.message is None

        message = MessageField(
            id='1',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[],
        )
        r = MessageResponse(success=True, message=message)
        assert r.success is True
        assert r.error is None
        assert r.message == message

    def test_to_json(self):
        r = MessageResponse()
        assert r.json(exclude_none=True) == '{"success": true}'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = MessageResponse(success=False, error=error)
        assert r.json(exclude_none=True) == '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}'

        message = MessageField(
            id='1',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[],
        )
        r = MessageResponse(success=True, message=message)
        assert r.json(exclude_none=True) == ('{"success": true, "message": {"id": "1", "text": "msg", "user_id": "1", '
                                             '"conversation_id": 1, "send_time": 1617889170, "update_time": 1617889170, "blocks": []}}')

    def test_to_plain(self):
        r = MessageResponse()
        assert r.plain() == 'OK'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = MessageResponse(success=False, error=error)
        assert r.plain() == 'Error code:\tapi_not_found\nMessage:\tapi not found'

        message = MessageField(
            id='1',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[],
        )
        r = MessageResponse(success=True, message=message)
        assert r.plain() == ('ID:\t1\nConversation ID:\t1\n'
                             'Send time:\t2021-04-08 22:39:30+09:00\nUpdate time:\t2021-04-08 22:39:30+09:00\nText:\tmsg\nBlocks:\t-')

    def test_from_json(self):
        assert MessageResponse.parse_raw('{"success": true}') == MessageResponse(success=True, error=None, message=None)

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert MessageResponse.parse_raw('{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}') == MessageResponse(success=False,
                                                                                                                                                  error=error,
                                                                                                                                                  message=None)

        message = MessageField(
            id='1',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[],
        )
        json_str = ('{"success": true, "message": {"id": "1", "text": "msg", "user_id": "1", '
                    '"conversation_id": 1, "send_time": 1617889170, "update_time": 1617889170, "blocks": []}}')
        assert MessageResponse.parse_raw(json_str) == MessageResponse(success=True, error=None, message=message)


class TestDepartmentListResponse:
    def test_properties(self):
        r = DepartmentListResponse()
        assert r.success is True
        assert r.error is None
        assert r.departments is None

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = DepartmentListResponse(success=False, error=error)
        assert r.success is False
        assert r.error == error
        assert r.departments is None

        department = DepartmentField(
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
        r = DepartmentListResponse(success=True, departments=[department])
        assert r.success is True
        assert r.error is None
        assert r.departments == [department]

    def test_to_json(self):
        r = DepartmentListResponse()
        assert r.json(exclude_none=True) == '{"success": true}'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = DepartmentListResponse(success=False, error=error)
        assert r.json(exclude_none=True) == '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}'

        department = DepartmentField(
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
        r = DepartmentListResponse(success=True, departments=[department])
        assert r.json(exclude_none=True) == (
            '{"success": true, "departments": [{"id": "1", "ids_path": "1", "parent_id": "0", "space_id": "1", '
            '"name": "name", "code": "code", "user_count": 1, "has_child": false, "depth": 0, "users_ids": [1], "leader_ids": [1], "ancestry": ""}]}')

    def test_to_plain(self):
        r = DepartmentListResponse()
        assert r.plain() == 'OK'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = DepartmentListResponse(success=False, error=error)
        assert r.plain() == 'Error code:\tapi_not_found\nMessage:\tapi not found'

        department = DepartmentField(
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
        r = DepartmentListResponse(success=True, departments=[department])
        assert r.plain() == 'ID:\t\t1\nName:\t\tname\nCode:\t\tcode\nUser count:\t1'

    def test_from_json(self):
        assert DepartmentListResponse.parse_raw('{"success": true}') == DepartmentListResponse(success=True, error=None, cursor=None, departments=None)

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert DepartmentListResponse.parse_raw('{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}') == DepartmentListResponse(
            success=False, error=error, cursor=None, departments=None)

        department = DepartmentField(
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
        json_str = ('{"success": true, "departments": [{"id": "1", "ids_path": "1", "parent_id": "0", "space_id": "1", '
                    '"name": "name", "code": "code", "user_count": 1, "has_child": false, "depth": 0, "users_ids": [1], "leader_ids": [1], "ancestry": ""}]}')
        assert DepartmentListResponse.parse_raw(json_str) == DepartmentListResponse(success=True, error=None, cursor=None, departments=[department])


class TestSpaceResponse:
    def test_properties(self):
        r = SpaceResponse()
        assert r.success is True
        assert r.error is None
        assert r.space is None

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = SpaceResponse(success=False, error=error)
        assert r.success is False
        assert r.error == error
        assert r.space is None

        space = SpaceField(
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
        r = SpaceResponse(success=True, space=space)
        assert r.success is True
        assert r.error is None
        assert r.space == space

    def test_to_json(self):
        r = SpaceResponse()
        assert r.json(exclude_none=True) == '{"success": true}'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = SpaceResponse(success=False, error=error)
        assert r.json(exclude_none=True) == '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}'

        space = SpaceField(
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
        r = SpaceResponse(success=True, space=space)
        assert r.json(exclude_none=True) == (
            '{"success": true, "space": {"id": 1, "kakaoi_org_id": 1, "name": "name", "color_code": "default", "color_tone": "light", '
            '"permitted_ext": ["*"], "profile_name_format": "name_only", "profile_position_format": "position", "logo_url": "http://localhost/image.png"}}')

    def test_to_plain(self):
        r = SpaceResponse()
        assert r.plain() == 'OK'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = SpaceResponse(success=False, error=error)
        assert r.plain() == 'Error code:\tapi_not_found\nMessage:\tapi not found'

        space = SpaceField(
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
        r = SpaceResponse(success=True, space=space)
        assert r.plain() == ("ID:\t1\nOrgID:\t1\nName:\tname\nColor code:\tdefault\nColor tone:\tlight\nPermitted ext:\t['*']\n"
                             "Profile name format:\tname_only\nProfile position format:\tposition\nLogo URL:\thttp://localhost/image.png")

    def test_from_json(self):
        assert SpaceResponse.parse_raw('{"success": true}') == SpaceResponse(success=True, error=None, space=None)

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert SpaceResponse.parse_raw('{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}') == SpaceResponse(success=False,
                                                                                                                                              error=error,
                                                                                                                                              space=None)

        space = SpaceField(
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
        json_str = (
            '{"success": true, "space": {"id": 1, "kakaoi_org_id": 1, "name": "name", "color_code": "default", "color_tone": "light", '
            '"permitted_ext": ["*"], "profile_name_format": "name_only", "profile_position_format": "position", "logo_url": "http://localhost/image.png"}}')
        assert SpaceResponse.parse_raw(json_str) == SpaceResponse(success=True, error=None, space=space)


class TestBotResponse:
    def test_properties(self):
        r = BotResponse()
        assert r.success is True
        assert r.error is None
        assert r.info is None

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = BotResponse(success=False, error=error)
        assert r.success is False
        assert r.error == error
        assert r.info is None

        info = BotField(
            bot_id=1,
            title='bot',
            status=BotStatus.ACTIVATED,
        )
        r = BotResponse(success=True, info=info)
        assert r.success is True
        assert r.error is None
        assert r.info == info

    def test_to_json(self):
        r = BotResponse()
        assert r.json(exclude_none=True) == '{"success": true}'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = BotResponse(success=False, error=error)
        assert r.json(exclude_none=True) == '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}'

        info = BotField(
            bot_id=1,
            title='bot',
            status=BotStatus.ACTIVATED,
        )
        r = BotResponse(success=True, info=info)
        assert r.json(exclude_none=True) == '{"success": true, "info": {"bot_id": 1, "title": "bot", "status": "activated"}}'

    def test_to_plain(self):
        r = BotResponse()
        assert r.plain() == 'OK'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = BotResponse(success=False, error=error)
        assert r.plain() == 'Error code:\tapi_not_found\nMessage:\tapi not found'

        info = BotField(
            bot_id=1,
            title='bot',
            status=BotStatus.ACTIVATED,
        )
        r = BotResponse(success=True, info=info)
        assert r.plain() == 'ID:\t1\nName:\tbot\nStatus:\tactivated'

    def test_from_json(self):
        assert BotResponse.parse_raw('{"success": true}') == BotResponse(success=True, error=None, info=None)

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert BotResponse.parse_raw('{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}') == BotResponse(success=False,
                                                                                                                                          error=error,
                                                                                                                                          info=None)

        info = BotField(
            bot_id=1,
            title='bot',
            status=BotStatus.ACTIVATED,
        )
        json_str = '{"success": true, "info": {"bot_id": 1, "title": "bot", "status": "activated"}}'
        assert BotResponse.parse_raw(json_str) == BotResponse(success=True, error=None, info=info)
