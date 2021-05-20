import os
import json
from datetime import datetime
from typing import Optional, Tuple, Any, Dict

import click

from kakaowork.consts import StrEnum, Limit
from kakaowork.client import Kakaowork
from kakaowork.models import (
    BaseResponse,
    UserListResponse,
    ConversationListResponse,
    DepartmentListResponse,
)
from kakaowork.blockkit import Block, BlockType
from kakaowork.utils import normalize_token, parse_kv_pairs


def _command_aliases() -> Dict[str, str]:
    aliases: Dict[str, str] = {}
    aliases.update({alias: 'users' for alias in ('user', )})
    aliases.update({alias: 'conversations'
                    for alias in (
                        'conversation',
                        'conv',
                    )})
    aliases.update({alias: 'messages'
                    for alias in (
                        'message',
                        'msg',
                    )})
    aliases.update({alias: 'departments'
                    for alias in (
                        'department',
                        'dept',
                    )})
    aliases.update({alias: 'spaces' for alias in ('space', )})
    aliases.update({alias: 'bots' for alias in ('bot', )})
    return aliases


class AliasedGroup(click.Group):
    def get_command(self, ctx: click.Context, cmd_name: str):
        # Return a command immediately if exact match
        command = super().get_command(ctx, cmd_name)
        if command is not None:
            return command

        # Returns a command if it matches an alias
        aliases = _command_aliases()
        if cmd_name in aliases:
            actual_cmd_name = aliases[cmd_name]
            return super().get_command(ctx, actual_cmd_name)

        ctx.fail(f"No such command: {cmd_name}.")


class BlockKitParamType(click.ParamType):
    name = 'blockkit'

    def convert(self, value: str, param: Optional[click.Parameter], ctx: Optional[click.Context]) -> Any:
        if value.startswith('@') and value.endswith('.json'):  # Load from a JSON file.
            with open(value[1:], 'r') as f:
                data = json.load(f)
        elif value[0] in ['[', '{']:  # Load form JSON string.
            data = json.loads(value)
        else:  # Parse key-value pairs with space separators
            data = parse_kv_pairs(value)
        block_cls = BlockType.block_cls(data['type'])
        return block_cls.from_dict(data)

    def __repr__(self) -> str:
        return 'BLOCKKIT'


class CLIOptions:
    def __init__(self) -> None:
        self.app_key: str = ''


def _echo(ctx: click.Context, resp: BaseResponse) -> None:
    click.echo(click.style(resp.to_plain(), fg=None if resp.success else 'red'))
    ctx.exit(0 if resp.success else 1)


BLOCKKIT = BlockKitParamType()


@click.group(name='kakaowork', cls=AliasedGroup, context_settings=dict(token_normalize_func=normalize_token), help='Kakaowork CLI using Client API')
@click.pass_context
@click.option('-k', '--app-key', default=os.environ.get('KAKAOWORK_APP_KEY'), help='Kakaowork app key. See https://docs.kakaoi.ai/kakao_work/botdevguide')
def cli(ctx: click.Context, app_key: str):
    if not app_key:
        click.echo(click.style('No app key! Please pass your app key using option(-k, --app-key) or environment variable($KAKAOWORK_APP_KEY)', fg='red'))
        ctx.exit(1)
    opts: CLIOptions = ctx.ensure_object(CLIOptions)
    opts.app_key = app_key


@cli.group(help='Manages users in a workspace')
@click.pass_context
def users(ctx: click.Context):
    ctx.ensure_object(CLIOptions)


@users.command(name='list', help="Show a list of details of users belonging to a workspace")
@click.pass_context
@click.option('-l', '--limit', type=click.IntRange(Limit.MIN, Limit.MAX), default=Limit.DEFAULT, show_default=True, help='Maximum paging size')
def users_list(ctx: click.Context, limit: int):
    opts: CLIOptions = ctx.obj
    client = Kakaowork(app_key=opts.app_key)
    r = client.users.list(limit=limit)
    if not r.success:
        return _echo(ctx, r)

    def _generate_output(resp: UserListResponse):
        yield resp.to_plain()
        while resp.cursor is not None:
            resp = client.users.list(cursor=resp.cursor)
            yield resp.to_plain()

    click.echo_via_pager(_generate_output(r))


