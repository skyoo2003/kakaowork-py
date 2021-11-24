import pytest
from pytest_mock import MockerFixture
from click.testing import Result, CliRunner

from kakaowork.consts import Limit
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
    DepartmentField,
    SpaceField,
    BotField,
    UserResponse,
    UserListResponse,
    ConversationResponse,
    ConversationListResponse,
    DepartmentListResponse,
    SpaceResponse,
    BotResponse,
)
from kakaowork.command import (
    _command_aliases,
    cli,
    users,
    conversations,
    departments,
    spaces,
    bots,
)


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
            (['list', '--limit', '1000'], 2),
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
            (['list', '--limit', '1000'], 2),
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

    def test_list(self, department_list_response, mocker: MockerFixture, cli_runner: CliRunner):
        mocker.patch('kakaowork.client.Kakaowork.Departments.list', return_value=department_list_response)

        expected_output = 'ID:\t\t1\nName:\t\tname\nCode:\t\tcode\nUser count:\t1\n'

        res = cli_runner.invoke(departments, ['list'])
        assert res.exit_code == 0
        assert res.output == expected_output

        res = cli_runner.invoke(cli, ['--app-key', 'dummy', 'department', 'list'])
        assert res.exit_code == 0
        assert res.output == expected_output

        res = cli_runner.invoke(cli, ['--app-key', 'dummy', 'dept', 'list'])
        assert res.exit_code == 0
        assert res.output == expected_output

    def test_departments_list_error(self, mocker: MockerFixture, cli_runner: CliRunner):
        resp = DepartmentListResponse(
            success=False,
            error=ErrorField(code=ErrorCode.UNAUTHORIZED, message='message'),
        )
        mocker.patch('kakaowork.client.Kakaowork.Departments.list', return_value=resp)

        res = cli_runner.invoke(departments, ['list'])
        assert res.exit_code == 1
        assert res.output == 'Error code:\tunauthorized\nMessage:\tmessage\n'

        res = cli_runner.invoke(departments, ['list', '--limit', '0'])
        assert res.exit_code == 2
        assert "Error: Invalid value for '-l' / '--limit': 0 is not in the range" in res.output

        res = cli_runner.invoke(departments, ['list', '--limit', '101'])
        assert res.exit_code == 2
        assert "Error: Invalid value for '-l' / '--limit': 101 is not in the range" in res.output


class TestSpacesCommand:
    def test_spaces_info_success(self, mocker: MockerFixture, cli_runner: CliRunner):
        resp = SpaceResponse(
            success=True,
            space=SpaceField(
                id=1,
                kakaoi_org_id=1,
                name='name',
                color_code='default',
                color_tone=ColorTone.LIGHT,
                permitted_ext=['*'],
                profile_name_format=ProfileNameFormat.NAME_NICKNAME,
                profile_position_format=ProfilePositionFormat.POSITION,
                logo_url='http://localhost/image.png',
            ),
        )
        mocker.patch('kakaowork.client.Kakaowork.Spaces.info', return_value=resp)

        expected_output = ("ID:\t1\nOrgID:\t1\nName:\tname\nColor code:\tdefault\nColor tone:\tlight\nPermitted ext:\t['*']\n"
                           "Profile name format:\tname_nickname\nProfile position format:\tposition\nLogo URL:\thttp://localhost/image.png\n")

        res = cli_runner.invoke(spaces, ['info'])
        assert res.exit_code == 0
        assert res.output == expected_output

        res = cli_runner.invoke(cli, ['--app-key', 'dummy', 'space', 'info'])
        assert res.exit_code == 0
        assert res.output == expected_output

    def test_spaces_info_error(self, mocker: MockerFixture, cli_runner: CliRunner):
        resp = SpaceResponse(
            success=False,
            error=ErrorField(code=ErrorCode.UNAUTHORIZED, message='message'),
        )
        mocker.patch('kakaowork.client.Kakaowork.Spaces.info', return_value=resp)

        res = cli_runner.invoke(spaces, ['info'])
        assert res.exit_code == 1
        assert res.output == 'Error code:\tunauthorized\nMessage:\tmessage\n'


class TestBotsCommand:
    def test_bots_info_success(self, mocker: MockerFixture, cli_runner: CliRunner):
        resp = BotResponse(
            success=True,
            info=BotField(bot_id=1, title='name', status=BotStatus.ACTIVATED),
        )
        mocker.patch('kakaowork.client.Kakaowork.Bots.info', return_value=resp)

        expected_output = 'ID:\t1\nName:\tname\nStatus:\tactivated\n'

        res = cli_runner.invoke(bots, ['info'])
        assert res.exit_code == 0
        assert res.output == expected_output

        res = cli_runner.invoke(cli, ['--app-key', 'dummy', 'bot', 'info'])
        assert res.exit_code == 0
        assert res.output == expected_output

    def test_bots_info_error(self, mocker: MockerFixture, cli_runner: CliRunner):
        response = BotResponse(
            success=False,
            error=ErrorField(code=ErrorCode.UNAUTHORIZED, message='message'),
        )
        mocker.patch('kakaowork.client.Kakaowork.Bots.info', return_value=response)

        res = cli_runner.invoke(bots, ['info'])
        assert res.exit_code == 1
        assert res.output == 'Error code:\tunauthorized\nMessage:\tmessage\n'
