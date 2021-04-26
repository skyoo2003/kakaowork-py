import json
from abc import ABC, abstractclassmethod
from datetime import datetime
from typing import Optional, NamedTuple, Union, Any, Dict, List

from pytz import utc, timezone

from kakaowork.consts import StrEnum
from kakaowork.blockkit import Block, BlockType
from kakaowork.exceptions import NoValueError
from kakaowork.utils import text2dict, exist_kv, to_kst


def json_default(value: Any) -> Any:
    if isinstance(value, datetime):
        return int(value.timestamp())
    raise TypeError('not JSON serializable')


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


class ConversationType(StrEnum):
    DM = 'dm'
    GROUP = 'group'


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

    def to_dict(self) -> Dict[str, Any]:
        return self._asdict()

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'ErrorField':
        if not value:
            raise NoValueError('No value to type cast')
        return cls(**dict(
            value,
            code=ErrorCode(value['code']) if exist_kv('code', value) else None,
        ))


class UserIdentificationField(NamedTuple):
    type: str
    value: str

    def to_dict(self) -> Dict[str, Any]:
        return self._asdict()

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'UserIdentificationField':
        if not value:
            raise NoValueError('No value to type cast')
        return cls(**dict(value))


class UserField(NamedTuple):
    id: str
    space_id: str
    name: str
    identifications: Optional[List[UserIdentificationField]] = None
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

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            self._asdict(),
            identifications=[uid.to_dict() for uid in self.identifications] if self.identifications else None,
        )

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'UserField':
        if not value:
            raise NoValueError('No value to type cast')
        return cls(**dict(
            value,
            identifications=[UserIdentificationField.from_dict(item) for item in value['identifications']] if exist_kv('identifications', value) else None,
            work_start_time=to_kst(value['work_start_time']) if exist_kv('work_start_time', value) else None,
            work_end_time=to_kst(value['work_end_time']) if exist_kv('work_end_time', value) else None,
            vacation_start_time=to_kst(value['vacation_start_time']) if exist_kv('vacation_start_time', value) else None,
            vacation_end_time=to_kst(value['vacation_end_time']) if exist_kv('vacation_end_time', value) else None,
        ))


class ConversationField(NamedTuple):
    id: str
    type: ConversationType
    users_count: int
    avatar_url: Optional[str] = None
    name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self._asdict()

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'ConversationField':
        if not value:
            raise NoValueError('No value to type cast')
        return cls(**dict(
            value,
            type=ConversationType(value['type']),
        ))


class MessageField(NamedTuple):
    id: str
    text: str
    user_id: str
    conversation_id: int
    send_time: datetime
    update_time: datetime
    blocks: Optional[List[Block]] = None

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            self._asdict(),
            blocks=[b.to_dict() for b in self.blocks] if self.blocks else None,
        )

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'MessageField':
        if not value:
            raise NoValueError('No value to type cast')

        blocks: List[Block] = []
        if exist_kv('blocks', value):
            for kv in value['blocks']:
                block_cls = BlockType.block_cls(kv['type'])
                block = block_cls(**{key: value for key, value in kv.items() if key != 'type'})
                blocks.append(block)
        return cls(**dict(
            value,
            send_time=to_kst(value['send_time']) if exist_kv('send_time', value) else None,
            update_time=to_kst(value['update_time']) if exist_kv('update_time', value) else None,
            blocks=blocks,
        ))


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

    def to_dict(self) -> Dict[str, Any]:
        return self._asdict()

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'DepartmentField':
        if not value:
            raise NoValueError('No value to type cast')
        return cls(**dict(value))


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

    def to_dict(self) -> Dict[str, Any]:
        return self._asdict()

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'SpaceField':
        if not value:
            raise NoValueError('No value to type cast')
        return cls(**dict(
            value,
            color_tone=ColorTone(value['color_tone']),
            profile_name_format=ProfileNameFormat(value['profile_name_format']),
            profile_position_format=ProfilePositionFormat(value['profile_position_format']),
        ))


class BotField(NamedTuple):
    bot_id: int
    title: str
    status: BotStatus

    def to_dict(self) -> Dict[str, Any]:
        return self._asdict()

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'BotField':
        if not value:
            raise NoValueError('No value to type cast')
        return cls(**dict(
            value,
            status=BotStatus(value['status']),
        ))


