import os
import json
from enum import unique
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, NamedTuple, Type, Union
from urllib.parse import urlparse

from kakaowork.consts import StrEnum
from kakaowork.exceptions import InvalidBlock, InvalidBlockType


@unique
class BlockType(StrEnum):
    TEXT = "text"
    IMAGE_LINK = "image_link"
    BUTTON = "button"
    DIVIDER = "divider"
    HEADER = "header"
    ACTION = "action"
    DESCRIPTION = "description"
    SECTION = "section"
    CONTEXT = "context"
    LABEL = "label"
    INPUT = "input"
    SELECT = "select"

    @classmethod
    def block_cls(cls, block_type: Union[str, 'BlockType']) -> Type['Block']:
        bt = cls(block_type) if isinstance(block_type, str) else block_type
        if bt == cls.TEXT:
            return TextBlock
        elif bt == cls.IMAGE_LINK:
            return ImageLinkBlock
        elif bt == cls.BUTTON:
            return ButtonBlock
        elif bt == cls.DIVIDER:
            return DividerBlock
        elif bt == cls.HEADER:
            return HeaderBlock
        elif bt == cls.ACTION:
            return ActionBlock
        elif bt == cls.DESCRIPTION:
            return DescriptionBlock
        elif bt == cls.SECTION:
            return SectionBlock
        elif bt == cls.CONTEXT:
            return ContextBlock
        elif bt == cls.LABEL:
            return LabelBlock
        elif bt == cls.INPUT:
            return InputBlock
        elif bt == cls.SELECT:
            return SelectBlock
        raise InvalidBlockType()


@unique
class ButtonStyle(StrEnum):
    DEFAULT = "default"
    PRIMARY = "primary"
    DANGER = "danger"


@unique
class ButtonActionType(StrEnum):
    OPEN_INAPP_BROWSER = "open_inapp_browser"
    OPEN_SYSTEM_BROWSER = "open_system_browser"
    OPEN_EXTERNAL_APP = "open_external_app"
    SUBMIT_ACTION = "submit_action"
    CALL_MODAL = "call_modal"


@unique
class HeaderStyle(StrEnum):
    BLUE = 'blue'
    RED = 'red'
    YELLOW = 'yellow'


@unique
class BlockKitType(StrEnum):
    MESSAGE = 'message'
    MODAL = 'modal'


class SelectBlockOption(NamedTuple):
    text: str
    value: str


def json_default(value: Any) -> Any:
    if isinstance(value, Block):
        return value.to_dict()
    raise TypeError('not JSON serializable')


class Block(ABC):
    def __init__(self, *, block_type: BlockType):
        self.block_type = block_type
        self.block_vars: Dict[str, Any] = {}

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return str(self)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Block):
            return False
        if self.block_type != value.block_type:
            return False
        if self.block_vars != value.block_vars:
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        block_vars = {key: value for key, value in self.block_vars.items() if value is not None}
        return dict(type=self.block_type, **block_vars)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=json_default)

    @abstractmethod
    def validate(self) -> bool:
        raise NotImplementedError()


class TextBlock(Block):
    max_len_text = 500

    def __init__(self, *, text: str, markdown: Optional[bool] = False):
        super().__init__(block_type=BlockType.TEXT)
        self.block_vars = {
            'text': text,
            'markdown': markdown or False,
        }

    @property
    def text(self) -> str:
        return self.block_vars['text']

    @property
    def markdown(self) -> bool:
        return self.block_vars['markdown']

    def validate(self) -> bool:
        if not self.text or len(self.text) > self.max_len_text:
            return False
        return True


class ImageLinkBlock(Block):
    def __init__(self, *, url: str):
        super().__init__(block_type=BlockType.IMAGE_LINK)
        self.block_vars = {
            'url': url,
        }

    @property
    def url(self) -> str:
        return self.block_vars['url']

    def validate(self) -> bool:
        if not self.url:
            return False
        o = urlparse(self.url)
        if not (o.scheme and o.netloc and o.path):
            return False
        if not os.path.splitext(o.path)[1]:
            return False
        return True


