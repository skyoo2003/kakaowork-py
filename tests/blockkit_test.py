import json
from unittest.mock import mock_open

import pytest
from pytest_mock import MockerFixture
from pydantic import ValidationError

from kakaowork.blockkit import (
    BlockType,
    ButtonStyle,
    ButtonActionType,
    HeaderStyle,
    BlockKitType,
    TextInlineType,
    TextInlineColor,
    TextInline,
    TextBlock,
    ImageLinkBlock,
    ButtonBlock,
    DividerBlock,
    HeaderBlock,
    ActionBlock,
    DescriptionBlock,
    SectionBlock,
    ContextBlock,
    LabelBlock,
    InputBlock,
    SelectBlockOption,
    SelectBlock,
    BlockKitBuilder,
)
from kakaowork.exceptions import InvalidBlock, InvalidBlockType


class TestTextInlineColor:
    def test_missing(self):
        assert TextInlineColor('#####') is TextInlineColor.DEFAULT


class TestTextInline:
    def test_validator(self):
        TextInline(type=TextInlineType.STYLED, text='msg', bold=True)

        with pytest.raises(ValidationError):
            TextInline(type=TextInlineType.STYLED, text='msg', url='http://localhost')

        TextInline(type=TextInlineType.LINK, text='msg', url='http://localhost')

        with pytest.raises(ValidationError):
            TextInline(type=TextInlineType.LINK, text='msg', bold=True)

        with pytest.raises(ValidationError):
            TextInline(type=TextInlineType.LINK, text='msg', bold=True, italic=True, strike=True, color=False)

        with pytest.raises(ValidationError):
            TextInline(type='####', text='msg')

    def test_to_dict(self):
        inline = TextInline(type=TextInlineType.STYLED, text='msg', bold=True, color=TextInlineColor.GREY)
        assert inline.dict(exclude_none=True) == {'type': 'styled', 'text': 'msg', 'bold': True, 'color': 'grey'}

        inline = TextInline(type=TextInlineType.LINK, text='msg', url='http://localhost')
        assert inline.dict(exclude_none=True) == {'type': 'link', 'text': 'msg', 'url': 'http://localhost'}

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            TextInline(**{})

        with pytest.raises(ValidationError):
            TextInline(**{'type': '####', 'text': 'msg'})

        inline = TextInline(**{'type': 'styled', 'text': 'msg', 'bold': True, 'color': 'grey'})
        assert inline == TextInline(type=TextInlineType.STYLED, text='msg', bold=True, color=TextInlineColor.GREY)

        inline = TextInline(**{'type': 'link', 'text': 'msg', 'url': 'http://localhost'})
        assert inline == TextInline(type=TextInlineType.LINK, text='msg', url='http://localhost')


class TestButtonStyle:
    def test_missing(self):
        assert ButtonStyle('#####') is ButtonStyle.DEFAULT


class TestHeaderStyle:
    def test_missing(self):
        assert HeaderStyle('#####') is HeaderStyle.BLUE


