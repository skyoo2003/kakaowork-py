import warnings
from datetime import datetime, timezone

import pytest
from pytz import utc

from kakaowork.exceptions import NoValueError
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


class TestErrorField:
    def test_error_field_to_dict(self):
        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert error.to_dict() == {'code': 'api_not_found', 'message': 'api not found'}

    def test_error_field_from_dict(self):
        with pytest.raises(NoValueError):
            ErrorField.from_dict({})

        error = ErrorField.from_dict({
            'code': 'api_not_found',
            'message': 'api not found',
        })
        assert error.code == ErrorCode.API_NOT_FOUND
        assert error.message == 'api not found'

        error = ErrorField.from_dict({
            'code': '???',
            'message': 'unknwon error',
        })
        assert error.code == ErrorCode.UNKNOWN
        assert error.message == 'unknwon error'

        with warnings.catch_warnings(record=True) as w:
            ErrorField.from_dict({
                'code': 'api_not_found',
                'message': 'api not found',
                '_extra': 'extra!!',
            })
            assert len(w) == 1
            assert issubclass(w[-1].category, RuntimeWarning)
            assert str(w[-1].message) == 'There are missing fields: _extra'


class TestUserIdentificationField:
    def test_user_identification_to_dict(self):
        uid = UserIdentificationField(type='gmail', value='user@localhost')
        assert uid.to_dict() == {'type': 'gmail', 'value': 'user@localhost'}

    def test_user_identification_from_dict(self):
        with pytest.raises(NoValueError):
            UserIdentificationField.from_dict({})

        uid = UserIdentificationField.from_dict({
            'type': 'gmail',
            'value': 'user@localhost',
        })
        assert uid.type == 'gmail'
        assert uid.value == 'user@localhost'

        with warnings.catch_warnings(record=True) as w:
            UserIdentificationField.from_dict({
                'type': 'gmail',
                'value': 'user@localhost',
                '_extra': 'extra!!',
            })
            assert len(w) == 1
            assert issubclass(w[-1].category, RuntimeWarning)
            assert str(w[-1].message) == 'There are missing fields: _extra'


class TestUserField:
    def test_user_field_to_dict(self):
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
        assert user.to_dict() == {
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
            'work_start_time': 1617889170,
            'work_end_time': 1617889170,
            'vacation_start_time': 1617889170,
            'vacation_end_time': 1617889170,
        }

    def test_user_field_from_dict(self):
        with pytest.raises(NoValueError):
            UserField.from_dict({})

        user = UserField.from_dict({
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
        })
        assert user.avatar_url is None
        assert user.department == 'test'
        assert user.id == '1234'
        assert user.identifications == [UserIdentificationField(type='email', value='user@localhost')]
        assert user.mobiles == []
        assert user.name == 'noname'
        assert user.nickname is None
        assert user.position is None
        assert user.responsibility == 'leader'
        assert user.space_id == '123'
        assert user.tels == []
        assert user.vacation_end_time == to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc))
        assert user.vacation_start_time == to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc))
        assert user.work_end_time == to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc))
        assert user.work_start_time == to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc))

        with warnings.catch_warnings(record=True) as w:
            UserField.from_dict({
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
                '_extra': 'extra!!',
            })
            assert len(w) == 1
            assert issubclass(w[-1].category, RuntimeWarning)
            assert str(w[-1].message) == 'There are missing fields: _extra'


