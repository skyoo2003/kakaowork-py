import os
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog='kakaowork',
        description='Kakaowork CLI',
    )
    parser.add_argument('-k', '--app-key', default=os.environ.get('KAKAOWORK_APP_KEY'), help='')

    subparsers = parser.add_subparsers(dest='command')

    users_parser = subparsers.add_parser(name='users')
    users_verb_parser = users_parser.add_subparsers(dest='verb')
    users_info_parser = users_verb_parser.add_parser(name='info')
    users_list_parser = users_verb_parser.add_parser(name='list')

    conversations_parser = subparsers.add_parser(name='conversations')
    messages_parser = subparsers.add_parser(name='messages')
    departments_parser = subparsers.add_parser(name='departments')
    spaces_parser = subparsers.add_parser(name='spaces')
    bots_parser = subparsers.add_parser(name='bots')

    args = parser.parse_args()

    print(args)


if __name__ == '__main__':
    main()
