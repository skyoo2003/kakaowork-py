import json
from shlex import shlex
from datetime import datetime
from typing import Union, Any, Dict

from pytz import utc

from kakaowork.consts import KST, BOOL_STRS, TRUE_STRS


def is_bool(text: Union[str, bytes]) -> bool:
    s = text.decode('utf-8') if isinstance(text, bytes) else text
    return s.strip().lower() in BOOL_STRS


def is_int(text: Union[str, bytes]) -> bool:
    s = text.decode('utf-8') if isinstance(text, bytes) else text
    try:
        int(s)
    except ValueError:
        return False
    return True


def is_float(text: Union[str, bytes]) -> bool:
    s = text.decode('utf-8') if isinstance(text, bytes) else text
    try:
        return str(float(s)) == s
    except ValueError:
        return False


def text2bool(text: Union[str, bytes]) -> bool:
    s = text.decode('utf-8') if isinstance(text, bytes) else text
    return s.strip().lower() in TRUE_STRS


def text2dict(text: Union[str, bytes]) -> Dict[str, Any]:
    json_str = text.decode('utf-8') if isinstance(text, bytes) else text
    return json.loads(json_str)


def exist_kv(key: str, node: Dict[str, Any]) -> bool:
    if key in node and node[key]:
        return True
    return False


def to_kst(timestamp: Union[int, datetime]) -> datetime:
    if isinstance(timestamp, int):
        return datetime.fromtimestamp(timestamp, tz=utc).astimezone(KST)
    elif isinstance(timestamp, datetime):
        # If the timestamp is naive then just replace tzinfo to KST
        # ref: https://docs.python.org/3/library/datetime.html#determining-if-an-object-is-aware-or-naive
        if timestamp.tzinfo is None or timestamp.tzinfo.utcoffset(timestamp) is None:
            return KST.localize(timestamp)
        else:
            return timestamp.astimezone(KST)
    raise ValueError('Unsupported timestamp type')


def normalize_token(token: str) -> str:
    token = token.lower()
    if '_' in token:
        return token.replace('_', '-')
    return token


def parse_kv_pairs(line: str) -> Dict[str, Any]:
    lexer = shlex(line, posix=True)
    lexer.wordchars += "=.-_()/:+*^&%$#@!?|{}"
    kvs: Dict[str, Any] = {}
    for token in lexer:
        key, value = token.split('=', maxsplit=1)
        if is_bool(value):
            kvs[key] = text2bool(value)
        elif is_int(value):
            kvs[key] = int(value)
        elif is_float(value):
            kvs[key] = float(value)
        else:
            kvs[key] = value
    return kvs


def json_default(value: Any) -> Any:
    from kakaowork.blockkit import Block

    if isinstance(value, Block):
        return value.to_dict()
    elif isinstance(value, datetime):
        return int(value.timestamp())
    raise TypeError('not JSON serializable')
