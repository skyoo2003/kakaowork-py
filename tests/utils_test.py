from datetime import datetime

import pytest
from pytz import utc

from kakaowork.blockkit import DividerBlock
from kakaowork.consts import KST
from kakaowork.utils import (is_bool, is_int, is_float, text2bool, text2dict, exist_kv, to_kst, normalize_token, command_aliases, parse_kv_pairs, json_default)


def test_is_bool():
    assert is_bool('') is False
    assert is_bool(b'') is False
    assert is_bool('abc') is False
    assert is_bool('true') is True
    assert is_bool('yes') is True
    assert is_bool('y') is True
    assert is_bool('false') is True
    assert is_bool('no') is True
    assert is_bool('n') is True


def test_is_int():
    assert is_int('') is False
    assert is_int('abc') is False
    assert is_int('-1.0') is False
    assert is_int('5.0') is False
    assert is_int('1') is True
    assert is_int('-5') is True


def test_is_float():
    assert is_float('') is False
    assert is_float('abc') is False
    assert is_float('1') is False
    assert is_float('-5') is False
    assert is_float('1.0') is True
    assert is_float('-5.4') is True


def test_text2bool():
    assert text2bool('') is False
    assert text2bool(b'') is False
    assert text2bool('true') is True
    assert text2bool('yes') is True
    assert text2bool('y') is True
    assert text2bool('false') is False
    assert text2bool('no') is False
    assert text2bool('n') is False


def test_text2dict():
    with pytest.raises(ValueError):
        text2dict('')
    with pytest.raises(ValueError):
        text2dict(b'')
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


def test_parse_kv_pairs():
    assert parse_kv_pairs('') == {}
    assert parse_kv_pairs('key=value') == {'key': 'value'}
    assert parse_kv_pairs("key1=value1 key2='value2,still_value2,not_key1=\"not_value1\"'") == {
        'key1': 'value1',
        'key2': 'value2,still_value2,not_key1="not_value1"',
    }
    assert parse_kv_pairs('subsystem="syslog-ng" message="I/O error occurred while writing; fd=20, error=\'Invalid argument (22)\'" retcode=1') == {
        'subsystem': 'syslog-ng',
        'message': "I/O error occurred while writing; fd=20, error='Invalid argument (22)'",
        'retcode': 1,
    }


def test_json_default():
    assert json_default(DividerBlock()) == {'type': 'divider'}
    assert json_default(datetime(2021, 1, 1, 0, 0, 0, tzinfo=utc)) == 1609459200
    with pytest.raises(TypeError):
        json_default(1234)
    with pytest.raises(TypeError):
        json_default('abc')