class ButtonBlock(Block):
    max_len_text = 20

    def __init__(self,
                 *,
                 text: str,
                 style: ButtonStyle,
                 action_type: Optional[ButtonActionType] = None,
                 action_name: Optional[str] = None,
                 value: Optional[str] = None):
        super().__init__(block_type=BlockType.BUTTON)
        self.block_vars = {
            'text': text,
            'style': style,
            'action_type': action_type,
            'action_name': action_name,
            'value': value,
        }

    @property
    def text(self) -> str:
        return self.block_vars['text']

    @property
    def style(self) -> ButtonStyle:
        return self.block_vars['style']

    @property
    def action_type(self) -> ButtonActionType:
        return self.block_vars['action_type']

    @property
    def action_name(self) -> str:
        return self.block_vars['action_name']

    @property
    def value(self) -> str:
        return self.block_vars['value']

    def validate(self) -> bool:
        if not self.text or len(self.text) > self.max_len_text:
            return False
        if not self.style:
            return False
        return True


class DividerBlock(Block):
    def __init__(self) -> None:
        super().__init__(block_type=BlockType.DIVIDER)

    def validate(self) -> bool:
        return True


class HeaderBlock(Block):
    max_len_text = 20

    def __init__(self, *, text: str, style: Optional[HeaderStyle] = None):
        super().__init__(block_type=BlockType.HEADER)
        self.block_vars = {
            'text': text,
            'style': style,
        }

    @property
    def text(self) -> str:
        return self.block_vars['text']

    @property
    def style(self) -> HeaderStyle:
        return self.block_vars['style']

    def validate(self) -> bool:
        if not self.text or len(self.text) > self.max_len_text:
            return False
        if not self.style:
            return False
        return True


class ActionBlock(Block):
    max_len_elements = 3

    def __init__(self, *, elements: List[ButtonBlock]):
        super().__init__(block_type=BlockType.ACTION)
        self.block_vars = {
            'elements': elements,
        }

    @property
    def elements(self) -> List[ButtonBlock]:
        return self.block_vars['elements']

    def validate(self) -> bool:
        if not self.elements or len(self.elements) > self.max_len_elements:
            return False
        return True


class DescriptionBlock(Block):
    max_len_term = 10

    def __init__(self, *, term: str, content: TextBlock, accent: Optional[bool] = False):
        super().__init__(block_type=BlockType.DESCRIPTION)
        self.block_vars = {
            'term': term,
            'content': content,
            'accent': accent or False,
        }

    @property
    def term(self) -> str:
        return self.block_vars['term']

    @property
    def content(self) -> TextBlock:
        return self.block_vars['content']

    @property
    def accent(self) -> bool:
        return self.block_vars['accent']

    def validate(self) -> bool:
        if not self.term or len(self.term) > self.max_len_term:
            return False
        if not self.content:
            return False
        if self.accent is None:
            return False
        return True


class SectionBlock(Block):
    def __init__(self, *, content: TextBlock, accessory: ImageLinkBlock):
        super().__init__(block_type=BlockType.SECTION)
        self.block_vars = {
            'content': content,
            'accessory': accessory,
        }

    @property
    def content(self) -> TextBlock:
        return self.block_vars['content']

    @property
    def accessory(self) -> ImageLinkBlock:
        return self.block_vars['accessory']

    def validate(self) -> bool:
        if not self.content:
            return False
        if not self.accessory:
            return False
        return True


class ContextBlock(Block):
    def __init__(self, *, content: TextBlock, image: ImageLinkBlock):
        super().__init__(block_type=BlockType.CONTEXT)
        self.block_vars = {
            'content': content,
            'image': image,
        }

    @property
    def content(self) -> TextBlock:
        return self.block_vars['content']

    @property
    def image(self) -> ImageLinkBlock:
        return self.block_vars['image']

    def validate(self) -> bool:
        if not self.content:
            return False
        if not self.image:
            return False
        return True


class LabelBlock(Block):
    max_len_text = 200

    def __init__(self, *, text: str, markdown: bool):
        super().__init__(block_type=BlockType.LABEL)
        self.block_vars = {
            'text': text,
            'markdown': markdown,
        }

    @property
    def text(self) -> str:
        return self.block_vars['text']

    @property
    def markdown(self) -> bool:
        return self.block_vars['markdown']

    def validate(self) -> bool:
        if not self.text or len(self.text) > self.max_len_text:
            return False
        if self.markdown is None:
            return False
        return True


