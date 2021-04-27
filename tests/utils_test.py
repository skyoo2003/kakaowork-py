from datetime import datetime

from pytz import utc

from kakaowork.consts import KST
from kakaowork.utils import text2dict, exist_kv, to_kst, normalize_token, command_aliases


def test_text2dict():
    assert text2dict('') == {}
    assert text2dict(b'') == {}
    assert text2dict('{"key": "value"}') == {"key": "value"}
    assert text2dict(b'{"key": "value"}') == {"key": "value"}


def test_exist_kv():
    assert exist_kv('', {"key": "value"}) is False
    assert exist_kv('key', {}) is False
    assert exist_kv('key', {"key": None}) is False
    assert exist_kv('key', {"key": ""}) is False
    assert exist_kv('key', {"key": "value"}) is True


def test_to_kst():
    assert to_kst(1617889170) == KST.localize(datetime(2021, 4, 8, 22, 39, 30))
    assert to_kst(1609426800) == KST.localize(datetime(2021, 1, 1, 0, 0, 0))
    assert to_kst(datetime(2021, 4, 8, 22, 39, 30)) == KST.localize(datetime(2021, 4, 8, 22, 39, 30))
    assert to_kst(datetime(2021, 4, 8, 13, 39, 30, tzinfo=utc)) == KST.localize(datetime(2021, 4, 8, 22, 39, 30))


def test_normalize_token():
    assert normalize_token('') == ''
    assert normalize_token('--to-str') == '--to-str'
    assert normalize_token('--TO-STR') == '--to-str'
    assert normalize_token('--to_str') == '--to-str'
    assert normalize_token('--TO_STR') == '--to-str'


def test_command_aliases():
    assert command_aliases() == {
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
