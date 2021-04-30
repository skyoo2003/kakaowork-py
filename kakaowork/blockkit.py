import os
import json
from enum import unique
from abc import ABC, abstractmethod, abstractclassmethod
from typing import Any, Dict, List, Optional, NamedTuple, Type, Union
from urllib.parse import urlparse

from kakaowork.consts import StrEnum
from kakaowork.exceptions import InvalidBlock, InvalidBlockType, NoValueError
from kakaowork.utils import exist_kv, json_default


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
    def block_cls(cls, type: Union[str, 'BlockType']) -> Type['Block']:
        bt = cls(type) if isinstance(type, str) else type
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

    def to_dict(self) -> Dict[str, Any]:
        return self._asdict()

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'SelectBlockOption':
        if not value:
            raise NoValueError('No value to type cast')
        return cls(**value)


class Block(ABC):
    def __init__(self, *, type: BlockType):
        self.type = type

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return str(self)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Block):
            return False
        if self.type != value.type:
            return False
        if self.to_dict() != value.to_dict():
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {'type': self.type}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=json_default)

    @abstractmethod
    def validate(self) -> bool:
        raise NotImplementedError()

    @classmethod
    @abstractclassmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'Block':
        raise NotImplementedError()


class TextBlock(Block):
    max_len_text = 500

    def __init__(self, *, text: str, markdown: Optional[bool] = False):
        super().__init__(type=BlockType.TEXT)
        self.text = text
        self.markdown = markdown if markdown is not None else False

    def to_dict(self):
        return dict(
            super().to_dict(),
            text=self.text,
            markdown=self.markdown,
        )

    def validate(self) -> bool:
        if not self.text or len(self.text) > self.max_len_text:
            return False
        return True

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'TextBlock':
        if not value:
            raise NoValueError('No value to type cast')
        if 'type' not in value or value['type'] != BlockType.TEXT:
            raise InvalidBlockType('No type or invalid')
        value = {k: v for k, v in value.items() if k != 'type'}

        return cls(**dict(
            value,
            markdown=value['markdown'] if exist_kv('markdown', value) else False,
        ))


class ImageLinkBlock(Block):
    def __init__(self, *, url: str):
        super().__init__(type=BlockType.IMAGE_LINK)
        self.url = url

    def to_dict(self):
        return dict(
            super().to_dict(),
            url=self.url,
        )

    def validate(self) -> bool:
        if not self.url:
            return False
        o = urlparse(self.url)
        if not (o.scheme and o.netloc and o.path):
            return False
        if not os.path.splitext(o.path)[1]:
            return False
        return True

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'ImageLinkBlock':
        if not value:
            raise NoValueError('No value to type cast')
        if 'type' not in value or value['type'] != BlockType.IMAGE_LINK:
            raise InvalidBlockType('No type or invalid')
        value = {k: v for k, v in value.items() if k != 'type'}

        return cls(**value)


class ButtonBlock(Block):
    max_len_text = 20

    def __init__(self,
                 *,
                 text: str,
                 style: ButtonStyle,
                 action_type: Optional[ButtonActionType] = None,
                 action_name: Optional[str] = None,
                 value: Optional[str] = None):
        super().__init__(type=BlockType.BUTTON)
        self.text = text
        self.style = style
        self.action_type = action_type
        self.action_name = action_name
        self.value = value

    def to_dict(self):
        kwargs = dict(
            super().to_dict(),
            text=self.text,
            style=self.style,
            action_type=self.action_type,
            action_name=self.action_name,
            value=self.value,
        )
        return {k: v for k, v in kwargs.items() if v is not None}

    def validate(self) -> bool:
        if not self.text or len(self.text) > self.max_len_text:
            return False
        if not self.style:
            return False
        return True

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'ButtonBlock':
        if not value:
            raise NoValueError('No value to type cast')
        if 'type' not in value or value['type'] != BlockType.BUTTON:
            raise InvalidBlockType('No type or invalid')
        value = {k: v for k, v in value.items() if k != 'type'}

        return cls(**dict(
            value,
            style=ButtonStyle(value['style']),
            action_type=ButtonActionType(value['action_type']) if exist_kv('action_type', value) else None,
        ))


class DividerBlock(Block):
    def __init__(self) -> None:
        super().__init__(type=BlockType.DIVIDER)

    def to_dict(self):
        return super().to_dict()

    def validate(self) -> bool:
        return True

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'DividerBlock':
        if not value:
            raise NoValueError('No value to type cast')
        if 'type' in value and value['type'] != BlockType.DIVIDER:
            raise InvalidBlockType('No type or invalid')

        return cls()