class BaseResponse(ABC, object):
    def __init__(self, *, success: Optional[bool] = None, error: Optional[ErrorField] = None):
        self.success = success if success is not None else True
        self.error = error

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return str(self)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, BaseResponse):
            return False
        return self.to_dict() == value.to_dict()

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=json_default)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'success': self.success,
            'error': self.error.to_dict() if self.error else None,
        }

    def to_plain(self) -> str:
        if self.error:
            return '\n'.join([
                f'Error code:\t{self.error.code}',
                f'Message:\t{self.error.message}',
            ])
        return 'OK'

    @classmethod
    def from_json(cls, value: Union[str, bytes]) -> 'BaseResponse':
        data = text2dict(value)
        return cls(**dict(
            data,
            error=ErrorField.from_dict(data['error']) if exist_kv('error', data) else None,
        ))


class UserResponse(BaseResponse):
    def __init__(self, *, success: Optional[bool] = None, error: Optional[ErrorField] = None, user: Optional[UserField] = None):
        super().__init__(success=success, error=error)
        self.user = user

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            super().to_dict(),
            user=self.user.to_dict() if self.user else None,
        )

    def to_plain(self) -> str:
        if self.user:
            return '\n'.join([
                f'ID:\t{self.user.id}',
                f'Name:\t{self.user.name}',
                f'Nickname:\t{self.user.nickname}',
                f'Department:\t{self.user.department}',
                f'Position:\t{self.user.position}',
                f'Responsibility:\t{self.user.responsibility}',
                f'Tels:\t{self.user.tels}',
                f'Mobiles:\t{self.user.mobiles}',
                f'Work start time:\t{self.user.work_start_time}',
                f'Work end time:\t{self.user.work_end_time}',
                f'Vacation start time:\t{self.user.vacation_start_time}',
                f'Vacation end time:\t{self.user.vacation_end_time}',
            ])
        return super().to_plain()

    @classmethod
    def from_json(cls, value: Union[str, bytes]) -> 'UserResponse':
        data = text2dict(value)
        r = cls(**dict(
            data,
            error=ErrorField.from_dict(data['error']) if exist_kv('error', data) else None,
            user=UserField.from_dict(data['user']) if exist_kv('user', data) else None,
        ))
        return r


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

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            super().to_dict(),
            cursor=self.cursor,
            users=[u.to_dict() for u in self.users] if self.users else None,
        )

    def to_plain(self) -> str:
        if self.users:
            outs = []
            for user in self.users:
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
        return super().to_plain()

    @classmethod
    def from_json(cls, value: Union[str, bytes]) -> 'UserListResponse':
        data = text2dict(value)
        return cls(**dict(
            data,
            error=ErrorField.from_dict(data['error']) if exist_kv('error', data) else None,
            users=[UserField.from_dict(node) for node in data['users']] if exist_kv('users', data) else None,
        ))


class ConversationResponse(BaseResponse):
    def __init__(self, *, success: Optional[bool] = None, error: Optional[ErrorField] = None, conversation: Optional[ConversationField] = None):
        super().__init__(success=success, error=error)
        self.conversation = conversation

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            super().to_dict(),
            conversation=self.conversation.to_dict() if self.conversation else None,
        )

    def to_plain(self) -> str:
        if self.conversation:
            return '\n'.join([
                f'ID:\t{self.conversation.id}',
                f'Type:\t{self.conversation.type}',
                f'Name:\t{self.conversation.name}',
                f'Avatar URL:\t{self.conversation.avatar_url}',
            ])
        return super().to_plain()

    @classmethod
    def from_json(cls, value: Union[str, bytes]) -> 'ConversationResponse':
        data = text2dict(value)
        return cls(**dict(
            data,
            error=ErrorField.from_dict(data['error']) if exist_kv('error', data) else None,
            conversation=ConversationField.from_dict(data['conversation']) if exist_kv('conversation', data) else None,
        ))


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

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            super().to_dict(),
            cursor=self.cursor,
            conversations=[c.to_dict() for c in self.conversations] if self.conversations else None,
        )

    def to_plain(self) -> str:
        if self.conversations:
            outs = []
            for conversation in self.conversations:
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
    def from_json(cls, value: Union[str, bytes]) -> 'ConversationListResponse':
        data = text2dict(value)
        return cls(**dict(
            data,
            error=ErrorField.from_dict(data['error']) if exist_kv('error', data) else None,
            conversations=[ConversationField.from_dict(node) for node in data['conversations']] if exist_kv('conversations', data) else None,
        ))