class TestTextBlock:
    def test_properties(self):
        text = '"hello"'
        block = TextBlock(text=text, markdown=False)
        assert block.type == BlockType.TEXT
        assert block.text == text
        assert block.markdown is False

        inlines = [TextInline(type=TextInlineType.STYLED, text='msg', bold=True)]
        block = TextBlock(text=text, inlines=inlines)
        assert block.type == BlockType.TEXT
        assert block.text == text
        assert block.inlines == inlines

    def test_validator(self):
        TextBlock(text="hello", markdown=False)

        with pytest.raises(ValidationError):
            TextBlock(text="", markdown=False)

        with pytest.raises(ValidationError):
            TextBlock(text="a" * 501, markdown=False)

        inlines = [TextInline(type=TextInlineType.STYLED, text='msg', bold=True)]
        TextBlock(text='hello', inlines=inlines)

        with pytest.raises(ValidationError):
            TextBlock(text='hello', markdown=True, inlines=inlines)

    def test_to_dict(self):
        block = TextBlock(text="hello", markdown=False)
        assert block.dict(exclude_none=True) == {
            'type': BlockType.TEXT,
            'text': 'hello',
            'markdown': False,
        }

        inlines = [TextInline(type=TextInlineType.STYLED, text='msg', bold=True)]
        block = TextBlock(text="hello", inlines=inlines)
        assert block.dict(exclude_none=True) == {
            'type': BlockType.TEXT,
            'text': 'hello',
            'inlines': [{
                'type': 'styled',
                'text': 'msg',
                'bold': True,
            }]
        }

    def test_to_json(self):
        block = TextBlock(text="hello", markdown=False)
        assert block.json(exclude_none=True) == '{"type": "text", "text": "hello", "markdown": false}'

        inlines = [TextInline(type=TextInlineType.STYLED, text='msg', bold=True)]
        block = TextBlock(text="hello", inlines=inlines)
        assert block.json(exclude_none=True) == ('{"type": "text", "text": "hello", "inlines": ' '[{"type": "styled", "text": "msg", "bold": true}]}')

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            TextBlock(**{})

        with pytest.raises(ValidationError):
            TextBlock(**{"type": "####", "text": "hello", "markdown": False})

        assert TextBlock(**{"text": "hello", "markdown": False}) == TextBlock(text='hello', markdown=False)
        assert TextBlock(**{"type": "text", "text": "hello", "markdown": False}) == TextBlock(text="hello", markdown=False)
        assert TextBlock(**{"type": "text", "text": "# title", "markdown": True}) == TextBlock(text="# title", markdown=True)

        inlines = [TextInline(type=TextInlineType.STYLED, text='msg', bold=True)]
        assert TextBlock(**{
            "type": "text",
            "text": "hello",
            "inlines": [{
                "type": "styled",
                "text": "msg",
                "bold": True,
            }]
        }) == TextBlock(text='hello', inlines=inlines)


class TestImageLinkBlock:
    def test_properties(self):
        url = "http://localhost/image.png"
        block = ImageLinkBlock(url=url)
        assert block.type == BlockType.IMAGE_LINK
        assert block.url == url

    def test_validator(self):
        with pytest.raises(ValidationError):
            ImageLinkBlock(url="")

        with pytest.raises(ValidationError):
            ImageLinkBlock(url="$*(#Y$(")

        ImageLinkBlock(url="http://localhost")
        ImageLinkBlock(url="http://localhost/")
        ImageLinkBlock(url="http://localhost/image.png")

    def test_to_dict(self):
        url = "http://localhost/image.png"
        block = ImageLinkBlock(url=url)
        assert block.dict(exclude_none=True) == {
            "type": "image_link",
            "url": "http://localhost/image.png",
        }

    def test_to_json(self):
        url = "http://localhost/image.png"
        block = ImageLinkBlock(url=url)
        assert block.json(exclude_none=True) == '{"type": "image_link", "url": "http://localhost/image.png"}'

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            assert ImageLinkBlock(**{})

        with pytest.raises(ValidationError):
            assert ImageLinkBlock(**{"type": "###", "url": "http://localhost/image.png"})

        assert ImageLinkBlock(**{"url": "http://localhost/image.png"}) == ImageLinkBlock(url="http://localhost/image.png")
        assert ImageLinkBlock(**{"type": "image_link", "url": "http://localhost/image.png"}) == ImageLinkBlock(url="http://localhost/image.png")


