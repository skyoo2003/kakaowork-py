from datetime import datetime
from typing import Optional, NamedTuple


class ErrorField(NamedTuple):
    code: str
    message: str


class UserField(NamedTuple):
    user_id: str
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


class BaseResponse:
    __slots__ = ('success', 'error')

    def __init__(self, success: bool, error: Optional[ErrorField] = None):
        self.success = success
        self.error = error


class UserInfoResponse(BaseResponse):
    __slots__ = ('success', 'error', 'user')

    def __init__(self, success, error: Optional[ErrorField] = None, user: Optional[UserField] = None):
        super().__init__(success, error=error)
        self.user = user