class MessageResponse(BaseResponse):
    def __init__(self, *, success: Optional[bool] = None, error: Optional[ErrorField] = None, message: Optional[MessageField] = None):
        super().__init__(success=success, error=error)
        self.message = message

    def to_dict(self):
        return dict(
            super().to_dict(),
            message=self.message.to_dict() if self.message else None,
        )

    def to_plain(self):
        if self.message:
            return '\n'.join([
                f'ID:\t{self.message.id}',
                f'Conversation ID:\t{self.message.conversation_id}',
                f'Send time:\t{self.message.send_time}',
                f'Update time:\t{self.message.update_time}',
                f'Text:\t{self.message.text}',
                f'Blocks:\t{len(self.message.blocks) if self.message.blocks else "-"}',
            ])
        return super().to_plain()

    @classmethod
    def from_json(cls, value: Union[str, bytes]) -> 'MessageResponse':
        data = text2dict(value)
        return cls(**dict(
            data,
            error=ErrorField.from_dict(data['error']) if exist_kv('error', data) else None,
            message=MessageField.from_dict(data['message']) if exist_kv('message', data) else None,
        ))


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
        return dict(
            super().to_dict(),
            cursor=self.cursor,
            departments=[d.to_dict() for d in self.departments] if self.departments else None,
        )

    def to_plain(self) -> str:
        if self.departments:
            outs = []
            for department in self.departments:
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
        data = text2dict(value)
        return cls(**dict(
            data,
            error=ErrorField.from_dict(data['error']) if exist_kv('error', data) else None,
            departments=[DepartmentField.from_dict(node) for node in data['departments']] if exist_kv('departments', data) else None,
        ))


class SpaceResponse(BaseResponse):
    def __init__(self, *, success: Optional[bool] = None, error: Optional[ErrorField] = None, space: Optional[SpaceField] = None):
        super().__init__(success=success, error=error)
        self.space = space

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            super().to_dict(),
            space=self.space.to_dict() if self.space else None,
        )

    def to_plain(self) -> str:
        if self.space:
            return '\n'.join([
                f'ID:\t{self.space.id}',
                f'OrgID:\t{self.space.kakaoi_org_id}',
                f'Name:\t{self.space.name}',
                f'Color code:\t{self.space.color_code}',
                f'Color tone:\t{self.space.color_tone}',
                f'Permitted ext:\t{self.space.permitted_ext}',
                f'Profile name format:\t{self.space.profile_name_format}',
                f'Profile position format:\t{self.space.profile_position_format}',
                f'Logo URL:\t{self.space.logo_url}',
            ])
        return super().to_plain()

    @classmethod
    def from_json(cls, value: Union[str, bytes]) -> 'SpaceResponse':
        data = text2dict(value)
        return cls(**dict(
            data,
            error=ErrorField.from_dict(data['error']) if exist_kv('error', data) else None,
            space=SpaceField.from_dict(data['space']) if exist_kv('space', data) else None,
        ))


class BotResponse(BaseResponse):
    def __init__(self, *, success: Optional[bool] = None, error: Optional[ErrorField] = None, info: Optional[BotField] = None):
        super().__init__(success=success, error=error)
        self.info = info

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            super().to_dict(),
            info=self.info.to_dict() if self.info else None,
        )

    def to_plain(self) -> str:
        if self.info:
            return '\n'.join([
                f'ID:\t{self.info.bot_id}',
                f'Name:\t{self.info.title}',
                f'Status:\t{self.info.status}'
            ])
        return super().to_plain()

    @classmethod
    def from_json(cls, value: Union[str, bytes]) -> 'BotResponse':
        data = text2dict(value)
        return cls(**dict(
            data,
            error=ErrorField.from_dict(data['error']) if exist_kv('error', data) else None,
            info=BotField.from_dict(data['info']) if exist_kv('info', data) else None,
        ))
