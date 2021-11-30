from datetime import datetime

import pytest
from pytz import utc
from pytest_mock import MockerFixture
from click.testing import Result, CliRunner

from kakaowork.consts import Limit
from kakaowork.blockkit import TextBlock, DividerBlock

from kakaowork.models import (
    BaseResponse,
    ErrorCode,
    BotStatus,
    ColorTone,
    ProfileNameFormat,
    ProfilePositionFormat,
    ErrorField,
    UserField,
    ConversationType,
    ConversationField,
    MessageField,
    DepartmentField,
    SpaceField,
    BotField,
    UserResponse,
    UserListResponse,
    ConversationResponse,
    ConversationListResponse,
    MessageResponse,
    DepartmentListResponse,
    SpaceResponse,
    BotResponse,
)
from kakaowork.command import (
    _command_aliases,
    cli,
    users,
    conversations,
    messages,
    departments,
    spaces,
    bots,
)
from kakaowork.utils import to_kst


def test__command_aliases():
    assert _command_aliases() == {
        'user': 'users',
        'conversation': 'conversations',
        'conv': 'conversations',
        'message': 'messages',
        'msg': 'messages',
        'department': 'departments',
        'dept': 'departments',
        'space': 'spaces',
        'bot': 'bots',
    }


class TestUsersCommand:
    @pytest.fixture(scope='class')
    def user_field(self):
        return UserField(id='1', space_id='2', name='name')

    @pytest.fixture(scope='class')
    def user_list_response(self, user_field):
        return UserListResponse(success=True, users=[user_field])

    @pytest.fixture(scope='class')
    def user_response(self, user_field):
        return UserResponse(success=True, user=user_field)

    @pytest.fixture(scope='class')
    def base_response(self):
        return BaseResponse(success=True)

    @pytest.mark.parametrize(
        'args,exit_code',
        [
            (['list'], 0),
            (['list', '--limit', '5'], 0),
            (['list', '--limit', '0'], 2),
            (['list', '--limit', '101'], 2),
        ]
    )
    def test_list(self, args, exit_code, user_list_response, mocker: MockerFixture, cli_runner: CliRunner):
        mocker.patch('kakaowork.client.Kakaowork.Users.list', return_value=user_list_response)
        res = cli_runner.invoke(users, args)
        assert res.exit_code == exit_code
        assert res.output is not None and len(res.output) > 0

    @pytest.mark.parametrize(
        'args,exit_code',
        [
            (['find'], 2),
            (['find', '--user-id', '1'], 0),
            (['find', '-u', '1'], 0),
            (['find', '--email', 'nobody@email.com'], 0),
            (['find', '-e', 'nobody@email.com'], 0),
            (['find', '--mobile', '000-0000-0000'], 0),
            (['find', '-m', '000-0000-0000'], 0)
        ],
    )
    def test_find(self, args, exit_code, user_response, mocker: MockerFixture, cli_runner: CliRunner):
        mocker.patch('kakaowork.client.Kakaowork.Users.info', return_value=user_response)
        mocker.patch('kakaowork.client.Kakaowork.Users.find_by_email', return_value=user_response)
        mocker.patch('kakaowork.client.Kakaowork.Users.find_by_phone_number', return_value=user_response)
        res = cli_runner.invoke(users, args)
        assert res.exit_code == exit_code

    @pytest.mark.parametrize(
        'args,exit_code',
        [
            (['set'], 2),
            (['set', '1'], 2),
            (['set', '1', '--work-time', '#####'], 2),
            (['set', '1', '--work-time', '2021-01-01T10:00:00'], 2),
            (['set', '1', '--vacation-time', '#####'], 2),
            (['set', '1', '--work-time', '2021-01-01T10:00:00'], 2),
            (['set', '1', '--vacation-time', '2021-01-01T10:00:00'], 2),
            (['set', '1', '2', '--work-time', '2021-01-01T10:00:00', '2021-01-01T19:00:00'], 2),
            (['set', '1', '2', '--vacation-time', '2021-01-01T10:00:00', '2021-01-01T19:00:00'], 2),
            (['set', '1', '--work-time', '2021-01-01T10:00:00', '2021-01-01T19:00:00'], 0),
            (['set', '1', '--vacation-time', '2021-01-01T10:00:00', '2021-01-01T19:00:00'], 0),
            (['set', '1', '--work-time', '2021-01-01T10:00:00', '2021-01-01T19:00:00', '--vacation-time', '2021-01-02T10:00:00', '2021-01-02T19:00:00'], 0),
        ],
    )
    def test_set(self, args, exit_code, base_response, mocker: MockerFixture, cli_runner: CliRunner):
        mocker.patch('kakaowork.client.Kakaowork.Users.set_work_time', return_value=base_response)
        mocker.patch('kakaowork.client.Kakaowork.Users.set_vacation_time', return_value=base_response)
        res = cli_runner.invoke(users, args)
        assert res.exit_code == exit_code