class TestConversationField:
    def test_conversation_field_to_dict(self):
        conversation = ConversationField(
            id='1',
            type=ConversationType.DM,
            users_count=2,
            avatar_url='http://localhost/image.png',
            name='noname',
        )
        assert conversation.to_dict() == {
            'id': '1',
            'type': 'dm',
            'users_count': 2,
            'avatar_url': 'http://localhost/image.png',
            'name': 'noname',
        }

    def test_conversation_field_from_dict(self):
        with pytest.raises(NoValueError):
            ConversationField.from_dict({})

        conversation = ConversationField.from_dict({
            'id': '1',
            'type': 'dm',
            'users_count': 2,
            'avatar_url': None,
            'name': 'noname',
        })
        assert conversation.id == '1'
        assert conversation.type == ConversationType.DM
        assert conversation.users_count == 2
        assert conversation.avatar_url is None
        assert conversation.name == 'noname'

        with warnings.catch_warnings(record=True) as w:
            ConversationField.from_dict({
                'id': '1',
                'type': 'dm',
                'users_count': 2,
                'avatar_url': None,
                'name': 'noname',
                '_extra': 'extra!!',
            })
            assert len(w) == 1
            assert issubclass(w[-1].category, RuntimeWarning)
            assert str(w[-1].message) == 'There are missing fields: _extra'


class TestMessageField:
    def test_message_field_to_dict(self):
        message = MessageField(
            id='123',
            text='msg',
            user_id='1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=[TextBlock(text='block', markdown=False)],
        )
        assert message.to_dict() == {
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
            }]
        }

    def test_message_field_from_dict(self):
        with pytest.raises(NoValueError):
            MessageField.from_dict({})

        message = MessageField.from_dict({
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
        })
        assert message.id == '123'
        assert message.text == 'msg'
        assert message.user_id == '1'
        assert message.conversation_id == 1
        assert message.send_time == to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc))
        assert message.update_time == to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc))
        assert message.blocks == [TextBlock(text='block', markdown=False)]

        with warnings.catch_warnings(record=True) as w:
            MessageField.from_dict({
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
                '_extra': 'extra!!',
            })
            assert len(w) == 1
            assert issubclass(w[-1].category, RuntimeWarning)
            assert str(w[-1].message) == 'There are missing fields: _extra'


