from pytest_mock import MockerFixture
from click.testing import Result, CliRunner

from kakaowork.models import (
    ErrorCode,
    BotStatus,
    ColorTone,
    ProfileNameFormat,
    ProfilePositionFormat,
    ErrorField,
    DepartmentField,
    SpaceField,
    BotField,
    DepartmentListResponse,
    SpaceResponse,
    BotResponse,
)
from kakaowork.command import (
    departments,
    spaces,
    bots,
)


class TestDepartmentsCommand:
    def test_departments_list_success(self, mocker: MockerFixture, cli_runner: CliRunner):
        resp = DepartmentListResponse(
            success=True,
            departments=[DepartmentField(
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
            )]
        )
        mocker.patch('kakaowork.client.Kakaowork.Departments.list', return_value=resp)

        res = cli_runner.invoke(departments, ['list'])
        assert res.exit_code == 0
        assert res.output == 'ID:\t\t1\nName:\t\tname\nCode:\t\tcode\nUser count:\t1\n'

    def test_departments_list_error(self, mocker: MockerFixture, cli_runner: CliRunner):
        resp = DepartmentListResponse(
            success=False,
            error=ErrorField(code=ErrorCode.UNAUTHORIZED, message='message'),
        )
        mocker.patch('kakaowork.client.Kakaowork.Departments.list', return_value=resp)

        res = cli_runner.invoke(departments, ['list'])
        assert res.exit_code == 1
        assert res.output == 'Error code:\tunauthorized\nMessage:\tmessage\n'


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
            )
        )
        mocker.patch('kakaowork.client.Kakaowork.Spaces.info', return_value=resp)

        res = cli_runner.invoke(spaces, ['info'])
        assert res.exit_code == 0
        assert res.output == (
            "ID:\t1\nOrgID:\t1\nName:\tname\nColor code:\tdefault\nColor tone:\tlight\nPermitted ext:\t['*']\n"
            "Profile name format:\tname_nickname\nProfile position format:\tposition\nLogo URL:\thttp://localhost/image.png\n"
        )

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

        res = cli_runner.invoke(bots, ['info'])
        assert res.exit_code == 0
        assert res.output == 'ID:\t1\nName:\tname\nStatus:\tactivated\n'

    def test_bots_info_error(self, mocker: MockerFixture, cli_runner: CliRunner):
        response = BotResponse(
            success=False,
            error=ErrorField(code=ErrorCode.UNAUTHORIZED, message='message'),
        )
        mocker.patch('kakaowork.client.Kakaowork.Bots.info', return_value=response)

        res = cli_runner.invoke(bots, ['info'])
        assert res.exit_code == 1
        assert res.output == 'Error code:\tunauthorized\nMessage:\tmessage\n'