class TestButtonBlock:
    def test_properties(self):
        text = "hello"
        block = ButtonBlock(
            text=text,
            style=ButtonStyle.DEFAULT,
        )
        assert block.type == BlockType.BUTTON
        assert block.text == text
        assert block.style == ButtonStyle.DEFAULT
        assert block.action_type is None
        assert block.action_name is None
        assert block.value is None

        action_name = "action"
        value = 'value'
        block = ButtonBlock(
            text=text,
            style=ButtonStyle.PRIMARY,
            action_type=ButtonActionType.OPEN_INAPP_BROWSER,
            action_name=action_name,
            value=value,
        )
        assert block.type == BlockType.BUTTON
        assert block.text == text
        assert block.style == ButtonStyle.PRIMARY
        assert block.action_type == ButtonActionType.OPEN_INAPP_BROWSER
        assert block.action_name == action_name
        assert block.value == value

    def test_validator(self):
        ButtonBlock(text="hello", style=ButtonStyle.PRIMARY)

        with pytest.raises(ValidationError):
            ButtonBlock(text="", style=ButtonStyle.DEFAULT)

        with pytest.raises(ValidationError):
            ButtonBlock(text="a" * 21, style=ButtonStyle.PRIMARY)

    def test_to_dict(self):
        block = ButtonBlock(
            text='hello',
            style=ButtonStyle.PRIMARY,
            action_type=ButtonActionType.OPEN_INAPP_BROWSER,
            action_name='action',
            value='value',
        )
        assert block.dict(exclude_none=True) == {
            "type": "button",
            "text": "hello",
            "style": "primary",
            "action_type": "open_inapp_browser",
            "action_name": "action",
            "value": "value",
        }

    def test_to_json(self):
        block = ButtonBlock(
            text='hello',
            style=ButtonStyle.PRIMARY,
            action_type=ButtonActionType.OPEN_INAPP_BROWSER,
            action_name='action',
            value='value',
        )
        assert block.json(exclude_none=True) == (
            '{"type": "button", "text": "hello", "style": "primary", "action_type": "open_inapp_browser", "action_name": "action", "value": "value"}')

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            ButtonBlock(**{})

        with pytest.raises(ValidationError):
            ButtonBlock(**{
                "type": "####",
                "text": "hello",
                "style": "primary",
                "action_type": "open_inapp_browser",
                "action_name": "action",
                "value": "value",
            })

        assert ButtonBlock(**{
            "text": "hello",
            "style": "primary",
            "action_type": "open_inapp_browser",
            "action_name": "action",
            "value": "value",
        }) == ButtonBlock(text='hello', style=ButtonStyle.PRIMARY, action_type=ButtonActionType.OPEN_INAPP_BROWSER, action_name='action', value='value')
        assert ButtonBlock(**{
            "type": "button",
            "text": "hello",
            "style": "primary",
            "action_type": "open_inapp_browser",
            "action_name": "action",
            "value": "value",
        }) == ButtonBlock(text='hello', style=ButtonStyle.PRIMARY, action_type=ButtonActionType.OPEN_INAPP_BROWSER, action_name='action', value='value')


class TestDividerBlock:
    def test_properties(self):
        block = DividerBlock()
        assert block.type == BlockType.DIVIDER

    def test_to_dict(self):
        block = DividerBlock()
        assert block.dict(exclude_none=True) == {"type": "divider"}

    def test_to_json(self):
        block = DividerBlock()
        assert block.json(exclude_none=True) == '{"type": "divider"}'

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            DividerBlock(**{"type": "####"})

        assert DividerBlock(**{}) == DividerBlock()
        assert DividerBlock(**{"type": "divider"}) == DividerBlock()


class TestHeaderBlock:
    def test_properties(self):
        block = HeaderBlock(text="hello", style=HeaderStyle.YELLOW)
        assert block.type == BlockType.HEADER
        assert block.text == 'hello'
        assert block.style == HeaderStyle.YELLOW

    def test_validator(self):
        HeaderBlock(text="hello", style=HeaderStyle.RED)

        with pytest.raises(ValidationError):
            HeaderBlock(text="", style=HeaderStyle.BLUE)

        with pytest.raises(ValidationError):
            HeaderBlock(text="a" * 21, style=HeaderStyle.YELLOW)

    def test_to_dict(self):
        block = HeaderBlock(text="hello", style=HeaderStyle.YELLOW)
        assert block.dict(exclude_none=True) == {
            "type": "header",
            "text": "hello",
            "style": "yellow",
        }

    def test_to_json(self):
        block = HeaderBlock(text="hello", style=HeaderStyle.YELLOW)
        assert block.json(exclude_none=True) == '{"type": "header", "text": "hello", "style": "yellow"}'

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            HeaderBlock(**{})

        with pytest.raises(ValidationError):
            HeaderBlock(**{"type": "####", "text": "hello", "style": "yellow"})

        assert HeaderBlock(**{"text": "hello", "style": "yellow"}) == HeaderBlock(text="hello", style=HeaderStyle.YELLOW)
        assert HeaderBlock(**{"type": "header", "text": "hello", "style": "yellow"}) == HeaderBlock(text="hello", style=HeaderStyle.YELLOW)


