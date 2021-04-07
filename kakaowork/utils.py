import json
from typing import Union, Any, Dict


def text2dict(text: Union[str, bytes]) -> Dict[str, Any]:
    if not text:
        return {}
    json_str = text.decode('utf-8') if isinstance(text, bytes) else text
    return json.loads(json_str)


def exist_kv(key: str, node: Dict[str, Any]) -> bool:
    if key in node and node[key]:
        return True
    return False