@users.command(name='find', help="Shows an user by ID, Email or Mobile)")
@click.pass_context
@click.option('-u', '--user-id', type=int, help='Only display the user by ID')
@click.option('-e', '--email', help='Only display the user by E-mail')
@click.option('-m', '--mobile', help='Only display the user by Mobile')
def users_find(ctx: click.Context, user_id: Optional[int] = None, email: Optional[str] = None, mobile: Optional[str] = None):
    opts: CLIOptions = ctx.obj
    client = Kakaowork(app_key=opts.app_key)

    if user_id is not None:
        r = client.users.info(user_id)
    elif email:
        r = client.users.find_by_email(email)
    elif mobile:
        r = client.users.find_by_phone_number(mobile)
    else:
        raise click.BadParameter("You must enter either '--user-id (-u)' or '--email (-e)' or '--mobile (-m)")
    _echo(ctx, r)


@users.command(name='set', help="Manages the status of a user")
@click.pass_context
@click.argument('user_id', type=int)
@click.option('-wt', '--work-time', nargs=2, type=click.DateTime(), help='Working time with start and end. e.g. 2021-01-01T10:00:00 2021-01-01T19:00:00')
@click.option('-vt', '--vacation-time', nargs=2, type=click.DateTime(), help='Vacation time with start and end. e.g. 2021-01-01T10:00:00 2021-01-05T19:00:00')
def users_set(ctx: click.Context,
              user_id: int,
              work_time: Optional[Tuple[datetime, datetime]] = None,
              vacation_time: Optional[Tuple[datetime, datetime]] = None):
    if not (work_time or vacation_time):
        raise click.BadParameter("You must enter either '--work-time (-wt)' or '--vacation-time (-vt)'")

    opts: CLIOptions = ctx.obj
    client = Kakaowork(app_key=opts.app_key)

    if work_time:
        start_time, end_time = work_time[0], work_time[1]
        r = client.users.set_work_time(user_id=user_id, work_start_time=start_time, work_end_time=end_time)
        click.echo(click.style('Set work time: ' + r.to_plain(), fg=None if r.success else 'red'))
        if not r.success:
            ctx.exit(1)

    if vacation_time:
        start_time, end_time = vacation_time[0], vacation_time[1]
        r = client.users.set_vacation_time(user_id=user_id, vacation_start_time=start_time, vacation_end_time=end_time)
        click.echo(click.style('Set vacation time: ' + r.to_plain(), fg=None if r.success else 'red'))
        if not r.success:
            ctx.exit(1)


@cli.group(help='Manages conversations in a workspace')
@click.pass_context
def conversations(ctx: click.Context):
    ctx.ensure_object(CLIOptions)


@conversations.command(name='open', help='Creates a conversation')
@click.pass_context
@click.argument('user_ids', nargs=-1, type=int)
def conversations_open(ctx: click.Context, user_ids: Tuple[int, ...]):
    opts: CLIOptions = ctx.obj
    r = Kakaowork(app_key=opts.app_key).conversations.open(user_ids=list(user_ids))
    _echo(ctx, r)


@conversations.command(name='list', help='Lists conversations')
@click.pass_context
@click.option('-l', '--limit', type=click.IntRange(Limit.MIN, Limit.MAX), default=Limit.DEFAULT, show_default=True, help='Maximum paging size')
def conversations_list(ctx: click.Context, limit: int):
    opts: CLIOptions = ctx.obj
    client = Kakaowork(app_key=opts.app_key)
    r = client.conversations.list(limit=limit)
    if not r.success:
        return _echo(ctx, r)

    def _generate_output(resp: ConversationListResponse):
        yield resp.to_plain()
        while resp.cursor is not None:
            resp = client.conversations.list(cursor=resp.cursor)
            yield resp.to_plain()

    click.echo_via_pager(_generate_output(r))