class TestDepartmentField:
    def test_department_field_to_dict(self):
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
        assert department.to_dict() == {
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

    def test_department_field_from_dict(self):
        with pytest.raises(NoValueError):
            DepartmentField.from_dict({})

        department = DepartmentField.from_dict({
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
        })
        assert department.id == '1'
        assert department.ids_path == '1'
        assert department.parent_id == ''
        assert department.space_id == '1'
        assert department.name == 'dep'
        assert department.code == 'depcode'
        assert department.user_count == 1
        assert department.has_child is False
        assert department.depth == 0
        assert department.users_ids == [1]
        assert department.leader_ids == [1]
        assert department.ancestry == ''

        with warnings.catch_warnings(record=True) as w:
            DepartmentField.from_dict({
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
                '_extra': 'extra!!',
            })
            assert len(w) == 1
            assert issubclass(w[-1].category, RuntimeWarning)
            assert str(w[-1].message) == 'There are missing fields: _extra'


class TestSpaceField:
    def test_space_field_to_dict(self):
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
        assert space.to_dict() == {
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

    def test_space_field_from_dict(self):
        with pytest.raises(NoValueError):
            SpaceField.from_dict({})

        space = SpaceField.from_dict({
            'id': 1,
            'kakaoi_org_id': 1,
            'name': 'space',
            'color_code': 'default',
            'color_tone': 'light',
            'permitted_ext': ['*'],
            'profile_name_format': 'name_only',
            'profile_position_format': 'position',
            'logo_url': 'http://localhost/image.png',
        })
        assert space.id == 1
        assert space.kakaoi_org_id == 1
        assert space.name == 'space'
        assert space.color_code == 'default'
        assert space.color_tone == ColorTone.LIGHT
        assert space.permitted_ext == ['*']
        assert space.profile_name_format == ProfileNameFormat.NAME_ONLY
        assert space.profile_position_format == ProfilePositionFormat.POSITION
        assert space.logo_url == 'http://localhost/image.png'

        with warnings.catch_warnings(record=True) as w:
            SpaceField.from_dict({
                'id': 1,
                'kakaoi_org_id': 1,
                'name': 'space',
                'color_code': 'default',
                'color_tone': 'light',
                'permitted_ext': ['*'],
                'profile_name_format': 'name_only',
                'profile_position_format': 'position',
                'logo_url': 'http://localhost/image.png',
                '_extra': 'extra!!',
            })
            assert len(w) == 1
            assert issubclass(w[-1].category, RuntimeWarning)
            assert str(w[-1].message) == 'There are missing fields: _extra'


class TestBotField:
    def test_bot_field_to_dict(self):
        bot = BotField(
            bot_id=1,
            title='bot',
            status=BotStatus.ACTIVATED,
        )
        assert bot.to_dict() == {
            'bot_id': 1,
            'title': 'bot',
            'status': 'activated',
        }

    def test_bot_field_from_dict(self):
        with pytest.raises(NoValueError):
            BotField.from_dict({})

        bot = BotField.from_dict({
            'bot_id': 1,
            'title': 'bot',
            'status': 'activated',
        })
        assert bot.bot_id == 1
        assert bot.title == 'bot'
        assert bot.status == BotStatus.ACTIVATED

        with warnings.catch_warnings(record=True) as w:
            BotField.from_dict({
                'bot_id': 1,
                'title': 'bot',
                'status': 'activated',
                '_extra': 'extra!!',
            })
            assert len(w) == 1
            assert issubclass(w[-1].category, RuntimeWarning)
            assert str(w[-1].message) == 'There are missing fields: _extra'


class TestBaseResponse:
    def test_base_response_properties(self):
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

    def test_base_response_to_json(self):
        r = BaseResponse()
        assert r.to_json() == '{"success": true, "error": null}'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = BaseResponse(success=False, error=error)
        assert r.to_json() == '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}'

        r = BaseResponse(success=True)
        assert r.to_json() == '{"success": true, "error": null}'

    def test_base_response_to_plain(self):
        r = BaseResponse()
        assert r.to_plain() == 'OK'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = BaseResponse(success=True, error=error)
        assert r.to_plain() == 'Error code:\tapi_not_found\nMessage:\tapi not found'

        r = BaseResponse(success=True)
        assert r.to_plain() == 'OK'

    def test_base_response_from_json(self):
        assert BaseResponse.from_json('{"success": true, "error": null}') == BaseResponse(success=True, error=None)

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert BaseResponse.from_json('{"success": false, "error": {"code": "api_not_found", "message": "api not found"}}') == BaseResponse(success=False,
                                                                                                                                            error=error)


class TestUserResponse:
    def test_user_response_properties(self):
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

    def test_user_response_to_json(self):
        r = UserResponse()
        assert r.to_json() == '{"success": true, "error": null, "user": null}'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = UserResponse(success=False, error=error)
        assert r.to_json() == '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}, "user": null}'

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
        assert r.to_json() == (
            '{"success": true, "error": null, "user": {"id": 1234, "space_id": 12, "name": "name", "display_name": "dp", '
            '"identifications": [{"type": "email", "value": "user@localhost"}], "nickname": "nickname", "avatar_url": "http://localhost/image.png", '
            '"department": "dep", "position": "position", "responsibility": "resp", "tels": [], "mobiles": [], "work_start_time": 1617889170, '
            '"work_end_time": 1617889170, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}}')

    def test_user_response_to_plain(self):
        r = UserResponse()
        assert r.to_plain() == 'OK'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = UserResponse(success=False, error=error)
        assert r.to_plain() == 'Error code:\tapi_not_found\nMessage:\tapi not found'

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
        assert r.to_plain() == (
            "ID:\t1234\nName:\tname\nNickname:\tnickname\nDepartment:\tdep\nPosition:\tposition\nResponsibility:\tresp\nTels:\t[]\nMobiles:\t[]\n"
            "Work start time:\t2021-04-08 22:39:30+09:00\nWork end time:\t2021-04-08 22:39:30+09:00\n"
            "Vacation start time:\t2021-04-08 22:39:30+09:00\nVacation end time:\t2021-04-08 22:39:30+09:00")

    def test_user_response_from_json(self):
        assert UserResponse.from_json('{"success": false, "error": null, "user": null}') == UserResponse(success=False, error=None, user=None)

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert UserResponse.from_json('{"success": true, "error": {"code": "api_not_found", "message": "api not found"}}') == UserResponse(success=True,
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
        assert UserResponse.from_json(json_str) == UserResponse(success=True, error=None, user=user)


class TestUserListResponse:
    def test_user_list_response_properties(self):
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
        assert r.success is True
        assert r.error is None
        assert r.cursor is None
        assert r.users == [user]

    def test_user_list_response_to_json(self):
        r = UserListResponse()
        assert r.to_json() == '{"success": true, "error": null, "cursor": null, "users": null}'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = UserListResponse(success=False, error=error)
        assert r.to_json() == '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}, "cursor": null, "users": null}'

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
        r = UserListResponse(success=True, users=[user])
        assert r.to_json() == (
            '{"success": true, "error": null, "cursor": null, "users": [{"id": 1234, "space_id": 12, "name": "name", "display_name": "dp", '
            '"identifications": [{"type": "email", "value": "user@localhost"}], "nickname": "nickname", "avatar_url": "http://localhost/image.png", '
            '"department": "dep", "position": "position", "responsibility": "resp", "tels": [], "mobiles": [], "work_start_time": 1617889170, '
            '"work_end_time": 1617889170, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}]}')

    def test_user_list_response_to_plain(self):
        r = UserListResponse()
        assert r.to_plain() == 'OK'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = UserListResponse(success=False, error=error)
        assert r.to_plain() == 'Error code:\tapi_not_found\nMessage:\tapi not found'

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
        assert r.to_plain() == (
            "ID:\t1234\nName:\tname\nNickname:\tnickname\nDepartment:\tdep\nPosition:\tposition\nResponsibility:\tresp\nTels:\t[]\nMobiles:\t[]\n"
            "Work start time:\t2021-04-08 22:39:30+09:00\nWork end time:\t2021-04-08 22:39:30+09:00\n"
            "Vacation start time:\t2021-04-08 22:39:30+09:00\nVacation end time:\t2021-04-08 22:39:30+09:00")

    def test_user_list_response_from_json(self):
        assert UserListResponse.from_json('{"success": true, "error": null, "cursor": null, "users": null}') == UserListResponse(success=True,
                                                                                                                                 error=None,
                                                                                                                                 cursor=None,
                                                                                                                                 users=None)

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert UserListResponse.from_json(
            '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}, "cursor": null, "users": null}') == UserListResponse(
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
        json_str = ('{"success": true, "error": null, "cursor": null, "users": [{"id": 1234, "space_id": 12, "name": "name", '
                    '"identifications": [{"type": "email", "value": "user@localhost"}], "nickname": "nickname", "avatar_url": "http://localhost/image.png", '
                    '"department": "dep", "position": "position", "responsibility": "resp", "tels": [], "mobiles": [], "work_start_time": 1617889170, '
                    '"work_end_time": 1617889170, "vacation_start_time": 1617889170, "vacation_end_time": 1617889170}]}')
        assert UserListResponse.from_json(json_str) == UserListResponse(success=True, error=None, cursor=None, users=[user])


class TestConversationResponse:
    def test_conversation_response_properties(self):
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

    def test_conversation_response_to_json(self):
        r = ConversationResponse()
        assert r.to_json() == '{"success": true, "error": null, "conversation": null}'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = ConversationResponse(success=False, error=error)
        assert r.to_json() == '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}, "conversation": null}'

        conversation = ConversationField(
            id='1',
            name='name',
            type=ConversationType.DM,
            users_count=1,
            avatar_url='http://localhost/image.png',
        )
        r = ConversationResponse(success=True, conversation=conversation)
        assert r.to_json() == ('{"success": true, "error": null, "conversation": {"id": "1", "type": "dm", "users_count": 1, '
                               '"avatar_url": "http://localhost/image.png", "name": "name"}}')

    def test_conversation_response_to_plain(self):
        r = ConversationResponse()
        assert r.to_plain() == 'OK'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = ConversationResponse(success=False, error=error)
        assert r.to_plain() == 'Error code:\tapi_not_found\nMessage:\tapi not found'

        conversation = ConversationField(
            id='1',
            name='name',
            type=ConversationType.DM,
            users_count=1,
            avatar_url='http://localhost/image.png',
        )
        r = ConversationResponse(success=True, conversation=conversation)
        assert r.to_plain() == 'ID:\t1\nType:\tdm\nName:\tname\nAvatar URL:\thttp://localhost/image.png'

    def test_conversation_response_from_json(self):
        assert ConversationResponse.from_json('{"success": true, "error": null, "conversation": null}') == ConversationResponse(success=True,
                                                                                                                                error=None,
                                                                                                                                conversation=None)

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert ConversationResponse.from_json(
            '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}, "conversation": null}') == ConversationResponse(
                success=False, error=error, conversation=None)

        conversation = ConversationField(
            id='1',
            name='name',
            type=ConversationType.DM,
            users_count=1,
            avatar_url='http://localhost/image.png',
        )
        json_str = ('{"success": true, "error": null, "conversation": {"id": "1", "type": "dm", "users_count": 1, '
                    '"avatar_url": "http://localhost/image.png", "name": "name"}}')
        assert ConversationResponse.from_json(json_str) == ConversationResponse(success=True, error=None, conversation=conversation)


class TestConversationListResponse:
    def test_conversation_list_response_properties(self):
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

    def test_conversation_list_response_to_json(self):
        r = ConversationListResponse()
        assert r.to_json() == '{"success": true, "error": null, "cursor": null, "conversations": null}'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = ConversationListResponse(success=False, error=error)
        assert r.to_json() == '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}, "cursor": null, "conversations": null}'

        conversation = ConversationField(
            id='1',
            name='name',
            type=ConversationType.DM,
            users_count=1,
            avatar_url='http://localhost/image.png',
        )
        r = ConversationListResponse(success=True, conversations=[conversation])
        assert r.to_json() == ('{"success": true, "error": null, "cursor": null, "conversations": [{"id": "1", "type": "dm", "users_count": 1, '
                               '"avatar_url": "http://localhost/image.png", "name": "name"}]}')

    def test_conversation_list_response_to_plain(self):
        r = ConversationListResponse()
        assert r.to_plain() == 'OK'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = ConversationListResponse(success=False, error=error)
        assert r.to_plain() == 'Error code:\tapi_not_found\nMessage:\tapi not found'

        conversation = ConversationField(
            id='1',
            name='name',
            type=ConversationType.DM,
            users_count=1,
            avatar_url='http://localhost/image.png',
        )
        r = ConversationListResponse(success=True, conversations=[conversation])
        assert r.to_plain() == 'ID:\t1\nType:\tdm\nName:\tname\nAvatar URL:\thttp://localhost/image.png'

    def test_conversation_list_response_from_json(self):
        assert ConversationListResponse.from_json('{"success": true, "error": null, "cursor": null, "conversations": null}') == ConversationListResponse(
            success=True, error=None, cursor=None, conversations=None)

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert ConversationListResponse.from_json(
            '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}, "cursor": null, "conversations": null}'
        ) == ConversationListResponse(success=False, error=error, cursor=None, conversations=None)

        conversation = ConversationField(
            id='1',
            name='name',
            type=ConversationType.DM,
            users_count=1,
            avatar_url='http://localhost/image.png',
        )
        json_str = ('{"success": true, "error": null, "cursor": null, "conversations": [{"id": "1", "type": "dm", "users_count": 1, '
                    '"avatar_url": "http://localhost/image.png", "name": "name"}]}')
        assert ConversationListResponse.from_json(json_str) == ConversationListResponse(success=True, error=None, cursor=None, conversations=[conversation])


class TestMessageResponse:
    def test_message_response_properties(self):
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

    def test_message_response_to_json(self):
        r = MessageResponse()
        assert r.to_json() == '{"success": true, "error": null, "message": null}'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = MessageResponse(success=False, error=error)
        assert r.to_json() == '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}, "message": null}'

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
        assert r.to_json() == (
            '{"success": true, "error": null, '
            '"message": {"id": "1", "text": "msg", "user_id": "1", "conversation_id": 1, "send_time": 1617889170, "update_time": 1617889170, "blocks": null}}')

    def test_message_response_to_plain(self):
        r = MessageResponse()
        assert r.to_plain() == 'OK'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = MessageResponse(success=False, error=error)
        assert r.to_plain() == 'Error code:\tapi_not_found\nMessage:\tapi not found'

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
        assert r.to_plain() == ('ID:\t1\nConversation ID:\t1\n'
                                'Send time:\t2021-04-08 22:39:30+09:00\nUpdate time:\t2021-04-08 22:39:30+09:00\nText:\tmsg\nBlocks:\t-')

    def test_message_response_from_json(self):
        assert MessageResponse.from_json('{"success": true, "error": null, "message": null}') == MessageResponse(success=True, error=None, message=None)

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert MessageResponse.from_json(
            '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}, "message": null}') == MessageResponse(success=False,
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
        json_str = (
            '{"success": true, "error": null, '
            '"message": {"id": "1", "text": "msg", "user_id": "1", "conversation_id": 1, "send_time": 1617889170, "update_time": 1617889170, "blocks": null}}')
        assert MessageResponse.from_json(json_str) == MessageResponse(success=True, error=None, message=message)


class TestDepartmentListResponse:
    def test_department_list_response_properties(self):
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

    def test_department_list_response_to_json(self):
        r = DepartmentListResponse()
        assert r.to_json() == '{"success": true, "error": null, "cursor": null, "departments": null}'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = DepartmentListResponse(success=False, error=error)
        assert r.to_json() == '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}, "cursor": null, "departments": null}'

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
        assert r.to_json() == (
            '{"success": true, "error": null, "cursor": null, "departments": [{"id": "1", "ids_path": "1", "parent_id": "0", "space_id": "1", '
            '"name": "name", "code": "code", "user_count": 1, "has_child": false, "depth": 0, "users_ids": [1], "leader_ids": [1], "ancestry": ""}]}')

    def test_department_list_response_to_plain(self):
        r = DepartmentListResponse()
        assert r.to_plain() == 'OK'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = DepartmentListResponse(success=False, error=error)
        assert r.to_plain() == 'Error code:\tapi_not_found\nMessage:\tapi not found'

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
        assert r.to_plain() == 'ID:\t\t1\nName:\t\tname\nCode:\t\tcode\nUser count:\t1'

    def test_department_list_response_from_json(self):
        assert DepartmentListResponse.from_json('{"success": true, "error": null, "cursor": null, "departments": null}') == DepartmentListResponse(
            success=True, error=None, cursor=None, departments=None)

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert DepartmentListResponse.from_json(
            '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}, "cursor": null, "departments": null}'
        ) == DepartmentListResponse(success=False, error=error, cursor=None, departments=None)

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
        json_str = ('{"success": true, "error": null, "cursor": null, "departments": [{"id": "1", "ids_path": "1", "parent_id": "0", "space_id": "1", '
                    '"name": "name", "code": "code", "user_count": 1, "has_child": false, "depth": 0, "users_ids": [1], "leader_ids": [1], "ancestry": ""}]}')
        assert DepartmentListResponse.from_json(json_str) == DepartmentListResponse(success=True, error=None, cursor=None, departments=[department])


class TestSpaceResponse:
    def test_space_response_properties(self):
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

    def test_space_response_to_json(self):
        r = SpaceResponse()
        assert r.to_json() == '{"success": true, "error": null, "space": null}'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = SpaceResponse(success=False, error=error)
        assert r.to_json() == '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}, "space": null}'

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
        assert r.to_json() == (
            '{"success": true, "error": null, "space": {"id": 1, "kakaoi_org_id": 1, "name": "name", "color_code": "default", "color_tone": "light", '
            '"permitted_ext": ["*"], "profile_name_format": "name_only", "profile_position_format": "position", "logo_url": "http://localhost/image.png"}}')

    def test_space_response_to_plain(self):
        r = SpaceResponse()
        assert r.to_plain() == 'OK'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = SpaceResponse(success=False, error=error)
        assert r.to_plain() == 'Error code:\tapi_not_found\nMessage:\tapi not found'

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
        assert r.to_plain() == ("ID:\t1\nOrgID:\t1\nName:\tname\nColor code:\tdefault\nColor tone:\tlight\nPermitted ext:\t['*']\n"
                                "Profile name format:\tname_only\nProfile position format:\tposition\nLogo URL:\thttp://localhost/image.png")

    def test_space_response_from_json(self):
        assert SpaceResponse.from_json('{"success": true, "error": null, "space": null}') == SpaceResponse(success=True, error=None, space=None)

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert SpaceResponse.from_json('{"success": false, "error": {"code": "api_not_found", "message": "api not found"}, "space": null}') == SpaceResponse(
            success=False, error=error, space=None)

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
            '{"success": true, "error": null, "space": {"id": 1, "kakaoi_org_id": 1, "name": "name", "color_code": "default", "color_tone": "light", '
            '"permitted_ext": ["*"], "profile_name_format": "name_only", "profile_position_format": "position", "logo_url": "http://localhost/image.png"}}')
        assert SpaceResponse.from_json(json_str) == SpaceResponse(success=True, error=None, space=space)


class TestBotResponse:
    def test_bot_response_properties(self):
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

    def test_bot_response_to_json(self):
        r = BotResponse()
        assert r.to_json() == '{"success": true, "error": null, "info": null}'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = BotResponse(success=False, error=error)
        assert r.to_json() == '{"success": false, "error": {"code": "api_not_found", "message": "api not found"}, "info": null}'

        info = BotField(
            bot_id=1,
            title='bot',
            status=BotStatus.ACTIVATED,
        )
        r = BotResponse(success=True, info=info)
        assert r.to_json() == '{"success": true, "error": null, "info": {"bot_id": 1, "title": "bot", "status": "activated"}}'

    def test_bot_response_to_plain(self):
        r = BotResponse()
        assert r.to_plain() == 'OK'

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        r = BotResponse(success=False, error=error)
        assert r.to_plain() == 'Error code:\tapi_not_found\nMessage:\tapi not found'

        info = BotField(
            bot_id=1,
            title='bot',
            status=BotStatus.ACTIVATED,
        )
        r = BotResponse(success=True, info=info)
        assert r.to_plain() == 'ID:\t1\nName:\tbot\nStatus:\tactivated'

    def test_bot_response_from_json(self):
        assert BotResponse.from_json('{"success": true, "error": null, "info": null}') == BotResponse(success=True, error=None, info=None)

        error = ErrorField(code=ErrorCode.API_NOT_FOUND, message='api not found')
        assert BotResponse.from_json('{"success": false, "error": {"code": "api_not_found", "message": "api not found"}, "info": null}') == BotResponse(
            success=False, error=error, info=None)

        info = BotField(
            bot_id=1,
            title='bot',
            status=BotStatus.ACTIVATED,
        )
        json_str = '{"success": true, "error": null, "info": {"bot_id": 1, "title": "bot", "status": "activated"}}'
        assert BotResponse.from_json(json_str) == BotResponse(success=True, error=None, info=info)
