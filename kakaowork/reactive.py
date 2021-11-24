from abc import ABCMeta, abstractmethod

from kakaowork.models import SubmitActionReactiveBody, SubmitModalReactiveBody, RequestModalReactiveBody, RequestModalReactiveResponse


class BaseReactiveActionHandler(metaclass=ABCMeta):
    """An abstract class for reactive action handler."""
    @abstractmethod
    def handle_submit(self, body: SubmitActionReactiveBody) -> bool:
        """An abstract method for handling user's request from the KakaoWork server to your server.

        Args:
            body: The request body of user's submission.

        Returns:
            True if this handler succeeds, False otherwise.
        """
        raise NotImplementedError()


class BaseReactiveModalHandler(metaclass=ABCMeta):
    """An abstract class for reactive modal handler."""
    @abstractmethod
    def handle_request(self, body: RequestModalReactiveBody) -> RequestModalReactiveResponse:
        """An abstract method for handling a request to compose a modal from the KakaoWork server to your server.

        Args:
            body: The request body of user's modal action.

        Returns:
            True if this handler succeeds, False otherwise.
        """
        raise NotImplementedError()

    @abstractmethod
    def handle_submit(self, body: SubmitModalReactiveBody) -> bool:
        """An abstract method for handling user's request from the KakaoWork server to your server.

        Args:
            body: The request body of user's submission.

        Returns:
            True if this handler succeeds, False otherwise.
        """
        raise NotImplementedError()
