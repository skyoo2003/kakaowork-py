import json
from shlex import shlex
from datetime import datetime
from typing import Union, Any, Dict, Sequence

from pytz import utc

from kakaowork.consts import KST, BOOL_STRS, TRUE_STRS


def is_bool(text: Union[str, bytes]) -> bool:
    """Whether a string can be cast to a bool type.

    Args:
        text: A text to check type

    Returns:
        True if it can be cast to a bool type, False otherwise.

    Examples:
        >>> is_bool('true')
        True
        >>> is_bool('yes')
        True
        >>> is_bool('123')
        False
    """
    s = text.decode('utf-8') if isinstance(text, bytes) else text
    return s.strip().lower() in BOOL_STRS


def is_int(text: Union[str, bytes]) -> bool:
    """Whether a string can be cast to an int type.

    Args:
        text: A text to check type

    Returns:
        True if it can be cast to an int type, False otherwise.

    Examples:
        >>> is_int('123')
        True
        >>> is_int('1.0')
        False
    """
    s = text.decode('utf-8') if isinstance(text, bytes) else text
    try:
        int(s)
    except ValueError:
        return False
    return True


def is_float(text: Union[str, bytes]) -> bool:
    """Whether a string can be cast to a float type.

    Args:
        text: A text to check type

    Returns:
        True if it can be cast to a float type, False otherwise.

    Examples:
        >>> is_float('1.0')
        True
        >>> is_float('123')
        False
    """
    s = text.decode('utf-8') if isinstance(text, bytes) else text
    try:
        return str(float(s)) == s
    except ValueError:
        return False


def text2bool(text: Union[str, bytes]) -> bool:
    """Returns the text as a boolean value.

    Args:
        text: A text to be cast as a boolean type.

    Returns:
        True if it can be cast to a boolean type and its value is true, False otherwise.

    Examples:
        >>> text2bool('true')
        True
        >>> text2bool('yes')
        True
        >>> text2bool('false')
        False
        >>> text2bool('123')
        False
    """
    s = text.decode('utf-8') if isinstance(text, bytes) else text
    return s.strip().lower() in TRUE_STRS


def text2dict(text: Union[str, bytes]) -> Union[Dict[str, Any], Sequence[Any]]:
    """Returns the text as a JSON object or array.

    Args:
        text: A text to be cast as a JSON object or array

    Returns:
        A value of Python dict or sequence type

    Examples:
        >>> text2dict('{}')
        {}
        >>> text2dict('{"key": "value"}')
        {'key': 'value'}
        >>> text2dict('[1, 2, 3]')
        [1, 2, 3]
    """
    json_str = text.decode('utf-8') if isinstance(text, bytes) else text
    return json.loads(json_str)


def exist_kv(key: str, node: Dict[str, Any]) -> bool:
    """Returns whether a key and its value exist.

    Args:
        key: A key of a dict
        node: dict node

    Returns:
        True if a key and its value exist, False otherwise.

    Examples:
        >>> exist_kv('', {})
        False
        >>> exist_kv('key', {'key': 'value'})
        True
    """
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


def command_aliases() -> Dict[str, str]:
    from kakaowork.command import users, conversations, messages, departments, spaces, bots
    aliases: Dict[str, str] = {}
    aliases.update({alias: users.name for alias in ('user', )})
    aliases.update({alias: conversations.name
                    for alias in (
                        'conversation',
                        'conv',
                    )})
    aliases.update({alias: messages.name
                    for alias in (
                        'message',
                        'msg',
                    )})
    aliases.update({alias: departments.name
                    for alias in (
                        'department',
                        'dept',
                    )})
    aliases.update({alias: spaces.name for alias in ('space', )})
    aliases.update({alias: bots.name for alias in ('bot', )})
    return aliases


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
