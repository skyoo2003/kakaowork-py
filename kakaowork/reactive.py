from abc import ABCMeta, abstractmethod
from typing import Any

from kakaowork.models import SubmitActionReactiveBody, SubmitModalReactiveBody, RequestModalReactiveBody, RequestModalReactiveResponse


class BaseReactiveActionHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle_submit(self, body: SubmitActionReactiveBody) -> bool:
        raise NotImplementedError()


class BaseReactiveModalHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle_request(self, body: RequestModalReactiveBody) -> RequestModalReactiveResponse:
        raise NotImplementedError()

    @abstractmethod
    def handle_submit(self, body: SubmitModalReactiveBody) -> bool:
        raise NotImplementedError()
