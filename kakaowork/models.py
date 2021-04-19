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
    identifications: Optional[List[Dict[str, Any]]] = None
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    responsibility: Optional[str] = None
    tels: Optional[str] = None
    mobiles: Optional[str] = None
    work_start_time: Optional[datetime] = None
    work_end_time: Optional[datetime] = None
    vacation_start_time: Optional[datetime] = None
    vacation_end_time: Optional[datetime] = None


class ConversationField(NamedTuple):
    id: str
    type: str
    users_count: int
    avatar_url: Optional[str] = None
    name: Optional[str] = None


class MessageField(NamedTuple):
    id: str
    text: str
    user_id: str
    conversation_id: int
    send_time: datetime
    update_time: datetime
    blocks: Optional[Block] = None


class DepartmentField(NamedTuple):
    id: str
    ids_path: str
    parent_id: str
    space_id: str
    name: str
    code: str
    user_count: int
    has_child: Optional[bool] = None
    depth: Optional[int] = None
    users_ids: Optional[List[int]] = None
    leader_ids: Optional[List[int]] = None
    ancestry: Optional[str] = None


class SpaceField(NamedTuple):
    id: int
    kakaoi_org_id: int
    name: str
    color_code: str
    color_tone: ColorTone
    permitted_ext: List[str]
    profile_name_format: ProfileNameFormat
    profile_position_format: ProfilePositionFormat
    logo_url: str


class BotField(NamedTuple):
    bot_id: int
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

    def to_dict(self) -> Dict[str, Any]:
        return {
            'success': self.success,
            'error': self.error,
        }

    def to_plain(self) -> str:
        if self.error:
            error = ErrorField(**self.error) if isinstance(self.error, dict) else self.error
            return '\n'.join([
                f'Error Code:\t{error.code}',
                f'Message:\t{error.message}',
            ])
        return 'OK'

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

    def to_plain(self):
        if self.user:
            user = UserField(**self.user) if isinstance(self.user, dict) else self.user
            return '\n'.join([
                f'ID:\t{user.id}',
                f'Name:\t{user.name}',
                f'Nickname:\t{user.nickname}',
                f'Department:\t{user.department}',
                f'Position:\t{user.position}',
                f'Responsibility:\t{user.responsibility}',
                f'Tels:\t{user.tels}',
                f'Mobiles:\t{user.mobiles}',
                f'Work start time:\t{user.work_start_time}',
                f'Work end time:\t{user.work_end_time}',
                f'Vacation start time:\t{user.vacation_start_time}',
                f'Vacation end time:\t{user.vacation_end_time}',
            ])
        return super().to_plain()

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

    def to_plain(self):
        if self.users:
            outs = []
            for user in self.users:
                print(user)
                if isinstance(user, dict):
                    user = UserField(**user)
                out = '\n'.join([
                    f'ID:\t{user.id}',
                    f'Name:\t{user.name}',
                    f'Nickname:\t{user.nickname}',
                    f'Department:\t{user.department}',
                    f'Position:\t{user.position}',
                    f'Responsibility:\t{user.responsibility}',
                    f'Tels:\t{user.tels}',
                    f'Mobiles:\t{user.mobiles}',
                    f'Work start time:\t{user.work_start_time}',
                    f'Work end time:\t{user.work_end_time}',
                    f'Vacation start time:\t{user.vacation_start_time}',
                    f'Vacation end time:\t{user.vacation_end_time}',
                ])
                outs.append(out)
            return ('\n' + '-' * 30 + '\n').join(outs)
            return '\n'.join([
                f'Users:\t{self.users}'
            ])
        return super().to_plain()

    @classmethod
    def from_json(cls, value: Union[str, bytes]):
        return super().from_json(value)


