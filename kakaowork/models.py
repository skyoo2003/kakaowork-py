import json
import warnings
from abc import ABC, abstractclassmethod
from datetime import datetime
from typing import Optional, NamedTuple, Union, Any, Dict, List, Sequence

from pytz import utc, timezone

from kakaowork.consts import StrEnum
from kakaowork.blockkit import Block, BlockType
from kakaowork.exceptions import NoValueError, InvalidReactiveBody
from kakaowork.utils import text2json, exist_kv, to_kst, json_default


def _drop_missing(kv: Dict[str, Any], keys: Sequence[str]) -> Dict[str, Any]:
    mk: List[str] = []  # missing keys
    ret: Dict[str, Any] = {}
    for k, v in kv.items():
        if k not in keys:
            mk.append(k)
            continue
        ret[k] = v
    if mk:
        warnings.warn(f'There are missing fields: {",".join(mk)}', category=RuntimeWarning, stacklevel=2)
    return ret


class ErrorCode(StrEnum):
    # If you return the 'UNKNOWN' error code, even though it's an official error code. please report it!
    UNKNOWN = 'unknown'

    # Common error codes
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
    BAD_REQUEST = 'bad_request'

    # API specific codes
    USER_NOT_FOUND = 'user_not_found'
    CONVERSATION_NOT_FOUND = 'conversation_not_found'
    TEXT_TOO_LONG = 'text_too_long'
    INVALID_BLOCKS = 'invalid_blocks'


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
        return dict(self._asdict())

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'ErrorField':
        if not value:
            raise NoValueError('No value to type cast')
        try:
            code = ErrorCode(value['code']) if exist_kv('code', value) else None
        except ValueError:
            code = ErrorCode.UNKNOWN
        return cls(**dict(
            _drop_missing(value, cls._fields),
            code=code,
        ))


class UserIdentificationField(NamedTuple):
    type: str
    value: str

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._asdict())

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'UserIdentificationField':
        if not value:
            raise NoValueError('No value to type cast')
        return cls(**dict(_drop_missing(value, cls._fields)))


class UserField(NamedTuple):
    id: str
    space_id: str
    name: str
    display_name: Optional[str] = None
    identifications: Optional[List[UserIdentificationField]] = None
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    responsibility: Optional[str] = None
    tels: Optional[List[str]] = None
    mobiles: Optional[List[str]] = None
    work_start_time: Optional[datetime] = None
    work_end_time: Optional[datetime] = None
    vacation_start_time: Optional[datetime] = None
    vacation_end_time: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            dict(self._asdict()),
            identifications=[uid.to_dict() for uid in self.identifications] if self.identifications else None,
            work_start_time=int(self.work_start_time.timestamp()) if self.work_start_time else None,
            work_end_time=int(self.work_end_time.timestamp()) if self.work_end_time else None,
            vacation_start_time=int(self.vacation_start_time.timestamp()) if self.vacation_start_time else None,
            vacation_end_time=int(self.vacation_end_time.timestamp()) if self.vacation_end_time else None,
        )

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'UserField':
        if not value:
            raise NoValueError('No value to type cast')
        return cls(**dict(
            _drop_missing(value, cls._fields),
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
        return dict(self._asdict())

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'ConversationField':
        if not value:
            raise NoValueError('No value to type cast')
        return cls(**dict(
            _drop_missing(value, cls._fields),
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
            dict(self._asdict()),
            send_time=int(self.send_time.timestamp()) if self.send_time else None,
            update_time=int(self.update_time.timestamp()) if self.update_time else None,
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
                blocks.append(block_cls.from_dict(kv))
        return cls(**dict(
            _drop_missing(value, cls._fields),
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
        return dict(self._asdict())

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'DepartmentField':
        if not value:
            raise NoValueError('No value to type cast')
        return cls(**dict(_drop_missing(value, cls._fields)))


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
        return dict(self._asdict())

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'SpaceField':
        if not value:
            raise NoValueError('No value to type cast')
        return cls(**dict(
            _drop_missing(value, cls._fields),
            color_tone=ColorTone(value['color_tone']),
            profile_name_format=ProfileNameFormat(value['profile_name_format']),
            profile_position_format=ProfilePositionFormat(value['profile_position_format']),
        ))


class BotField(NamedTuple):
    bot_id: int
    title: str
    status: BotStatus

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._asdict())

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'BotField':
        if not value:
            raise NoValueError('No value to type cast')
        return cls(**dict(
            _drop_missing(value, cls._fields),
            status=BotStatus(value['status']),
        ))


class ReactiveType(StrEnum):
    SUBMIT_ACTION = "submit_action"
    SUBMIT_MODAL = "submission"
    REQUEST_MODAL = "request_modal"


class BaseReactiveBody(ABC, object):
    def __init__(self, *, type: ReactiveType, action_time: str, message: MessageField, value: str) -> None:
        self.type = type
        self.action_time = action_time
        self.message = message
        self.value = value

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return str(self)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, BaseReactiveBody):
            return False
        return self.to_dict() == value.to_dict()

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=json_default)

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            type=self.type,
            action_time=self.action_time,
            message=self.message.to_dict(),
            value=self.value,
        )

    @classmethod
    def from_json(cls, value: Union[str, bytes]) -> 'BaseReactiveBody':
        data = dict(text2json(value))
        if 'type' not in data:
            raise InvalidReactiveBody('No type')
        return cls(**dict(
            data,
            type=ReactiveType(data['type']),
            message=MessageField.from_dict(data['message']),
        ))


class SubmitActionReactiveBody(BaseReactiveBody):
    def __init__(self, *, action_time: str, message: MessageField, value: str, action_name: str, react_user_id: int) -> None:
        super().__init__(type=ReactiveType.SUBMIT_ACTION, action_time=action_time, message=message, value=value)
        self.action_name = action_name
        self.react_user_id = react_user_id

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            super().to_dict(),
            action_name=self.action_name,
            react_user_id=self.react_user_id,
        )

    @classmethod
    def from_json(cls, value: Union[str, bytes]) -> 'SubmitActionReactiveBody':
        data = dict(text2json(value))
        if 'type' not in data or data['type'] != ReactiveType.SUBMIT_ACTION:
            raise InvalidReactiveBody('No type or invalid')
        data = {k: v for k, v in data.items() if k != 'type'}
        return cls(**dict(
            data,
            message=MessageField.from_dict(data['message']),
            action_name=data['action_name'],
            react_user_id=int(data['react_user_id']),
        ))


class SubmitModalReactiveBody(BaseReactiveBody):
    def __init__(self, *, action_time: str, message: MessageField, value: str, actions: Dict[str, Any], react_user_id: int) -> None:
        super().__init__(type=ReactiveType.SUBMIT_MODAL, action_time=action_time, message=message, value=value)
        self.actions = actions
        self.react_user_id = react_user_id

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            super().to_dict(),
            actions=self.actions,
            react_user_id=self.react_user_id,
        )

    @classmethod
    def from_json(cls, value: Union[str, bytes]) -> 'SubmitModalReactiveBody':
        data = dict(text2json(value))
        if 'type' not in data or data['type'] != ReactiveType.SUBMIT_MODAL:
            raise InvalidReactiveBody('No type or invalid')
        data = {k: v for k, v in data.items() if k != 'type'}
        return cls(**dict(
            data,
            message=MessageField.from_dict(data['message']),
            actions=data['actions'],
            react_user_id=int(data['react_user_id']),
        ))