class HeaderBlock(Block):
    max_len_text = 20

    def __init__(self, *, text: str, style: Optional[HeaderStyle] = None):
        super().__init__(type=BlockType.HEADER)
        self.text = text
        self.style = style

    def to_dict(self):
        return dict(
            super().to_dict(),
            text=self.text,
            style=self.style,
        )

    def validate(self) -> bool:
        if not self.text or len(self.text) > self.max_len_text:
            return False
        if not self.style:
            return False
        return True

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'HeaderBlock':
        if not value:
            raise NoValueError('No value to type cast')
        if 'type' not in value or value['type'] != BlockType.HEADER:
            raise InvalidBlockType('No type or invalid')
        value = {k: v for k, v in value.items() if k != 'type'}

        return cls(**dict(
            value,
            style=HeaderStyle(value['style']) if exist_kv('style', value) else None,
        ))


class ActionBlock(Block):
    max_len_elements = 3

    def __init__(self, *, elements: List[ButtonBlock]):
        super().__init__(type=BlockType.ACTION)
        self.elements = elements or []

    def to_dict(self):
        return dict(
            super().to_dict(),
            elements=[item.to_dict() for item in self.elements],
        )

    def validate(self) -> bool:
        if not self.elements or len(self.elements) > self.max_len_elements:
            return False
        return True

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'ActionBlock':
        if not value:
            raise NoValueError('No value to type cast')
        if 'type' not in value or value['type'] != BlockType.ACTION:
            raise InvalidBlockType('No type or invalid')
        value = {k: v for k, v in value.items() if k != 'type'}

        return cls(**dict(
            value,
            elements=[ButtonBlock.from_dict(item) for item in value['elements']],
        ))


class DescriptionBlock(Block):
    max_len_term = 10

    def __init__(self, *, term: str, content: TextBlock, accent: Optional[bool] = False):
        super().__init__(type=BlockType.DESCRIPTION)
        self.term = term
        self.content = content
        self.accent = accent if accent is not None else False

    def to_dict(self):
        return dict(
            super().to_dict(),
            term=self.term,
            content=self.content.to_dict(),
            accent=self.accent,
        )

    def validate(self) -> bool:
        if not self.term or len(self.term) > self.max_len_term:
            return False
        if not self.content:
            return False
        if self.accent is None:
            return False
        return True

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'DescriptionBlock':
        if not value:
            raise NoValueError('No value to type cast')
        if 'type' not in value or value['type'] != BlockType.DESCRIPTION:
            raise InvalidBlockType('No type or invalid')
        value = {k: v for k, v in value.items() if k != 'type'}

        return cls(**dict(
            value,
            content=TextBlock.from_dict(value['content']),
            accent=value['accent'] if exist_kv('accent', value) else False,
        ))


class SectionBlock(Block):
    def __init__(self, *, content: TextBlock, accessory: ImageLinkBlock):
        super().__init__(type=BlockType.SECTION)
        self.content = content
        self.accessory = accessory

    def to_dict(self):
        return dict(
            super().to_dict(),
            content=self.content.to_dict(),
            accessory=self.accessory.to_dict(),
        )

    def validate(self) -> bool:
        if not self.content:
            return False
        if not self.accessory:
            return False
        return True

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'SectionBlock':
        if not value:
            raise NoValueError('No value to type cast')
        if 'type' not in value or value['type'] != BlockType.SECTION:
            raise InvalidBlockType('No type or invalid')
        value = {k: v for k, v in value.items() if k != 'type'}

        return cls(**dict(
            value,
            content=TextBlock.from_dict(value['content']),
            accessory=ImageLinkBlock.from_dict(value['accessory']),
        ))


class ContextBlock(Block):
    def __init__(self, *, content: TextBlock, image: ImageLinkBlock):
        super().__init__(type=BlockType.CONTEXT)
        self.content = content
        self.image = image

    def to_dict(self):
        return dict(
            super().to_dict(),
            content=self.content.to_dict(),
            image=self.image.to_dict(),
        )

    def validate(self) -> bool:
        if not self.content:
            return False
        if not self.image:
            return False
        return True

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'ContextBlock':
        if not value:
            raise NoValueError('No value to type cast')
        if 'type' not in value or value['type'] != BlockType.CONTEXT:
            raise InvalidBlockType('No type or invalid')
        value = {k: v for k, v in value.items() if k != 'type'}

        return cls(**dict(
            value,
            content=TextBlock.from_dict(value['content']),
            image=ImageLinkBlock.from_dict(value['image']),
        ))


class LabelBlock(Block):
    max_len_text = 200

    def __init__(self, *, text: str, markdown: bool):
        super().__init__(type=BlockType.LABEL)
        self.text = text
        self.markdown = markdown

    def to_dict(self):
        return dict(
            super().to_dict(),
            text=self.text,
            markdown=self.markdown,
        )

    def validate(self) -> bool:
        if not self.text or len(self.text) > self.max_len_text:
            return False
        if self.markdown is None:
            return False
        return True

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'LabelBlock':
        if not value:
            raise NoValueError('No value to type cast')
        if 'type' not in value or value['type'] != BlockType.LABEL:
            raise InvalidBlockType('No type or invalid')
        value = {k: v for k, v in value.items() if k != 'type'}

        return cls(**value)


