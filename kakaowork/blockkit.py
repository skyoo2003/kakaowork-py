import json
from enum import unique
from functools import reduce
from abc import ABC
from typing import Any, Dict, List, Optional, Type, Union, ClassVar, Iterable

from pydantic import (
    BaseModel,
    root_validator,
    validator,
    AnyHttpUrl,
)

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


class TextInlineType(StrEnum):
    STYLED = 'styled'
    LINK = 'link'


class TextInlineColor(StrEnum):
    DEFAULT = 'default'
    GREY = 'grey'
    BLUE = 'blue'
    RED = 'red'

    @classmethod
    def _missing_(cls, value: Any) -> 'TextInlineColor':
        return cls.DEFAULT


class TextInline(BaseModel):
    type: TextInlineType
    text: str
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    strike: Optional[bool] = None
    color: Optional[TextInlineColor] = None
    url: Optional[str] = None

    class Config:
        underscore_attrs_are_private = True
        validate_assignment = True

    @root_validator
    def _check_conflict_props(cls, values: Dict) -> Dict:
        _type = values.get('type')
        if _type is TextInlineType.STYLED and values.get('url') is not None:
            raise ValueError("If the 'type' property is 'styled', the 'url' property can't be set")
        elif _type is TextInlineType.LINK:
            only_url_set = all([
                values.get('bold') is None,
                values.get('italic') is None,
                values.get('strike') is None,
                values.get('color') is None,
            ])
            if not only_url_set:
                raise ValueError("If the 'type' property is 'link', the 'url' property only can be set")
        return values


@unique
class ButtonStyle(StrEnum):
    DEFAULT = "default"
    PRIMARY = "primary"
    DANGER = "danger"

    @classmethod
    def _missing_(cls, value: Any) -> 'ButtonStyle':
        return cls.DEFAULT


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

    @classmethod
    def _missing_(cls, value: Any) -> 'HeaderStyle':
        return cls.BLUE


@unique
class BlockKitType(StrEnum):
    MESSAGE = 'message'
    MODAL = 'modal'


class SelectBlockOption(BaseModel):
    text: str
    value: str


class Block(BaseModel, ABC):
    type: BlockType

    class Config:
        underscore_attrs_are_private = True
        validate_assignment = True

    def __str__(self):
        return self.json(exclude_none=True)

    def __repr__(self):
        return str(self)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Block):
            return False
        if self.type != value.type:
            return False
        if str(self) != str(value):
            return False
        return True

    @classmethod
    def new(cls, value: Union[Dict, 'Block']) -> 'Block':
        if isinstance(value, dict):
            if 'type' not in value:
                raise ValueError("There is no 'type' from the argument")
            return BlockType.block_cls(value['type'])(**value)
        return value


class TextBlock(Block):
    _max_len_text: ClassVar[int] = 500

    text: str
    markdown: Optional[bool] = None
    inlines: Optional[List[TextInline]] = None

    def __init__(self, **data) -> None:
        if 'type' not in data:
            data['type'] = BlockType.TEXT
        super().__init__(**data)

    @root_validator
    def _check_deprecation(cls, values: Dict) -> Dict:
        markdown = values.get('markdown')
        inlines = values.get('inlines')
        if markdown and inlines is not None:
            raise ValueError("The 'markdown' property can't be set with the 'inlines' property")
        return values

    @validator('text')
    def _check_max_len_text(cls, value: str) -> str:
        if not value:
            raise ValueError("The 'text' property should be exists")
        if len(value) > cls._max_len_text:
            raise ValueError(f"The 'text' property's length should be less than or equal to {cls._max_len_text}")
        return value

    @validator('inlines')
    def _check_max_len_inlines(cls, value: Optional[List[TextInline]]) -> Optional[List[TextInline]]:
        if value is not None:
            len_inlines = reduce(lambda acc, text: acc + len(text), map(lambda i: i.text, value), 0)
            if len_inlines > cls._max_len_text:
                raise ValueError(f"The 'inlines' property's all texts should be less than or equal to {cls._max_len_text}")
        return value


class ImageLinkBlock(Block):
    url: AnyHttpUrl

    def __init__(self, **data) -> None:
        if 'type' not in data:
            data['type'] = BlockType.IMAGE_LINK
        super().__init__(**data)


class ButtonBlock(Block):
    _max_len_text: ClassVar[int] = 20

    text: str
    style: ButtonStyle = ButtonStyle.DEFAULT
    action_type: Optional[ButtonActionType] = None
    action_name: Optional[str] = None
    value: Optional[str] = None

    def __init__(self, **data) -> None:
        if 'type' not in data:
            data['type'] = BlockType.BUTTON
        super().__init__(**data)

    @validator('text')
    def _check_text(cls, value: str) -> str:
        if not value:
            raise ValueError("The 'text' property should be exists")
        if len(value) > cls._max_len_text:
            raise ValueError(f"The 'text' property's length should be less than or equal to {cls._max_len_text}")
        return value


class DividerBlock(Block):
    def __init__(self, **data) -> None:
        if 'type' not in data:
            data['type'] = BlockType.DIVIDER
        super().__init__(**data)


class HeaderBlock(Block):
    _max_len_text: ClassVar[int] = 20

    text: str
    style: HeaderStyle = HeaderStyle.BLUE

    def __init__(self, **data):
        if 'type' not in data:
            data['type'] = BlockType.HEADER
        super().__init__(**data)

    @validator('text')
    def _check_text(cls, value: str) -> str:
        if not value:
            raise ValueError("The 'text' property should be exists")
        if len(value) > cls._max_len_text:
            raise ValueError(f"The 'text' property's length should be less than or equal to {cls._max_len_text}")
        return value