class TestConversationsCommand:
    @pytest.fixture(scope='class')
    def conversation_field(self):
        return ConversationField(id='1', type=ConversationType.DM, users_count=1)

    @pytest.fixture(scope='class')
    def user_field(self):
        return UserField(id='1', space_id='2', name='name')

    @pytest.fixture(scope='class')
    def conversation_response(self, conversation_field):
        return ConversationResponse(success=True, conversation=conversation_field)

    @pytest.fixture(scope='class')
    def conversation_list_response(self, conversation_field):
        return ConversationListResponse(success=True, conversations=[conversation_field])

    @pytest.fixture(scope='class')
    def user_list_response(self, user_field):
        return UserListResponse(success=True, users=[user_field])

    @pytest.fixture(scope='class')
    def base_response(self):
        return BaseResponse(success=True)

    @pytest.mark.parametrize(
        'args,exit_code',
        [
            (['open'], 2),
            (['open', '1'], 0),
            (['open', '1', '2'], 0),
        ],
    )
    def test_open(self, args, exit_code, conversation_response, mocker: MockerFixture, cli_runner: CliRunner):
        mocker.patch('kakaowork.client.Kakaowork.Conversations.open', return_value=conversation_response)
        res = cli_runner.invoke(conversations, args)
        assert res.exit_code == exit_code

    @pytest.mark.parametrize(
        'args,exit_code',
        [
            (['list'], 0),
            (['list', '--limit', '5'], 0),
            (['list', '--limit', '0'], 2),
            (['list', '--limit', '101'], 2),
        ]
    )
    def test_list(self, args, exit_code, conversation_list_response, mocker: MockerFixture, cli_runner: CliRunner):
        mocker.patch('kakaowork.client.Kakaowork.Conversations.list', return_value=conversation_list_response)
        res = cli_runner.invoke(conversations, args)
        assert res.exit_code == exit_code

    @pytest.mark.parametrize(
        'args,exit_code',
        [
            (['users'], 2),
            (['users', '1'], 0),
            (['users', '1', '2'], 2),
        ]
    )
    def test_users(self, args, exit_code, user_list_response, mocker: MockerFixture, cli_runner: CliRunner):
        mocker.patch('kakaowork.client.Kakaowork.Conversations.users', return_value=user_list_response)
        res = cli_runner.invoke(conversations, args)
        assert res.exit_code == exit_code

    @pytest.mark.parametrize(
        'args,exit_code',
        [
            (['invite'], 2),
            (['invite', '1'], 2),
            (['invite', '1', '2'], 0),
            (['invite', '1', '2', '3'], 0),
        ]
    )
    def test_invite(self, args, exit_code, base_response, mocker: MockerFixture, cli_runner: CliRunner):
        mocker.patch('kakaowork.client.Kakaowork.Conversations.invite', return_value=base_response)
        res = cli_runner.invoke(conversations, args)
        assert res.exit_code == exit_code

    @pytest.mark.parametrize(
        'args,exit_code',
        [
            (['kick'], 2),
            (['kick', '1'], 2),
            (['kick', '1', '2'], 0),
            (['kick', '1', '2', '3'], 0),
        ]
    )
    def test_kick(self, args, exit_code, base_response, mocker: MockerFixture, cli_runner: CliRunner):
        mocker.patch('kakaowork.client.Kakaowork.Conversations.kick', return_value=base_response)
        res = cli_runner.invoke(conversations, args)
        assert res.exit_code == exit_code