class TestActionBlock:
    def test_properties(self):
        button = ButtonBlock(text="hello", style=ButtonStyle.DEFAULT)
        block = ActionBlock(elements=[button])
        assert block.type == BlockType.ACTION
        assert block.elements == [button]

    def test_validator(self):
        button = ButtonBlock(text="hello", style=ButtonStyle.DEFAULT)
        ActionBlock(elements=[button])

        with pytest.raises(ValidationError):
            ActionBlock(elements=[])

        with pytest.raises(ValidationError):
            ActionBlock(elements=[button] * 4)

    def test_to_dict(self):
        button = ButtonBlock(text="hello", style=ButtonStyle.DEFAULT)
        block = ActionBlock(elements=[button])
        assert block.dict(exclude_none=True) == {
            "type": "action",
            "elements": [{
                "type": "button",
                "text": "hello",
                "style": "default"
            }],
        }

    def test_to_json(self):
        button = ButtonBlock(text="hello", style=ButtonStyle.DEFAULT)
        block = ActionBlock(elements=[button])
        assert block.json(exclude_none=True) == '{"type": "action", "elements": [{"type": "button", "text": "hello", "style": "default"}]}'

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            ActionBlock(**{})

        with pytest.raises(ValidationError):
            ActionBlock(**{"type": "####", "elements": [{"type": "button", "text": "hello", "style": "default"}]})

        with pytest.raises(ValidationError):
            ActionBlock(**{'elements': []})

        assert ActionBlock(**{
            "elements": [{
                "type": "button",
                "text": "hello",
                "style": "default"
            }],
        }) == ActionBlock(elements=[ButtonBlock(text="hello", style=ButtonStyle.DEFAULT)])
        assert ActionBlock(**{
            "type": "action",
            "elements": [{
                "type": "button",
                "text": "hello",
                "style": "default"
            }],
        }) == ActionBlock(elements=[ButtonBlock(text="hello", style=ButtonStyle.DEFAULT)])


class TestDescriptionBlock:
    def test_properties(self):
        content = TextBlock(text='content')
        block = DescriptionBlock(term='hello', content=content, accent=True)
        assert block.type == BlockType.DESCRIPTION
        assert block.term == 'hello'
        assert block.content == content
        assert block.accent is True

    def test_validator(self):
        content = TextBlock(text='content')

        with pytest.raises(ValidationError):
            DescriptionBlock(term="", content=content, accent=False)

        with pytest.raises(ValidationError):
            DescriptionBlock(term="a" * 11, content=content, accent=False)

        DescriptionBlock(term="hello", content=content, accent=False)

    def test_to_dict(self):
        content = TextBlock(text='content')
        block = DescriptionBlock(term='hello', content=content, accent=True)
        assert block.dict(exclude_none=True) == {
            "type": "description",
            "term": "hello",
            "content": {
                "type": "text",
                "text": "content",
            },
            "accent": True,
        }

    def test_to_json(self):
        content = TextBlock(text='content')
        block = DescriptionBlock(term='hello', content=content, accent=True)
        expected_json = '{"type": "description", "term": "hello", "content": {"type": "text", "text": "content"}, "accent": true}'
        assert block.json(exclude_none=True) == expected_json

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            DescriptionBlock(**{})

        with pytest.raises(ValidationError):
            DescriptionBlock(**{"type": "####", "term": "hello", "content": {"type": "text", "text": "content", "markdown": False}, "accent": True})

        assert DescriptionBlock(**{
            "term": "hello",
            "content": {
                "type": "text",
                "text": "content",
                "markdown": False
            },
            "accent": True,
        }) == DescriptionBlock(term="hello", content=TextBlock(text='content', markdown=False), accent=True)
        assert DescriptionBlock(**{
            "type": "description",
            "term": "hello",
            "content": {
                "type": "text",
                "text": "content",
                "markdown": False
            },
            "accent": True,
        }) == DescriptionBlock(term="hello", content=TextBlock(text='content', markdown=False), accent=True)


