class KakaoworkError(Exception):
    """Kakaowork base error."""


class InvalidBlockType(KakaoworkError):
    """Invalid block type."""


class InvalidBlock(KakaoworkError):
    """Invalid block."""


class InvalidReactiveBody(KakaoworkError):
    """Invalid reactive body."""
