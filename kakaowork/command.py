import os
from datetime import datetime
from typing import Optional, Tuple

import click

from kakaowork.consts import StrEnum
from kakaowork.client import Kakaowork
from kakaowork.models import (
    BaseResponse,
    UserListResponse,
    ConversationListResponse,
    DepartmentListResponse,
)


class CLIOptions:
    def __init__(self) -> None:
        self.app_key: str = ''


def _echo(ctx: click.Context, resp: BaseResponse) -> None:
    click.echo(click.style(resp.to_plain(), fg=None if resp.success else 'red'))
    ctx.exit(0 if resp.success else 1)


@click.group(name='kakaowork')
@click.pass_context
@click.option('-k', '--app-key', default=os.environ.get('KAKAOWORK_APP_KEY'))
def cli(ctx: click.Context, app_key: str):
    if not app_key:
        click.echo(click.style('No app key! Please pass your app key using option(-k, --app-key) or environment variable($KAKAOWORK_APP_KEY)', fg='red'))
        ctx.exit(1)
    ctx.ensure_object(CLIOptions)
    ctx.obj.app_key = app_key


@cli.group()
@click.pass_context
def users(ctx: click.Context):
    ctx.ensure_object(CLIOptions)


@users.command(name='list', help="Show a list of details of users belonging to the workspace")
@click.pass_context
@click.option('-l', '--limit', type=int, default=10)
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


@users.command(name='find', help="Show details of a user by identifier (ID, Email, Mobile)")
@click.pass_context
@click.option('-u', '--user-id', type=int)
@click.option('-e', '--email')
@click.option('-m', '--mobile')
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


@users.command(name='set', help="Change the user's status (working time, vacation time)")
@click.pass_context
@click.argument('user_id', type=int)
@click.option('-wt', '--work-time', nargs=2, type=click.DateTime())
@click.option('-vt', '--vacation-time', nargs=2, type=click.DateTime())
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


@cli.group()
@click.pass_context
def conversations(ctx: click.Context):
    ctx.ensure_object(CLIOptions)


@conversations.command(name='open')
@click.pass_context
@click.argument('user_ids', nargs=-1, type=int)
def conversations_open(ctx: click.Context, user_ids: Tuple[int, ...]):
    opts: CLIOptions = ctx.obj
    r = Kakaowork(app_key=opts.app_key).conversations.open(user_ids=list(user_ids))
    _echo(ctx, r)


@conversations.command(name='list')
@click.pass_context
@click.option('-l', '--limit', type=int, default=10)
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


@conversations.command(name='users')
@click.pass_context
@click.argument('conversation_id', type=int)
def conversations_users(ctx: click.Context, conversation_id: int):
    opts: CLIOptions = ctx.obj
    client = Kakaowork(app_key=opts.app_key)
    r = client.conversations.users(conversation_id=conversation_id)
    _echo(ctx, r)


@conversations.command(name='invite')
@click.pass_context
@click.argument('conversation_id', type=int)
@click.argument('user_ids', nargs=-1, type=int)
def conversations_invite(ctx: click.Context, conversation_id: int, user_ids: Tuple[int, ...]):
    opts: CLIOptions = ctx.obj
    client = Kakaowork(app_key=opts.app_key)
    r = client.conversations.invite(conversation_id=conversation_id, user_ids=list(user_ids))
    _echo(ctx, r)


@conversations.command(name='kick')
@click.pass_context
@click.argument('conversation_id', type=int)
@click.argument('user_ids', nargs=-1, type=int)
def conversations_kick(ctx: click.Context, conversation_id: int, user_ids: Tuple[int, ...]):
    opts: CLIOptions = ctx.obj
    client = Kakaowork(app_key=opts.app_key)
    r = client.conversations.kick(conversation_id=conversation_id, user_ids=list(user_ids))
    _echo(ctx, r)


@cli.group()
@click.pass_context
def messages(ctx: click.Context):
    ctx.ensure_object(CLIOptions)


@messages.command(name='send')
@click.pass_context
@click.argument('conversation_id', type=int)
@click.argument('text', type=str)
# TODO: block should be one of jsonable or key=value with space deplimiter
# @click.option('-b', '--block', 'blocks', multiple=True)
def messages_send(ctx: click.Context, conversation_id: int, text: str):
    opts: CLIOptions = ctx.obj
    r = Kakaowork(app_key=opts.app_key).messages.send(conversation_id=conversation_id, text=text)
    _echo(ctx, r)


@cli.group()
@click.pass_context
def departments(ctx: click.Context):
    ctx.ensure_object(CLIOptions)


@departments.command(name='list')
@click.pass_context
@click.option('-l', '--limit', type=int, default=10)
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


@cli.group()
@click.pass_context
def spaces(ctx: click.Context):
    ctx.ensure_object(CLIOptions)


@spaces.command(name='info')
@click.pass_context
def spaces_info(ctx: click.Context):
    opts: CLIOptions = ctx.obj
    r = Kakaowork(app_key=opts.app_key).spaces.info()
    _echo(ctx, r)


@cli.group()
@click.pass_context
def bots(ctx: click.Context):
    ctx.ensure_object(CLIOptions)


@bots.command(name='info')
@click.pass_context
def bots_info(ctx: click.Context):
    opts: CLIOptions = ctx.obj
    r = Kakaowork(app_key=opts.app_key).bots.info()
    _echo(ctx, r)
