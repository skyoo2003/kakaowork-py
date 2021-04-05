from enum import Enum


class StrEnum(str, Enum):
    """
    String enumeration type
    """
    pass


BASE_URL = 'api.kakaowork.com'
BASE_PATH_USERS = '/v1/users'
BASE_PATH_CONVERSATIONS = '/v1/conversations'