class TestSectionBlock:
    def test_properties(self):
        content = TextBlock(text='hello')
        accessory = ImageLinkBlock(url='http://localhost/image.png')
        block = SectionBlock(
            content=content,
            accessory=accessory,
        )
        assert block.type == BlockType.SECTION
        assert block.content == content
        assert block.accessory == accessory

    def test_validator(self):
        with pytest.raises(ValidationError):
            SectionBlock()

        content = TextBlock(text='hello')
        accessory = ImageLinkBlock(url='http://localhost/image.png')

        with pytest.raises(ValidationError):
            SectionBlock(content=content)

        with pytest.raises(ValidationError):
            SectionBlock(accessory=accessory)

        SectionBlock(content=content, accessory=accessory)

    def test_to_dict(self):
        content = TextBlock(text='hello')
        accessory = ImageLinkBlock(url='http://localhost/image.png')
        block = SectionBlock(
            content=content,
            accessory=accessory,
        )
        assert block.dict(exclude_none=True) == {
            'type': 'section',
            'content': {
                "type": "text",
                "text": "hello",
            },
            'accessory': {
                "type": "image_link",
                "url": "http://localhost/image.png"
            },
        }

    def test_to_json(self):
        content = TextBlock(text='hello')
        accessory = ImageLinkBlock(url='http://localhost/image.png')
        block = SectionBlock(
            content=content,
            accessory=accessory,
        )
        expected_json = ('{"type": "section", "content": {"type": "text", "text": "hello"},'
                         ' "accessory": {"type": "image_link", "url": "http://localhost/image.png"}}')
        assert block.json(exclude_none=True) == expected_json

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            SectionBlock(**{})

        with pytest.raises(ValidationError):
            SectionBlock(
                **{
                    "type": "####",
                    "content": {
                        "type": "text",
                        "text": "hello",
                        "markdown": False
                    },
                    "accessory": {
                        "type": "image_link",
                        "url": "http://localhost/image.png"
                    },
                })

        assert SectionBlock(**{
            "content": {
                "type": "text",
                "text": "hello",
                "markdown": False,
            },
            "accessory": {
                "type": "image_link",
                "url": "http://localhost/image.png"
            },
        }) == SectionBlock(
            content=TextBlock(text='hello', markdown=False),
            accessory=ImageLinkBlock(url='http://localhost/image.png'),
        )
        data = {
            "type": "section",
            "content": {
                "type": "text",
                "text": "hello",
                "markdown": False,
            },
            "accessory": {
                "type": "image_link",
                "url": "http://localhost/image.png"
            },
        }
        assert SectionBlock(**data) == SectionBlock(
            content=TextBlock(text='hello', markdown=False),
            accessory=ImageLinkBlock(url='http://localhost/image.png'),
        )


