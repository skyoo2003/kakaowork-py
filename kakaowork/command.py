import os
import sys
from argparse import ArgumentParser, _SubParsersAction
from typing import Type

from kakaowork.client import Kakaowork


class CLI:
    def __init__(self: 'CLI'):
        self.parser = ArgumentParser(
            prog='kakaowork',
            description='Kakaowork CLI',
        )
        self.parser.add_argument('-k', '--app-key', default=os.environ.get('KAKAOWORK_APP_KEY'), help='')
        self.parser.add_argument('-o', '--output', default=None, choices=['json', 'yaml'], help='')

        self.subparsers = self.parser.add_subparsers(dest='command')
        self._create_users_parser()
        self._create_conversations_parser()
        self._create_messages_parser()
        self._create_departments_parser()
        self._create_spaces_parser()
        self._create_bots_parser()

    def _create_users_parser(self):
        users_parser = self.subparsers.add_parser(name='users')
        users_verb_parser = users_parser.add_subparsers(dest='verb')

        users_list_parser = users_verb_parser.add_parser(name='list', help="Show a list of details of users belonging to the workspace")
        users_list_parser.add_argument('-n', '--size', type=int, default=10, help="A page size")

        users_find_parser = users_verb_parser.add_parser(name='find', help='Show details of a user by identifier (ID, Email, Mobile)')
        users_set_parser = users_verb_parser.add_parser(name='set', help="Change the user's status (working time, vacation time)")

    def _create_conversations_parser(self):
        conversations_parser = self.subparsers.add_parser(name='conversations')
        conversations_verb_parser = conversations_parser.add_subparsers(dest='verb')
        conversations_open_parser = conversations_verb_parser.add_parser(name='open')
        conversations_list_parser = conversations_verb_parser.add_parser(name='list')
        conversations_users_parser = conversations_verb_parser.add_parser(name='users')
        conversations_invite_parser = conversations_verb_parser.add_parser(name='invite')
        conversations_kick_parser = conversations_verb_parser.add_parser(name='kick')

    def _create_messages_parser(self):
        messages_parser = self.subparsers.add_parser(name='messages')
        messages_verb_parser = messages_parser.add_subparsers(dest='verb')
        messages_send_parser = messages_verb_parser.add_parser(name='send')

    def _create_departments_parser(self):
        departments_parser = self.subparsers.add_parser(name='departments')
        departments_verb_parser = departments_parser.add_subparsers(dest='verb')
        departments_list_parser = departments_verb_parser.add_parser(name='list')

    def _create_spaces_parser(self):
        spaces_parser = self.subparsers.add_parser(name='spaces')
        spaces_verb_parser = spaces_parser.add_subparsers(dest='verb')
        spaces_info_parser = spaces_verb_parser.add_parser(name='info')

    def _create_bots_parser(self):
        bots_parser = self.subparsers.add_parser(name='bots')
        bots_verb_parser = bots_parser.add_subparsers(dest='verb')
        bots_info_parser = bots_verb_parser.add_parser(name='info')

    def run(self):
        args = self.parser.parse_args()
        if not args.app_key:
            sys.exit("No app key")
        client = Kakaowork(app_key=args.app_key)
        print(args)
        if args.command == 'users':
            r = getattr(client.users, args.verb)()
            print(r)