@conversations.command(name='users', help='Lists users of a conversation')
@click.pass_context
@click.argument('conversation_id', type=int)
def conversations_users(ctx: click.Context, conversation_id: int):
    opts: CLIOptions = ctx.obj
    client = Kakaowork(app_key=opts.app_key)
    r = client.conversations.users(conversation_id=conversation_id)
    _echo(ctx, r)


@conversations.command(name='invite', help='Invites one or many users to a conversation')
@click.pass_context
@click.argument('conversation_id', type=int)
@click.argument('user_ids', nargs=-1, type=int)
def conversations_invite(ctx: click.Context, conversation_id: int, user_ids: Tuple[int, ...]):
    opts: CLIOptions = ctx.obj
    client = Kakaowork(app_key=opts.app_key)
    r = client.conversations.invite(conversation_id=conversation_id, user_ids=list(user_ids))
    _echo(ctx, r)


@conversations.command(name='kick', help='Kicks one or many users from a conversation')
@click.pass_context
@click.argument('conversation_id', type=int)
@click.argument('user_ids', nargs=-1, type=int)
def conversations_kick(ctx: click.Context, conversation_id: int, user_ids: Tuple[int, ...]):
    opts: CLIOptions = ctx.obj
    client = Kakaowork(app_key=opts.app_key)
    r = client.conversations.kick(conversation_id=conversation_id, user_ids=list(user_ids))
    _echo(ctx, r)


@cli.group(help='Manages a message in a conversation')
@click.pass_context
def messages(ctx: click.Context):
    ctx.ensure_object(CLIOptions)


@messages.command(name='send', help='Sends a message in a conversation')
@click.pass_context
@click.argument('conversation_id', type=int)
@click.argument('text', type=str)
@click.option('-b', '--block', 'blocks', type=BLOCKKIT, multiple=True, help='One or many blocks to send in a message')
def messages_send(ctx: click.Context, conversation_id: int, text: str, blocks: Tuple[Block, ...]):
    opts: CLIOptions = ctx.obj
    r = Kakaowork(app_key=opts.app_key).messages.send(conversation_id=conversation_id, text=text, blocks=list(blocks))
    _echo(ctx, r)


@cli.group(help='Display departments in a workspace')
@click.pass_context
def departments(ctx: click.Context):
    ctx.ensure_object(CLIOptions)


@departments.command(name='list', help='Lists departments ina workspace')
@click.pass_context
@click.option('-l', '--limit', type=click.IntRange(Limit.MIN, Limit.MAX), default=Limit.DEFAULT, show_default=True, help='Maximum paging size')
def departments_list(ctx: click.Context, limit: int):
    opts: CLIOptions = ctx.obj
    client = Kakaowork(app_key=opts.app_key)
    r = client.departments.list(limit=limit)
    if not r.success:
        return _echo(ctx, r)

    def _generate_output(resp: DepartmentListResponse):
        yield resp.to_plain()
        while resp.cursor is not None:
            resp = client.departments.list(cursor=resp.cursor)
            yield resp.to_plain()

    click.echo_via_pager(_generate_output(r))


@cli.group(help='Shows the info of a space in a workspace')
@click.pass_context
def spaces(ctx: click.Context):
    ctx.ensure_object(CLIOptions)


@spaces.command(name='info', help='Display the info of a space')
@click.pass_context
def spaces_info(ctx: click.Context):
    opts: CLIOptions = ctx.obj
    r = Kakaowork(app_key=opts.app_key).spaces.info()
    _echo(ctx, r)


@cli.group(help='Shows the info of a bot in a workspace')
@click.pass_context
def bots(ctx: click.Context):
    ctx.ensure_object(CLIOptions)


@bots.command(name='info', help='Display the info of a bot')
@click.pass_context
def bots_info(ctx: click.Context):
    opts: CLIOptions = ctx.obj
    r = Kakaowork(app_key=opts.app_key).bots.info()
    _echo(ctx, r)
