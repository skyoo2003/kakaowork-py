from enum import Enum
from datetime import timedelta

from pytz import timezone


class StrEnum(str, Enum):
    """
    String enumeration type
    """
    pass


LIMIT = 10

BASE_URL = 'https://api.kakaowork.com'
BASE_PATH_USERS = '/v1/users'
BASE_PATH_CONVERSATIONS = '/v1/conversations'
BASE_PATH_MESSAGES = '/v1/messages'
BASE_PATH_DEPARTMENTS = '/v1/departments'
BASE_PATH_SPACES = '/v1/spaces'
BASE_PATH_BOTS = '/v1/bots'

KST = timezone('Asia/Seoul')