class TestMessagesCommand:
    @pytest.fixture(scope='class')
    def blocks(self):
        return [
            TextBlock(text='msg'),
            DividerBlock(),
        ]

    @pytest.fixture(scope='class')
    def message_field(self, blocks):
        return MessageField(
            id='1',
            text='msg',
            user_id='uid1',
            conversation_id=1,
            send_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            update_time=to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)),
            blocks=blocks,
        )

    @pytest.fixture(scope='class')
    def message_response(self, message_field):
        return MessageResponse(message=message_field)

    @pytest.mark.parametrize(
        'args,exit_code',
        [
            (['send'], 2),
            (['send', '1'], 2),
            (['send', '1', 'hello'], 0),
            (['send', '1', 'hello', '--block', 'type=text text=msg'], 0),
            (['send', '1', 'hello', '-b', 'type=text text=msg'], 0),
            (['send', '1', 'hello', '-b', 'type=text text=msg', '-b', 'type=divider'], 0),
        ],
    )
    def test_send(self, args, exit_code, message_response, mocker: MockerFixture, cli_runner: CliRunner):
        mocker.patch('kakaowork.client.Kakaowork.Messages.send', return_value=message_response)
        res = cli_runner.invoke(messages, args)
        assert res.exit_code == exit_code


class TestDepartmentsCommand:
    @pytest.fixture(scope='class')
    def department_field(self):
        return DepartmentField(
            id='1',
            ids_path='1',
            parent_id='',
            space_id='1',
            name='name',
            code='code',
            user_count=1,
            has_child=False,
            depth=0,
            users_ids=[1],
            leader_ids=[1],
            ancestry='anc',
        )

    @pytest.fixture(scope='class')
    def department_list_response(self, department_field):
        return DepartmentListResponse(
            success=True,
            departments=[department_field],
        )

    @pytest.mark.parametrize(
        'args,exit_code',
        [
            (['list'], 0),
            (['list', '--limit', '5'], 0),
            (['list', '--limit', '0'], 2),
            (['list', '--limit', '101'], 2),
        ]
    )
    def test_list(self, args, exit_code, department_list_response, mocker: MockerFixture, cli_runner: CliRunner):
        mocker.patch('kakaowork.client.Kakaowork.Departments.list', return_value=department_list_response)
        res = cli_runner.invoke(departments, args)
        assert res.exit_code == exit_code


class TestSpacesCommand:
    @pytest.fixture(scope='class')
    def space_field(self):
        return SpaceField(
            id=1,
            kakaoi_org_id=1,
            name='name',
            color_code='default',
            color_tone=ColorTone.LIGHT,
            permitted_ext=['*'],
            profile_name_format=ProfileNameFormat.NAME_NICKNAME,
            profile_position_format=ProfilePositionFormat.POSITION,
            logo_url='http://localhost/image.png',
        )

    @pytest.fixture(scope='class')
    def space_response(self, space_field):
        return SpaceResponse(
            success=True,
            space=space_field,
        )

    @pytest.mark.parametrize(
        'args,exit_code',
        [
            (['info'], 0),
        ],
    )
    def test_info(self, args, exit_code, space_response, mocker: MockerFixture, cli_runner: CliRunner):
        mocker.patch('kakaowork.client.Kakaowork.Spaces.info', return_value=space_response)
        res = cli_runner.invoke(spaces, args)
        assert res.exit_code == exit_code


class TestBotsCommand:
    @pytest.fixture(scope='class')
    def bot_field(self):
        return BotField(bot_id=1, title='name', status=BotStatus.ACTIVATED)

    @pytest.fixture(scope='class')
    def bot_response(self, bot_field):
        return BotResponse(
            success=True,
            info=bot_field,
        )

    @pytest.mark.parametrize(
        'args,exit_code',
        [
            (['info'], 0),
        ],
    )
    def test_info(self, args, exit_code, bot_response, mocker: MockerFixture, cli_runner: CliRunner):
        mocker.patch('kakaowork.client.Kakaowork.Bots.info', return_value=bot_response)
        res = cli_runner.invoke(bots, args)
        assert res.exit_code == exit_code