class TestContextBlock:
    def test_properties(self):
        content = TextBlock(text='hello')
        image = ImageLinkBlock(url='http://localhost/image.png')
        block = ContextBlock(
            content=content,
            image=image,
        )
        assert block.type == BlockType.CONTEXT
        assert block.content == content
        assert block.image == image

    def test_validator(self):
        with pytest.raises(ValidationError):
            ContextBlock()

        content = TextBlock(text='hello')
        image = ImageLinkBlock(url='http://localhost/image.png')

        with pytest.raises(ValidationError):
            ContextBlock(content=content)

        with pytest.raises(ValidationError):
            ContextBlock(image=image)

        ContextBlock(content=content, image=image)

    def test_to_dict(self):
        content = TextBlock(text='hello')
        image = ImageLinkBlock(url='http://localhost/image.png')
        block = ContextBlock(
            content=content,
            image=image,
        )
        assert block.dict(exclude_none=True) == {
            'type': 'context',
            'content': {
                "type": "text",
                "text": "hello",
            },
            'image': {
                "type": "image_link",
                "url": "http://localhost/image.png"
            },
        }

    def test_to_json(self):
        content = TextBlock(text='hello')
        image = ImageLinkBlock(url='http://localhost/image.png')
        block = ContextBlock(
            content=content,
            image=image,
        )
        expected_json = ('{"type": "context", "content": {"type": "text", "text": "hello"},'
                         ' "image": {"type": "image_link", "url": "http://localhost/image.png"}}')
        assert block.json(exclude_none=True) == expected_json

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            ContextBlock(**{})

        with pytest.raises(ValidationError):
            ContextBlock(
                **{
                    "type": "####",
                    "content": {
                        "type": "text",
                        "text": "hello",
                        "markdown": False
                    },
                    "image": {
                        "type": "image_link",
                        "url": "http://localhost/image.png"
                    },
                })

        assert ContextBlock(**{
            "content": {
                "type": "text",
                "text": "hello",
                "markdown": False,
            },
            "image": {
                "type": "image_link",
                "url": "http://localhost/image.png"
            },
        }) == ContextBlock(
            content=TextBlock(text='hello', markdown=False),
            image=ImageLinkBlock(url='http://localhost/image.png'),
        )
        data = {
            "type": "context",
            "content": {
                "type": "text",
                "text": "hello",
                "markdown": False,
            },
            "image": {
                "type": "image_link",
                "url": "http://localhost/image.png"
            },
        }
        assert ContextBlock(**data) == ContextBlock(
            content=TextBlock(
                text='hello',
                markdown=False,
            ),
            image=ImageLinkBlock(url='http://localhost/image.png'),
        )


class TestLabelBlock:
    def test_properties(self):
        block = LabelBlock(text="hello", markdown=True)
        assert block.type == BlockType.LABEL
        assert block.text == 'hello'
        assert block.markdown is True

    def test_validator(self):
        with pytest.raises(ValidationError):
            LabelBlock()

        with pytest.raises(ValidationError):
            LabelBlock(text="abc")

        with pytest.raises(ValidationError):
            LabelBlock(markdown=True)

        with pytest.raises(ValidationError):
            LabelBlock(text="", markdown=False)

        with pytest.raises(ValidationError):
            LabelBlock(text="a" * 201, markdown=False)

        LabelBlock(text="hello", markdown=True)

    def test_to_dict(self):
        block = LabelBlock(text="hello", markdown=True)
        assert block.dict(exclude_none=True) == {
            "type": "label",
            "text": "hello",
            "markdown": True,
        }

    def test_to_json(self):
        block = LabelBlock(text="hello", markdown=True)
        assert block.json(exclude_none=True) == '{"type": "label", "text": "hello", "markdown": true}'

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            LabelBlock(**{})

        with pytest.raises(ValidationError):
            LabelBlock(**{"type": "####", "text": "hello", "markdown": True})

        assert LabelBlock(**{"text": "hello", "markdown": True}) == LabelBlock(text="hello", markdown=True)
        assert LabelBlock(**{"type": "label", "text": "hello", "markdown": True}) == LabelBlock(text="hello", markdown=True)