class InputBlock(Block):
    max_len_placeholder = 50

    def __init__(self, *, name: str, required: Optional[bool] = False, placeholder: Optional[str] = None):
        super().__init__(block_type=BlockType.INPUT)
        self.block_vars = {
            'name': name,
            'required': required or False,
            'placeholder': placeholder,
        }

    @property
    def name(self) -> str:
        return self.block_vars['name']

    @property
    def required(self) -> Optional[bool]:
        return self.block_vars['required']

    @property
    def placeholder(self) -> Optional[str]:
        return self.block_vars['placeholder']

    def validate(self) -> bool:
        if not self.name:
            return False
        if self.placeholder and len(self.placeholder) > self.max_len_placeholder:
            return False
        return True


class SelectBlock(Block):
    max_len_options = 30
    max_len_placeholder = 50

    def __init__(self, *, name: str, options: List[SelectBlockOption], required: Optional[bool] = False, placeholder: Optional[str] = None):
        super().__init__(block_type=BlockType.SELECT)
        self.block_vars = {
            'name': name,
            'options': options,
            'required': required or False,
            'placeholder': placeholder,
        }

    @property
    def name(self) -> str:
        return self.block_vars['name']

    @property
    def options(self) -> List[SelectBlockOption]:
        return self.block_vars['options']

    @property
    def required(self) -> Optional[bool]:
        return self.block_vars['required']

    @property
    def placeholder(self) -> Optional[str]:
        return self.block_vars['placeholder']

    def validate(self) -> bool:
        if not self.name:
            return False
        if not self.options or len(self.options) > self.max_len_options:
            return False
        if self.placeholder and len(self.placeholder) > self.max_len_placeholder:
            return False
        return True


class BlockKitBuilder:
    def __init__(self, *, kit_type: BlockKitType):
        self.kit_type = kit_type
        self.reset()

    def reset(self):
        self.kit_vars: Dict[str, Any] = {
            'blocks': [],
        }

    @property
    def text(self) -> str:
        if self.kit_type != BlockKitType.MESSAGE:
            raise InvalidBlockType("It can be set only for message type")
        return self.kit_vars['text'] if 'text' in self.kit_vars else ''

    @text.setter
    def text(self, value: str):
        if self.kit_type != BlockKitType.MESSAGE:
            raise InvalidBlockType("It can be set only for message type")
        self.kit_vars['text'] = value

    @property
    def title(self) -> str:
        if self.kit_type != BlockKitType.MODAL:
            raise InvalidBlockType("It can be set only for modal type")
        return self.kit_vars['title'] if 'title' in self.kit_vars else ''

    @title.setter
    def title(self, value: str):
        if self.kit_type != BlockKitType.MODAL:
            raise InvalidBlockType("It can be set only for modal type")
        self.kit_vars['title'] = value

    @property
    def accept(self) -> str:
        if self.kit_type != BlockKitType.MODAL:
            raise InvalidBlockType("It can be set only for modal type")
        return self.kit_vars['accept'] if 'accept' in self.kit_vars else ''

    @accept.setter
    def accept(self, value: str):
        if self.kit_type != BlockKitType.MODAL:
            raise InvalidBlockType("It can be set only for modal type")
        self.kit_vars['accept'] = value

    @property
    def decline(self) -> str:
        if self.kit_type != BlockKitType.MODAL:
            raise InvalidBlockType("It can be set only for modal type")
        return self.kit_vars['decline'] if 'decline' in self.kit_vars else ''

    @decline.setter
    def decline(self, value: str):
        if self.kit_type != BlockKitType.MODAL:
            raise InvalidBlockType("It can be set only for modal type")
        self.kit_vars['decline'] = value

    @property
    def value(self) -> str:
        if self.kit_type != BlockKitType.MODAL:
            raise InvalidBlockType("It can be set only for modal type")
        return self.kit_vars['value'] if 'value' in self.kit_vars else ''

    @value.setter
    def value(self, value: str):
        if self.kit_type != BlockKitType.MODAL:
            raise InvalidBlockType("It can be set only for modal type")
        self.kit_vars['value'] = value

    @property
    def blocks(self) -> List[Block]:
        return self.kit_vars['blocks'] if 'blocks' in self.kit_vars and self.kit_vars['blocks'] else []

    @blocks.setter
    def blocks(self, value: List[Block]):
        self.kit_vars['blocks'] = []
        for item in value:
            self.add_block(item)

    def add_block(self, block: Block):
        if not block.validate():
            raise InvalidBlock()
        self.kit_vars['blocks'].append(block)

    def to_dict(self) -> Dict[str, Any]:
        return {key: value for key, value in self.kit_vars.items() if value is not None}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=json_default)