class ActionBlock(Block):
    _max_len_elements: ClassVar[int] = 3

    elements: List[ButtonBlock]

    def __init__(self, **data) -> None:
        if 'type' not in data:
            data['type'] = BlockType.ACTION
        super().__init__(**data)

    @validator('elements')
    def _check_elements(cls, value: List[ButtonBlock]) -> List[ButtonBlock]:
        if not value:
            raise ValueError("The 'elements' property should be exists")
        if len(value) > cls._max_len_elements:
            raise ValueError(f"The 'elements' property's length should be less than or equal to {cls._max_len_elements}")
        return value


class DescriptionBlock(Block):
    _max_len_term: ClassVar[int] = 10

    term: str
    content: TextBlock
    accent: Optional[bool] = None

    def __init__(self, **data) -> None:
        if 'type' not in data:
            data['type'] = BlockType.DESCRIPTION
        super().__init__(**data)

    @validator('term')
    def _check_term(cls, value: str) -> str:
        if not value:
            raise ValueError("The 'term' property should be exists")
        if len(value) > cls._max_len_term:
            raise ValueError(f"The 'term' property's length should be less than or equal to {cls._max_len_term}")
        return value


class SectionBlock(Block):
    content: TextBlock
    accessory: ImageLinkBlock

    def __init__(self, **data) -> None:
        if 'type' not in data:
            data['type'] = BlockType.SECTION
        super().__init__(**data)


class ContextBlock(Block):
    content: TextBlock
    image: ImageLinkBlock

    def __init__(self, **data) -> None:
        if 'type' not in data:
            data['type'] = BlockType.CONTEXT
        super().__init__(**data)


class LabelBlock(Block):
    _max_len_text: ClassVar[int] = 200

    text: str
    markdown: bool

    def __init__(self, **data) -> None:
        if 'type' not in data:
            data['type'] = BlockType.LABEL
        super().__init__(**data)

    @validator('text')
    def _check_text(cls, value: str) -> str:
        if not value:
            raise ValueError("The 'text' property should be exists")
        if len(value) > cls._max_len_text:
            raise ValueError(f"The 'text' property's length should be less than or equal to {cls._max_len_text}")
        return value


class InputBlock(Block):
    _max_len_placeholder: ClassVar[int] = 50

    name: str
    required: Optional[bool] = None
    placeholder: Optional[str] = None

    def __init__(self, **data) -> None:
        if 'type' not in data:
            data['type'] = BlockType.INPUT
        super().__init__(**data)

    @validator('name')
    def _check_name(cls, value: str) -> str:
        if not value:
            raise ValueError("The 'name' property should be exists")
        return value

    @validator('placeholder')
    def _check_placeholder(cls, value: Optional[str] = None) -> Optional[str]:
        if value and len(value) > cls._max_len_placeholder:
            raise ValueError(f"The 'placeholder' property's length should be less than or equal to {cls._max_len_placeholder}")
        return value


class SelectBlock(Block):
    _max_len_options: ClassVar[int] = 30
    _max_len_placeholder: ClassVar[int] = 50

    name: str
    options: List[SelectBlockOption]
    required: Optional[bool] = None
    placeholder: Optional[str] = None

    def __init__(self, **data) -> None:
        if 'type' not in data:
            data['type'] = BlockType.SELECT
        super().__init__(**data)

    @validator('name')
    def _check_name(cls, value: str) -> str:
        if not value:
            raise ValueError("The 'name' property should be exists")
        return value

    @validator('options')
    def _check_options(cls, value: List[SelectBlockOption]) -> List[SelectBlockOption]:
        if not value:
            raise ValueError("The 'options' property should be exists")
        if len(value) > cls._max_len_options:
            raise ValueError(f"The 'options' property's length should be less than or equal to {cls._max_len_options}")
        return value

    @validator('placeholder')
    def _check_placeholder(cls, value: Optional[str] = None) -> Optional[str]:
        if value and len(value) > cls._max_len_placeholder:
            raise ValueError(f"The 'placeholder' property's length should be less than or equal to {cls._max_len_placeholder}")
        return value


class BlockKitBuilder(BaseModel):
    type: BlockKitType
    blocks: List[Block] = []
    text: Optional[str] = None
    title: Optional[str] = None
    accept: Optional[str] = None
    decline: Optional[str] = None
    value: Optional[str] = None

    class Config:
        validate_assignment = True

    @root_validator
    def _check_message_type(cls, values: Dict) -> Dict:
        _type = values.get('type')
        if _type and _type != BlockKitType.MESSAGE:
            if values.get('text'):
                raise ValueError("The 'text' property can be set only for message type")
        return values

    @root_validator
    def _check_modal_type(cls, values: Dict) -> Dict:
        _type = values.get('type')
        if _type and _type != BlockKitType.MODAL:
            if values.get('title'):
                raise ValueError("The 'title' property can be set only for modal type")
            elif values.get('accept'):
                raise ValueError("The 'accept' property can be set only for modal type")
            elif values.get('decline'):
                raise ValueError("The 'decline' property can be set only for modal type")
            elif values.get('value'):
                raise ValueError("The 'value' property can be set only for modal type")
        return values

    def add_block(self, block: Union[Block, dict]):
        if isinstance(block, dict):
            if 'type' not in block:
                raise InvalidBlock()
            block = BlockType.block_cls(block['type'])(**block)
        self.blocks.append(block)

    @classmethod
    def load(cls, path: str) -> 'BlockKitBuilder':
        with open(path, 'r') as f:
            data = json.load(f)
        self = cls(type=data['type'])
        for key, value in data.items():
            if key == 'blocks' and isinstance(value, Iterable):
                self.blocks = []
                for block in value:
                    self.add_block(block)
            else:
                setattr(self, key, value)
        return self
