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
