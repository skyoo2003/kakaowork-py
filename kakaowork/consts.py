from enum import Enum, IntEnum

from pytz import timezone


class StrEnum(str, Enum):
    """String enumeration type."""
    pass


class Limit(IntEnum):
    """Limit enumeration type."""
    MIN = 1
    DEFAULT = 10
    MAX = 100

    def __str__(self):
        return str(self.value)


BASE_URL = 'https://api.kakaowork.com'
BASE_PATH_USERS = '/v1/users'
BASE_PATH_CONVERSATIONS = '/v1/conversations'
BASE_PATH_MESSAGES = '/v1/messages'
BASE_PATH_DEPARTMENTS = '/v1/departments'
BASE_PATH_SPACES = '/v1/spaces'
BASE_PATH_BOTS = '/v1/bots'
BASE_PATH_BATCH = '/v1/batch'

KST = timezone('Asia/Seoul')

TRUE_STRS = ['true', 'y', 'yes']
FALSE_STRS = ['false', 'n', 'no']
BOOL_STRS = TRUE_STRS + FALSE_STRS