class ConversationResponse(BaseResponse):
    def __init__(self, *, success: Optional[bool] = None, error: Optional[ErrorField] = None, conversation: Optional[ConversationField] = None):
        super().__init__(success=success, error=error)
        self.conversation = conversation

    def to_dict(self):
        return dict(conversation=self.conversation, **super().to_dict())

    def to_plain(self):
        if self.conversation:
            conversation = ConversationField(**self.conversation) if isinstance(self.conversation, dict) else self.conversation
            return '\n'.join([
                f'ID:\t{conversation.id}',
                f'Type:\t{conversation.type}',
                f'Name:\t{conversation.name}',
                f'Avatar URL:\t{conversation.avatar_url}',
            ])
        return super().to_plain()

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

    def to_plain(self):
        if self.conversations:
            outs = []
            for conversation in self.conversations:
                if isinstance(conversation, dict):
                    conversation = ConversationField(**conversation)
                out = '\n'.join([
                    f'ID:\t{conversation.id}',
                    f'Type:\t{conversation.type}',
                    f'Name:\t{conversation.name}',
                    f'Avatar URL:\t{conversation.avatar_url}',
                ])
                outs.append(out)
            return ('\n' + '-' * 30 + '\n').join(outs)
        return super().to_plain()

    @classmethod
    def from_json(cls, value: Union[str, bytes]):
        return super().from_json(value)


class MessageResponse(BaseResponse):
    def __init__(self, *, success: Optional[bool] = None, error: Optional[ErrorField] = None, message: Optional[MessageField] = None):
        super().__init__(success=success, error=error)
        self.message = message

    def to_dict(self):
        return dict(message=self.message, **super().to_dict())

    def to_plain(self):
        if self.message:
            message = MessageField(**self.message) if isinstance(self.message, dict) else self.message
            return '\n'.join([
                f'ID:\t{message.id}',
                f'Conversation ID:\t{message.conversation_id}',
                f'Send time:\t{message.send_time}',
                f'Update time:\t{message.update_time}',
                f'Text:\t{message.text}',
                f'Blocks:\t{len(message.blocks) if message.blocks else "-"}',
            ])
        return super().to_plain()

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

    def to_dict(self) -> Dict[str, Any]:
        return dict(departments=self.departments, cursor=self.cursor, **super().to_dict())

    def to_plain(self) -> str:
        if self.departments:
            outs = []
            for department in self.departments:
                if isinstance(department, dict):
                    department = DepartmentField(**department)
                out = '\n'.join([
                    f'ID:\t\t{department.id}',
                    f'Name:\t\t{department.name}',
                    f'Code:\t\t{department.code}',
                    f'User count:\t{department.user_count}',
                ])
                outs.append(out)
            return ('\n' + '-' * 30 + '\n').join(outs)
        return super().to_plain()

    @classmethod
    def from_json(cls, value: Union[str, bytes]):
        return super().from_json(value)


class SpaceResponse(BaseResponse):
    def __init__(self, *, success: Optional[bool] = None, error: Optional[ErrorField] = None, space: Optional[SpaceField] = None):
        super().__init__(success=success, error=error)
        self.space = space

    def to_dict(self) -> Dict[str, Any]:
        return dict(space=self.space, **super().to_dict())

    def to_plain(self) -> str:
        if self.space:
            space = SpaceField(**self.space) if isinstance(self.space, dict) else self.space
            return '\n'.join([
                f'ID:\t{space.id}',
                f'OrgID:\t{space.kakaoi_org_id}',
                f'Name:\t{space.name}',
                f'Color code:\t{space.color_code}',
                f'Color tone:\t{space.color_tone}',
                f'Permitted ext:\t{space.permitted_ext}',
                f'Profile name format:\t{space.profile_name_format}',
                f'Profile position format:\t{space.profile_position_format}',
                f'Logo URL:\t{space.logo_url}',
            ])
        return super().to_plain()

    @classmethod
    def from_json(cls, value: Union[str, bytes]):
        return super().from_json(value)


class BotResponse(BaseResponse):
    def __init__(self, *, success: Optional[bool] = None, error: Optional[ErrorField] = None, info: Optional[BotField] = None):
        super().__init__(success=success, error=error)
        self.info = info

    def to_dict(self) -> Dict[str, Any]:
        return dict(info=self.info, **super().to_dict())

    def to_plain(self) -> str:
        if self.info:
            info = BotField(**self.info) if isinstance(self.info, dict) else self.info
            return '\n'.join([
                f'ID:\t{info.bot_id}',
                f'Name:\t{info.title}',
                f'Status:\t{info.status}'
            ])
        return super().to_plain()

    @classmethod
    def from_json(cls, value: Union[str, bytes]):
        return super().from_json(value)