class InputBlock(Block):
    max_len_placeholder = 50

    def __init__(self, *, name: str, required: Optional[bool] = False, placeholder: Optional[str] = None):
        super().__init__(type=BlockType.INPUT)
        self.name = name
        self.required = required if required is not None else False
        self.placeholder = placeholder

    def to_dict(self):
        return dict(
            super().to_dict(),
            name=self.name,
            required=self.required,
            placeholder=self.placeholder,
        )

    def validate(self) -> bool:
        if not self.name:
            return False
        if self.placeholder and len(self.placeholder) > self.max_len_placeholder:
            return False
        return True

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'InputBlock':
        if not value:
            raise NoValueError('No value to type cast')
        if 'type' not in value or value['type'] != BlockType.INPUT:
            raise InvalidBlockType('No type or invalid')
        value = {k: v for k, v in value.items() if k != 'type'}

        return cls(**dict(
            value,
            required=value['required'] if exist_kv('required', value) else False,
        ))


class SelectBlock(Block):
    max_len_options = 30
    max_len_placeholder = 50

    def __init__(self, *, name: str, options: List[SelectBlockOption], required: Optional[bool] = False, placeholder: Optional[str] = None):
        super().__init__(type=BlockType.SELECT)
        self.name = name
        self.options = options or []
        self.required = required if required is not None else False
        self.placeholder = placeholder

    def to_dict(self):
        return dict(
            super().to_dict(),
            name=self.name,
            options=[item.to_dict() for item in self.options],
            required=self.required,
            placeholder=self.placeholder,
        )

    def validate(self) -> bool:
        if not self.name:
            return False
        if not self.options or len(self.options) > self.max_len_options:
            return False
        if self.placeholder and len(self.placeholder) > self.max_len_placeholder:
            return False
        return True

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'SelectBlock':
        if not value:
            raise NoValueError('No value to type cast')
        if 'type' not in value or value['type'] != BlockType.SELECT:
            raise InvalidBlockType('No type or invalid')
        value = {k: v for k, v in value.items() if k != 'type'}

        return cls(**dict(
            value,
            options=[SelectBlockOption.from_dict(item) for item in value['options']],
            required=value['required'] if exist_kv('required', value) else False,
        ))


class BlockKitBuilder:
    def __init__(self, *, type: BlockKitType):
        self.type = type
        self.reset()

    def reset(self):
        self.vars: Dict[str, Any] = {
            'blocks': [],
        }

    @property
    def text(self) -> str:
        if self.type != BlockKitType.MESSAGE:
            raise InvalidBlockType("It can be set only for message type")
        return self.vars['text'] if 'text' in self.vars else ''

    @text.setter
    def text(self, value: str):
        if self.type != BlockKitType.MESSAGE:
            raise InvalidBlockType("It can be set only for message type")
        self.vars['text'] = value

    @property
    def title(self) -> str:
        if self.type != BlockKitType.MODAL:
            raise InvalidBlockType("It can be set only for modal type")
        return self.vars['title'] if 'title' in self.vars else ''

    @title.setter
    def title(self, value: str):
        if self.type != BlockKitType.MODAL:
            raise InvalidBlockType("It can be set only for modal type")
        self.vars['title'] = value

    @property
    def accept(self) -> str:
        if self.type != BlockKitType.MODAL:
            raise InvalidBlockType("It can be set only for modal type")
        return self.vars['accept'] if 'accept' in self.vars else ''

    @accept.setter
    def accept(self, value: str):
        if self.type != BlockKitType.MODAL:
            raise InvalidBlockType("It can be set only for modal type")
        self.vars['accept'] = value

    @property
    def decline(self) -> str:
        if self.type != BlockKitType.MODAL:
            raise InvalidBlockType("It can be set only for modal type")
        return self.vars['decline'] if 'decline' in self.vars else ''

    @decline.setter
    def decline(self, value: str):
        if self.type != BlockKitType.MODAL:
            raise InvalidBlockType("It can be set only for modal type")
        self.vars['decline'] = value

    @property
    def value(self) -> str:
        if self.type != BlockKitType.MODAL:
            raise InvalidBlockType("It can be set only for modal type")
        return self.vars['value'] if 'value' in self.vars else ''

    @value.setter
    def value(self, value: str):
        if self.type != BlockKitType.MODAL:
            raise InvalidBlockType("It can be set only for modal type")
        self.vars['value'] = value

    @property
    def blocks(self) -> List[Block]:
        return self.vars['blocks'] if 'blocks' in self.vars and self.vars['blocks'] else []

    @blocks.setter
    def blocks(self, value: List[Block]):
        self.vars['blocks'] = []
        for item in value:
            self.add_block(item)

    def add_block(self, block: Block):
        if not block.validate():
            raise InvalidBlock()
        self.vars['blocks'].append(block)

    def to_dict(self) -> Dict[str, Any]:
        return {key: value for key, value in self.vars.items() if value is not None}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=json_default)
