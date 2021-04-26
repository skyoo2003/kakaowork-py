from datetime import datetime

from kakaowork.consts import KST
from kakaowork.utils import text2dict, exist_kv, to_kst


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