class TestInputBlock:
    def test_properties(self):
        block = InputBlock(name="name")
        assert block.type == BlockType.INPUT
        assert block.name == 'name'
        assert block.required is None
        assert block.placeholder is None

        block = InputBlock(name="name", required=True)
        assert block.type == BlockType.INPUT
        assert block.name == 'name'
        assert block.required is True
        assert block.placeholder is None

        block = InputBlock(name="name", required=True, placeholder="placeholder")
        assert block.type == BlockType.INPUT
        assert block.name == 'name'
        assert block.required is True
        assert block.placeholder == 'placeholder'

    def test_validator(self):
        with pytest.raises(ValidationError):
            InputBlock()

        with pytest.raises(ValidationError):
            InputBlock(required=True)

        with pytest.raises(ValidationError):
            InputBlock(placeholder="ph")

        with pytest.raises(ValidationError):
            InputBlock(required=True, placeholder="ph")

        with pytest.raises(ValidationError):
            InputBlock(name="", required=False)

        with pytest.raises(ValidationError):
            InputBlock(name="name", required=False, placeholder='a' * 51)

        InputBlock(name="abc")
        InputBlock(name="name", required=True, placeholder='placeholder')

    def test_to_dict(self):
        block = InputBlock(name="name", required=True, placeholder="placeholder")
        assert block.dict(exclude_none=True) == {
            "type": "input",
            "name": "name",
            "required": True,
            "placeholder": "placeholder",
        }

    def test_to_json(self):
        block = InputBlock(name="name", required=True, placeholder="placeholder")
        assert block.json(exclude_none=True) == '{"type": "input", "name": "name", "required": true, "placeholder": "placeholder"}'

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            InputBlock(**{})

        with pytest.raises(ValidationError):
            InputBlock(**{
                "type": "####",
                "name": "name",
                "required": True,
                "placeholder": "placeholder",
            })

        assert InputBlock(**{
            "name": "name",
            "required": True,
            "placeholder": "placeholder",
        }) == InputBlock(name="name", required=True, placeholder="placeholder")
        assert InputBlock(**{
            "type": "input",
            "name": "name",
            "required": True,
            "placeholder": "placeholder",
        }) == InputBlock(name="name", required=True, placeholder="placeholder")


class TestSelectBlock:
    def test_properties(self):
        options = [SelectBlockOption(text='text', value='text')]

        block = SelectBlock(
            name='name',
            options=options,
        )
        assert block.type == BlockType.SELECT
        assert block.options == options
        assert block.required is None
        assert block.placeholder is None

        block = SelectBlock(name='name', options=options, required=True, placeholder="placeholder")
        assert block.type == BlockType.SELECT
        assert block.options == options
        assert block.required is True
        assert block.placeholder == 'placeholder'

    def test_validator(self):
        with pytest.raises(ValidationError):
            SelectBlock()

        with pytest.raises(ValidationError):
            SelectBlock(required=True)

        with pytest.raises(ValidationError):
            SelectBlock(placeholder='ph')

        with pytest.raises(ValidationError):
            SelectBlock(required=True, placeholder='ph')

        options = [SelectBlockOption(text='text', value='text')]

        with pytest.raises(ValidationError):
            SelectBlock(name="", options=options)

        with pytest.raises(ValidationError):
            SelectBlock(name="name", options=[])

        with pytest.raises(ValidationError):
            SelectBlock(name="name", options=options * 31)

        with pytest.raises(ValidationError):
            SelectBlock(name="name", options=options, placeholder="a" * 51)

        SelectBlock(name="name", options=options)
        SelectBlock(
            name="name",
            options=options,
            placeholder="placeholder",
            required=True,
        )

    def test_to_dict(self):
        options = [SelectBlockOption(text='text', value='text')]
        block = SelectBlock(name='name', options=options, required=True, placeholder="placeholder")
        assert block.dict(exclude_none=True) == {
            "type": "select",
            "name": "name",
            "options": [{
                "text": "text",
                "value": "text"
            }],
            "required": True,
            "placeholder": "placeholder",
        }

    def test_to_json(self):
        options = [SelectBlockOption(text='text', value='text')]
        block = SelectBlock(name='name', options=options, required=True, placeholder="placeholder")
        assert block.json(exclude_none=True) == \
            '{"type": "select", "name": "name", "options": [{"text": "text", "value": "text"}], "required": true, "placeholder": "placeholder"}'

    def test_from_dict(self):
        with pytest.raises(ValidationError):
            SelectBlock(**{})

        with pytest.raises(ValidationError):
            SelectBlock(**{
                "type": "####",
                "name": "name",
                "options": [{
                    "text": "text",
                    "value": "text"
                }],
                "required": True,
                "placeholder": "placeholder",
            })

        assert SelectBlock(**{
            "name": "name",
            "options": [{
                "text": "text",
                "value": "text"
            }],
            "required": True,
            "placeholder": "placeholder",
        }) == SelectBlock(name='name', options=[SelectBlockOption(text='text', value='text')], required=True, placeholder="placeholder")
        assert SelectBlock(**{
            "type": "select",
            "name": "name",
            "options": [{
                "text": "text",
                "value": "text"
            }],
            "required": True,
            "placeholder": "placeholder",
        }) == SelectBlock(name='name', options=[SelectBlockOption(text='text', value='text')], required=True, placeholder="placeholder")


