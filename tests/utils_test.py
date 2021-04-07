from kakaowork.utils import text2dict, exist_kv


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
