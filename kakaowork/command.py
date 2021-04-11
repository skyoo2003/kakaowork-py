import os
from typing import Optional

import click

from kakaowork.consts import StrEnum
from kakaowork.client import Kakaowork


class CLIOptions:
    def __init__(self):
        self.app_key: str = ''


@click.group(name='kakaowork')
@click.pass_context
@click.option('-k', '--app-key', default=os.environ.get('KAKAOWORK_APP_KEY'))
def cli(ctx, app_key):
    ctx.ensure_object(CLIOptions)
    ctx.obj.app_key = app_key
    pass


@cli.group()
@click.pass_context
def users(ctx):
    pass


@users.command(name='list', help="Show a list of details of users belonging to the workspace")
def users_list():
    pass


@users.command(name='find', help="Show details of a user by identifier (ID, Email, Mobile)")
def users_find():
    pass


@users.command(name='set', help="Change the user's status (working time, vacation time)")
def users_set():
    pass


@cli.group()
def conversations():
    pass


def conversations_open():
    pass


def conversations_list():
    pass


def conversations_users():
    pass


def conversations_invite():
    pass


def conversations_kick():
    pass


@cli.group()
def messages():
    pass


def messages_send():
    pass


@cli.group()
def departments():
    pass


def departments_list():
    pass


@cli.group()
def spaces():
    pass


def spaces_info():
    pass


@cli.group()
def bots():
    pass


def bots_info():
    pass
