import json
from datetime import datetime
from typing import Union, Any, Dict

from pytz import utc

from kakaowork.consts import KST


def text2dict(text: Union[str, bytes]) -> Dict[str, Any]:
    if not text:
        return {}
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
