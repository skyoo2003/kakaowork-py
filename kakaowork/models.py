from abc import ABC
from datetime import datetime
from typing import Optional, Union, Any, Dict, List

from pydantic import BaseModel, validator

from kakaowork.consts import StrEnum
from kakaowork.blockkit import Block
from kakaowork.utils import to_kst


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

    @classmethod
    def _missing_(cls, value: Any) -> 'ErrorCode':
        return cls.UNKNOWN


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


class ErrorField(BaseModel):
    code: ErrorCode
    message: str


class UserIdentificationField(BaseModel):
    type: str
    value: str


class UserField(BaseModel):
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

    class Config:
        json_encoders = {
            datetime: lambda dt: int(dt.timestamp()),
        }

    def __init__(self,
                 *,
                 work_start_time: Optional[Union[datetime, int, str]] = None,
                 work_end_time: Optional[Union[datetime, int, str]] = None,
                 vacation_start_time: Optional[Union[datetime, int, str]] = None,
                 vacation_end_time: Optional[Union[datetime, int, str]] = None,
                 **data) -> None:
        if work_start_time:
            data['work_start_time'] = to_kst(work_start_time) if isinstance(work_start_time, (datetime, int)) else work_start_time
        if work_end_time:
            data['work_end_time'] = to_kst(work_end_time) if isinstance(work_end_time, (datetime, int)) else work_end_time
        if vacation_start_time:
            data['vacation_start_time'] = to_kst(vacation_start_time) if isinstance(vacation_start_time, (datetime, int)) else vacation_start_time
        if vacation_end_time:
            data['vacation_end_time'] = to_kst(vacation_end_time) if isinstance(vacation_end_time, (datetime, int)) else vacation_end_time
        super().__init__(**data)


class ConversationField(BaseModel):
    id: str
    type: ConversationType
    users_count: int
    avatar_url: Optional[str] = None
    name: Optional[str] = None


class MessageField(BaseModel):
    id: str
    text: str
    user_id: str
    conversation_id: int
    send_time: datetime
    update_time: datetime
    blocks: Optional[List[Block]] = None

    class Config:
        json_encoders = {
            datetime: lambda dt: int(dt.timestamp()),
        }

    def __init__(self,
                 *,
                 send_time: Optional[Union[datetime, int, str]] = None,
                 update_time: Optional[Union[datetime, int, str]] = None,
                 blocks: Optional[List[Union[Block, Dict]]] = None,
                 **data) -> None:
        if send_time:
            data['send_time'] = to_kst(send_time) if isinstance(send_time, (datetime, int)) else send_time
        if update_time:
            data['update_time'] = to_kst(update_time) if isinstance(update_time, (datetime, int)) else update_time
        if blocks is not None:
            data['blocks'] = [Block.new(block) for block in blocks]
        super().__init__(**data)


class DepartmentField(BaseModel):
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


class SpaceField(BaseModel):
    id: int
    kakaoi_org_id: int
    name: str
    color_code: str
    color_tone: ColorTone
    permitted_ext: List[str]
    profile_name_format: ProfileNameFormat
    profile_position_format: ProfilePositionFormat
    logo_url: str


class BotField(BaseModel):
    bot_id: int
    title: str
    status: BotStatus


class WorkTimeField(BaseModel):
    user_id: int
    work_start_time: datetime
    work_end_time: datetime

    class Config:
        json_encoders = {
            datetime: lambda dt: int(dt.timestamp()),
        }

    def __init__(
        self,
        *,
        work_start_time: Optional[Union[datetime, int, str]] = None,
        work_end_time: Optional[Union[datetime, int, str]] = None,
        **data,
    ) -> None:
        if work_start_time:
            data['work_start_time'] = to_kst(work_start_time) if isinstance(work_start_time, (datetime, int)) else work_start_time
        if work_end_time:
            data['work_end_time'] = to_kst(work_end_time) if isinstance(work_end_time, (datetime, int)) else work_end_time
        super().__init__(**data)


class VacationTimeField(BaseModel):
    user_id: int
    vacation_start_time: datetime
    vacation_end_time: datetime

    class Config:
        json_encoders = {
            datetime: lambda dt: int(dt.timestamp()),
        }

    def __init__(
        self,
        *,
        vacation_start_time: Optional[Union[datetime, int, str]] = None,
        vacation_end_time: Optional[Union[datetime, int, str]] = None,
        **data,
    ) -> None:
        if vacation_start_time:
            data['vacation_start_time'] = to_kst(vacation_start_time) if isinstance(vacation_start_time, (datetime, int)) else vacation_start_time
        if vacation_end_time:
            data['vacation_end_time'] = to_kst(vacation_end_time) if isinstance(vacation_end_time, (datetime, int)) else vacation_end_time
        super().__init__(**data)


class ReactiveType(StrEnum):
    SUBMIT_ACTION = "submit_action"
    SUBMIT_MODAL = "submission"
    REQUEST_MODAL = "request_modal"