class TestBlockKitBuilder:
    def test_message_properties(self):
        builder = BlockKitBuilder(type=BlockKitType.MESSAGE)
        assert builder.type == BlockKitType.MESSAGE
        assert builder.blocks == []

        divider = DividerBlock()
        builder = BlockKitBuilder(type=BlockKitType.MESSAGE, text='hello', blocks=[divider])
        assert builder.type == BlockKitType.MESSAGE
        assert builder.text == 'hello'
        assert builder.blocks == [divider]

        with pytest.raises(ValidationError):
            builder.title = 'title'
        assert builder.title is None

        with pytest.raises(ValidationError):
            builder.accept = 'ok'
        assert builder.accept is None

        with pytest.raises(ValidationError):
            builder.decline = 'cancel'
        assert builder.decline is None

        with pytest.raises(ValidationError):
            builder.value = 'value'
        assert builder.value is None

    def test_modal_properties(self):
        builder = BlockKitBuilder(type=BlockKitType.MODAL)
        assert builder.type == BlockKitType.MODAL
        assert builder.blocks == []

        divider = DividerBlock()
        builder = BlockKitBuilder(
            type=BlockKitType.MODAL,
            title='title',
            accept='ok',
            decline='cancel',
            value='value',
            blocks=[divider],
        )
        assert builder.type == BlockKitType.MODAL
        assert builder.title == 'title'
        assert builder.accept == 'ok'
        assert builder.decline == 'cancel'
        assert builder.value == 'value'
        assert builder.blocks == [divider]

        with pytest.raises(ValidationError):
            builder.text = 'hello'
        assert builder.text is None

    def test_message_add_block(self):
        divider = DividerBlock()

        builder = BlockKitBuilder(type=BlockKitType.MESSAGE)
        builder.add_block(divider)
        assert builder.blocks[-1] == divider

        with pytest.raises(ValidationError):
            builder.add_block({'type': 'text', 'text': '', 'markdown': False})

        builder.add_block({'type': 'text', 'text': 'hello', 'markdown': False})
        assert builder.blocks[-1] == TextBlock(text='hello', markdown=False)

    def test_modal_add_block(self):
        divider = DividerBlock()

        builder = BlockKitBuilder(type=BlockKitType.MODAL)
        builder.add_block(divider)
        assert builder.blocks[-1] == divider

        with pytest.raises(ValidationError):
            builder.add_block({'type': 'text', 'text': '', 'markdown': False})

        builder.add_block({'type': 'text', 'text': 'hello', 'markdown': False})
        assert builder.blocks[-1] == TextBlock(text='hello', markdown=False)

    def test_load(self, mocker: MockerFixture):
        json_str = json.dumps({
            'type': 'message',
            'text': 'hello',
            'blocks': [
                {
                    'type': 'text',
                    'text': 'block',
                    'markdown': False,
                },
            ],
        })
        mocker.patch('builtins.open', mock_open(read_data=json_str))

        builder = BlockKitBuilder(type=BlockKitType.MESSAGE)
        builder.load('/path/to/jsonfile')

        assert builder.type == BlockKitType.MESSAGE
        assert builder.text == 'hello'
        assert builder.blocks == [TextBlock(text='block', markdown=False)]