class RequestModalReactiveBody(BaseReactiveBody):
    def __init__(self, *, action_time: str, message: MessageField, value: str, react_user_id: int) -> None:
        super().__init__(type=ReactiveType.REQUEST_MODAL, action_time=action_time, message=message, value=value)
        self.react_user_id = react_user_id

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            super().to_dict(),
            react_user_id=self.react_user_id,
        )

    @classmethod
    def from_json(cls, value: Union[str, bytes]) -> 'RequestModalReactiveBody':
        data = dict(text2json(value))
        if 'type' not in data or data['type'] != ReactiveType.REQUEST_MODAL:
            raise InvalidReactiveBody('No type or invalid')
        data = {k: v for k, v in data.items() if k != 'type'}
        return cls(**dict(
            data,
            message=MessageField.from_dict(data['message']),
            react_user_id=int(data['react_user_id']),
        ))


class ModalReactiveView(NamedTuple):
    title: str
    accept: str
    decline: str
    blocks: List[Block]
    value: str

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            dict(self._asdict()),
            blocks=[b.to_dict() for b in self.blocks] if self.blocks else None,
        )

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'ModalReactiveView':
        if not value:
            raise NoValueError('No value to type cast')
        blocks: List[Block] = []
        if exist_kv('blocks', value):
            for kv in value['blocks']:
                block_cls = BlockType.block_cls(kv['type'])
                blocks.append(block_cls.from_dict(kv))
        return cls(**dict(
            _drop_missing(value, cls._fields),
            blocks=blocks,
        ))


class RequestModalReactiveResponse(object):
    def __init__(self, *, view: ModalReactiveView) -> None:
        self.view = view

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return str(self)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, RequestModalReactiveResponse):
            return False
        return self.to_dict() == value.to_dict()

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=json_default)

    def to_dict(self) -> Dict[str, Any]:
        return dict(view=self.view.to_dict())

    @classmethod
    def from_json(cls, value: Union[str, bytes]) -> 'RequestModalReactiveResponse':
        data = dict(text2json(value))
        return cls(**dict(
            data,
            view=ModalReactiveView.from_dict(data['view']),
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
        data = dict(text2json(value))
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
        data = dict(text2json(value))
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
        data = dict(text2json(value))
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
        data = dict(text2json(value))
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
        data = dict(text2json(value))
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
        data = dict(text2json(value))
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
        data = dict(text2json(value))
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
        data = dict(text2json(value))
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
            return '\n'.join([f'ID:\t{self.info.bot_id}', f'Name:\t{self.info.title}', f'Status:\t{self.info.status}'])
        return super().to_plain()

    @classmethod
    def from_json(cls, value: Union[str, bytes]) -> 'BotResponse':
        data = dict(text2json(value))
        return cls(**dict(
            data,
            error=ErrorField.from_dict(data['error']) if exist_kv('error', data) else None,
            info=BotField.from_dict(data['info']) if exist_kv('info', data) else None,
        ))