class BaseReactiveBody(BaseModel, ABC):
    type: ReactiveType
    action_time: str
    message: MessageField
    value: str

    class Config:
        validate_assignment = True
        json_encoders = {
            datetime: lambda dt: int(dt.timestamp()),
        }

    def __str__(self):
        return self.json(exclude_none=True)

    def __repr__(self):
        return str(self)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, BaseReactiveBody):
            return False
        return self.dict(exclude_none=True) == value.dict(exclude_none=True)


class SubmitActionReactiveBody(BaseReactiveBody):
    action_name: str
    react_user_id: int

    def __init__(self, **data) -> None:
        if 'type' not in data:
            data['type'] = ReactiveType.SUBMIT_ACTION
        super().__init__(**data)

    @validator('type')
    def _check_type(cls, value: ReactiveType) -> ReactiveType:
        if value != ReactiveType.SUBMIT_ACTION:
            raise ValueError(f"The 'type' should be f{ReactiveType.SUBMIT_ACTION}")
        return value


class SubmitModalReactiveBody(BaseReactiveBody):
    actions: Dict[str, Any]
    react_user_id: int

    def __init__(self, **data) -> None:
        if 'type' not in data:
            data['type'] = ReactiveType.SUBMIT_MODAL
        super().__init__(**data)

    @validator('type')
    def _check_type(cls, value: ReactiveType) -> ReactiveType:
        if value != ReactiveType.SUBMIT_MODAL:
            raise ValueError(f"The 'type' should be f{ReactiveType.SUBMIT_MODAL}")
        return value


class RequestModalReactiveBody(BaseReactiveBody):
    react_user_id: int

    def __init__(self, **data) -> None:
        if 'type' not in data:
            data['type'] = ReactiveType.REQUEST_MODAL
        super().__init__(**data)

    @validator('type')
    def _check_type(cls, value: ReactiveType) -> ReactiveType:
        if value != ReactiveType.REQUEST_MODAL:
            raise ValueError(f"The 'type' should be f{ReactiveType.REQUEST_MODAL}")
        return value


class ModalReactiveView(BaseModel):
    title: str
    accept: str
    decline: str
    blocks: List[Block]
    value: str

    def __init__(self, *, blocks: Optional[List[Union[Block, Dict]]] = None, **data) -> None:
        if blocks is not None:
            data['blocks'] = [Block.new(block) for block in blocks]
        super().__init__(**data)


class RequestModalReactiveResponse(BaseModel):
    view: ModalReactiveView

    def __str__(self):
        return self.json(exclude_none=True)

    def __repr__(self):
        return str(self)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, RequestModalReactiveResponse):
            return False
        return self.dict(exclude_none=True) == value.dict(exclude_none=True)


class BaseResponse(BaseModel, ABC):
    success: bool = True
    error: Optional[ErrorField] = None

    class Config:
        validate_assignment = True
        json_encoders = {
            datetime: lambda dt: int(dt.timestamp()),
        }

    def __str__(self):
        return self.json(exclude_none=True)

    def __repr__(self):
        return str(self)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, BaseResponse):
            return False
        return self.dict(exclude_none=True) == value.dict(exclude_none=True)

    def plain(self) -> str:
        if self.error:
            return '\n'.join([
                f'Error code:\t{self.error.code}',
                f'Message:\t{self.error.message}',
            ])
        return 'OK'


class UserResponse(BaseResponse):
    user: Optional[UserField] = None

    def plain(self) -> str:
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
        return super().plain()


class UserListResponse(BaseResponse):
    cursor: Optional[str] = None
    users: Optional[List[UserField]] = None

    def plain(self) -> str:
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
        return super().plain()


class ConversationResponse(BaseResponse):
    conversation: Optional[ConversationField] = None

    def plain(self) -> str:
        if self.conversation:
            return '\n'.join([
                f'ID:\t{self.conversation.id}',
                f'Type:\t{self.conversation.type}',
                f'Name:\t{self.conversation.name}',
                f'Avatar URL:\t{self.conversation.avatar_url}',
            ])
        return super().plain()


class ConversationListResponse(BaseResponse):
    cursor: Optional[str] = None
    conversations: Optional[List[ConversationField]] = None

    def plain(self) -> str:
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
        return super().plain()


class MessageResponse(BaseResponse):
    message: Optional[MessageField] = None

    def plain(self):
        if self.message:
            return '\n'.join([
                f'ID:\t{self.message.id}',
                f'Conversation ID:\t{self.message.conversation_id}',
                f'Send time:\t{self.message.send_time}',
                f'Update time:\t{self.message.update_time}',
                f'Text:\t{self.message.text}',
                f'Blocks:\t{len(self.message.blocks) if self.message.blocks else "-"}',
            ])
        return super().plain()


class DepartmentListResponse(BaseResponse):
    cursor: Optional[str] = None
    departments: Optional[List[DepartmentField]] = None

    def plain(self) -> str:
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
        return super().plain()


class SpaceResponse(BaseResponse):
    space: Optional[SpaceField] = None

    def plain(self) -> str:
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
        return super().plain()


class BotResponse(BaseResponse):
    info: Optional[BotField] = None

    def plain(self) -> str:
        if self.info:
            return '\n'.join([f'ID:\t{self.info.bot_id}', f'Name:\t{self.info.title}', f'Status:\t{self.info.status}'])
        return super().plain()
