import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, NamedTuple, Union, Any, Dict, List

from kakaowork.consts import StrEnum
from kakaowork.blockkit import Block


class ErrorCode(StrEnum):
    INVALID_PARAMETER = 'invalid_parameter'
    INVALID_AUTHENTICATION = 'invalid_authentication'
    INVALID_REPRESENTATION = 'invalid_representation'
    INVALID_CONTENT_TYPE = 'invalid_content_type'
    API_NOT_FOUND = 'api_not_found'
    UNAUTHORIZED = 'unauthorized'
    INTERNAL_SERVER_ERROR = 'internal_server_error'
    TOO_MANY_REQUESTS = 'too_many_requests'
    EXPIRED_AUTHENTICATION = 'expired_authentication'
    MISSING_PARAMETER = 'missing_parameter'


class ColorTone(StrEnum):
    LIGHT = 'light'
    DARK = 'dark'


class ProfileNameFormat(StrEnum):
    NAME_ONLY = 'name_only'
    NAME_NICKNAME = 'name_nickname'
    NICKNAME_NAME = 'nickname_name'


class ProfilePositionFormat(StrEnum):
    POSITION = 'position'
    RESPONSIBILITY = 'responsibility'


class BotStatus(StrEnum):
    ACTIVATED = 'activated'
    DEACTIVATED = 'deactivated'


class ErrorField(NamedTuple):
    code: ErrorCode
    message: str


class UserField(NamedTuple):
    id: str
    space_id: str
    name: str
    nickname: Optional[str]
    avatar_url: Optional[str]
    department: Optional[str]
    position: Optional[str]
    responsibility: Optional[str]
    tels: Optional[str]
    mobiles: Optional[str]
    work_start_time: Optional[datetime]
    work_end_time: Optional[datetime]
    vacation_start_time: Optional[datetime]
    vacation_end_time: Optional[datetime]


class ConversationField(NamedTuple):
    id: str
    type: str
    users_count: int
    avatar_url: Optional[str]
    name: Optional[str]


class MessageField(NamedTuple):
    id: str
    text: str
    user_id: str
    conversation_id: int
    send_time: datetime
    update_time: datetime
    blocks: Optional[Block]


class DepartmentField(NamedTuple):
    id: str
    space_id: str
    name: str
    code: str
    user_count: int
    has_child: Optional[bool]
    depth: Optional[int]
    user_ids: Optional[List[int]]
    leader_ids: Optional[List[int]]
    ancestry: Optional[str]


class SpaceField(NamedTuple):
    id: str
    kakaoi_org_id: str
    name: str
    color_code: str
    color_tone: ColorTone
    permitted_ext: List[str]
    profile_name_format: ProfileNameFormat
    profile_position_format: ProfilePositionFormat
    logo_url: str


class BotField(NamedTuple):
    title: str
    status: BotStatus


class BaseResponse(ABC):
    def __init__(self, *, success: Optional[bool] = None, error: Optional[ErrorField] = None):
        self.success = success or False
        self.error = error

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return str(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        return {
            'success': self.success,
            'error': self.error,
        }

    @classmethod
    def from_json(cls, value: Union[str, bytes]):
        json_str = value.decode('utf-8') if isinstance(value, bytes) else value
        json_data = json.loads(json_str)
        return cls(**json_data)


class UserResponse(BaseResponse):
    def __init__(self, *, success: Optional[bool] = None, error: Optional[ErrorField] = None, user: Optional[UserField] = None):
        super().__init__(success=success, error=error)
        self.user = user

    def to_dict(self):
        return dict(user=self.user, **super().to_dict())

    @classmethod
    def from_json(cls, value: Union[str, bytes]):
        return super().from_json(value)


class UserListResponse(BaseResponse):
    def __init__(self,
                 *,
                 success: Optional[bool] = None,
                 error: Optional[ErrorField] = None,
                 cursor: Optional[str] = None,
                 users: Optional[List[UserField]] = None):
        super().__init__(success=success, error=error)
        self.cursor = cursor
        self.users = users

    def to_dict(self):
        return dict(users=self.users, cursor=self.cursor, **super().to_dict())

    @classmethod
    def from_json(cls, value: Union[str, bytes]):
        return super().from_json(value)


class ConversationResponse(BaseResponse):
    def __init__(self, *, success: Optional[bool] = None, error: Optional[ErrorField] = None, conversation: ConversationField):
        super().__init__(success=success, error=error)
        self.conversation = conversation

    def to_dict(self):
        return dict(conversation=self.conversation, **super().to_dict())

    @classmethod
    def from_json(cls, value: Union[str, bytes]):
        return super().from_json(value)


class ConversationListResponse(BaseResponse):
    def __init__(self,
                 *,
                 success: Optional[bool] = None,
                 error: Optional[ErrorField] = None,
                 cursor: Optional[str] = None,
                 conversations: Optional[List[ConversationField]] = None):
        super().__init__(success=success, error=error)
        self.cursor = cursor
        self.conversations = conversations

    def to_dict(self):
        return dict(conversations=self.conversations, cursor=self.cursor, **super().to_dict())

    @classmethod
    def from_json(cls, value: Union[str, bytes]):
        return super().from_json(value)


class MessageResponse(BaseResponse):
    def __init__(self, *, success: Optional[bool] = None, error: Optional[ErrorField] = None, message: Optional[MessageField] = None):
        super().__init__(success=success, error=error)
        self.message = message

    def to_dict(self):
        return dict(message=self.message, **super().to_dict())

    @classmethod
    def from_json(cls, value: Union[str, bytes]):
        return super().from_json(value)


class DepartmentListResponse(BaseResponse):
    def __init__(self,
                 *,
                 success: Optional[bool] = None,
                 error: Optional[ErrorField] = None,
                 cursor: Optional[str] = None,
                 departments: Optional[List[DepartmentField]] = None):
        super().__init__(success=success, error=error)
        self.cursor = cursor
        self.departments = departments

    def to_dict(self):
        return dict(departments=self.departments, cursor=self.cursor, **super().to_dict())

    @classmethod
    def from_json(cls, value: Union[str, bytes]):
        return super().from_json(value)


class SpaceResponse(BaseResponse):
    def __init__(self, *, success: Optional[bool] = None, error: Optional[ErrorField] = None, space: Optional[SpaceField] = None):
        super().__init__(success=success, error=error)
        self.space = space

    def to_dict(self):
        return dict(space=self.space, **super().to_dict())

    @classmethod
    def from_json(cls, value: Union[str, bytes]):
        return super().from_json(value)


class BotResponse(BaseResponse):
    def __init__(self, *, success: Optional[bool] = None, error: Optional[ErrorField] = None, bot: Optional[BotField] = None):
        super().__init__(success=success, error=error)
        self.bot = bot

    def to_dict(self):
        return dict(bot=self.bot, **super().to_dict())

    @classmethod
    def from_json(cls, value: Union[str, bytes]):
        return super().from_json(value)
