import json
from unittest.mock import mock_open
from contextlib import ExitStack as does_not_raise

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
    def test_properties(self):
        text = 'hello'
        block = TextInline(
            type=TextInlineType.STYLED,
            text=text,
        )
        assert block.type == TextInlineType.STYLED
        assert block.text == text
        assert block.bold is None
        assert block.italic is None
        assert block.strike is None
        assert block.color is None
        assert block.url is None

    @pytest.mark.parametrize(
        'attributes,raises',
        [
            (dict(), pytest.raises(ValidationError)),
            (dict(type='####', text='msg'), pytest.raises(ValidationError)),
            (dict(type=TextInlineType.STYLED, text='msg', bold=True), does_not_raise()),
            (dict(type=TextInlineType.STYLED, text='msg', bold=False), does_not_raise()),
            (dict(type=TextInlineType.STYLED, text='msg', italic=True), does_not_raise()),
            (dict(type=TextInlineType.STYLED, text='msg', italic=False), does_not_raise()),
            (dict(type=TextInlineType.STYLED, text='msg', strike=True), does_not_raise()),
            (dict(type=TextInlineType.STYLED, text='msg', strike=False), does_not_raise()),
            (dict(type=TextInlineType.STYLED, text='msg', color=True), does_not_raise()),
            (dict(type=TextInlineType.STYLED, text='msg', color=False), does_not_raise()),
            (dict(type=TextInlineType.STYLED, text='msg', bold=True, italic=True, strike=True, color=True), does_not_raise()),
            (dict(type=TextInlineType.STYLED, text='msg', bold=False, italic=False, strike=False, color=False), does_not_raise()),
            (dict(type=TextInlineType.STYLED, text='msg', url='http://localhost'), pytest.raises(ValidationError)),
            (dict(type=TextInlineType.LINK, text='msg', url='http://localhost'), does_not_raise()),
            (dict(type=TextInlineType.LINK, text='msg', bold=True), pytest.raises(ValidationError)),
            (dict(type=TextInlineType.LINK, text='msg', bold=False), pytest.raises(ValidationError)),
            (dict(type=TextInlineType.LINK, text='msg', italic=True), pytest.raises(ValidationError)),
            (dict(type=TextInlineType.LINK, text='msg', italic=False), pytest.raises(ValidationError)),
            (dict(type=TextInlineType.LINK, text='msg', strike=True), pytest.raises(ValidationError)),
            (dict(type=TextInlineType.LINK, text='msg', strike=False), pytest.raises(ValidationError)),
            (dict(type=TextInlineType.LINK, text='msg', color=True), pytest.raises(ValidationError)),
            (dict(type=TextInlineType.LINK, text='msg', color=False), pytest.raises(ValidationError)),
            (dict(type=TextInlineType.LINK, text='msg', bold=True, italic=True, strike=True, color=True), pytest.raises(ValidationError)),
            (dict(type=TextInlineType.LINK, text='msg', bold=False, italic=False, strike=False, color=False), pytest.raises(ValidationError)),
        ],
    )
    def test_validator(self, attributes, raises):
        with raises:
            TextInline(**attributes)

    @pytest.mark.parametrize(
        'attributes,expectation',
        [
            (dict(type=TextInlineType.STYLED, text='msg', bold=True, color=TextInlineColor.GREY), {
                'type': 'styled',
                'text': 'msg',
                'bold': True,
                'color': 'grey'
            }),
            (
                dict(type=TextInlineType.LINK, text='msg', url='http://localhost'),
                {
                    'type': 'link',
                    'text': 'msg',
                    'url': 'http://localhost'
                },
            ),
        ],
    )
    def test_to_dict(self, attributes, expectation):
        assert TextInline(**attributes).dict(exclude_none=True) == expectation


class TestButtonStyle:
    def test_missing(self):
        assert ButtonStyle('#####') is ButtonStyle.DEFAULT


class TestHeaderStyle:
    def test_missing(self):
        assert HeaderStyle('#####') is HeaderStyle.BLUE


class TestTextBlock:
    def test_properties(self):
        text = 'hello'
        block = TextBlock(text=text)
        assert block.type == BlockType.TEXT
        assert block.text == text
        assert block.markdown is None
        assert block.inlines is None

    @pytest.mark.parametrize(
        'attributes,raises',
        [
            (dict(), pytest.raises(ValidationError)),
            (dict(type='####', text='msg'), pytest.raises(ValidationError)),
            (dict(text="hello"), does_not_raise()),
            (dict(text="hello", markdown=True), does_not_raise()),
            (dict(text="hello", markdown=False), does_not_raise()),
            (dict(text=""), pytest.raises(ValidationError)),
            (dict(text="a" * 501, markdown=False), pytest.raises(ValidationError)),
            (dict(text='hello', inlines=[TextInline(type=TextInlineType.STYLED, text='msg')]), does_not_raise()),
            (dict(text='hello', inlines=[TextInline(type=TextInlineType.STYLED, text='a' * 501)]), pytest.raises(ValidationError)),
            (dict(text='hello', inlines=[TextInline(type=TextInlineType.STYLED, text='a' * 251)] * 2), pytest.raises(ValidationError)),
            (dict(text='hello', markdown=True, inlines=[TextInline(type=TextInlineType.STYLED, text='msg', bold=True)]), pytest.raises(ValidationError)),
        ],
    )
    def test_validator(self, attributes, raises):
        with raises:
            TextBlock(**attributes)

    @pytest.mark.parametrize(
        'attributes,expectation',
        [
            (dict(text="hello", markdown=False), {
                'type': BlockType.TEXT,
                'text': 'hello',
                'markdown': False,
            }),
            (dict(text="hello", inlines=[TextInline(type=TextInlineType.STYLED, text='msg', bold=True)]), {
                'type': BlockType.TEXT,
                'text': 'hello',
                'inlines': [{
                    'type': 'styled',
                    'text': 'msg',
                    'bold': True,
                }]
            }),
        ],
    )
    def test_to_dict(self, attributes, expectation):
        assert TextBlock(**attributes).dict(exclude_none=True) == expectation

    @pytest.mark.parametrize(
        'attributes,expectation',
        [
            (dict(text="hello", markdown=False), '{"type": "text", "text": "hello", "markdown": false}'),
            (dict(text="hello", inlines=[
                TextInline(type=TextInlineType.STYLED, text='msg', bold=True),
            ]), '{"type": "text", "text": "hello", "inlines": [{"type": "styled", "text": "msg", "bold": true}]}'),
        ],
    )
    def test_to_json(self, attributes, expectation):
        assert TextBlock(**attributes).json(exclude_none=True) == expectation


class TestImageLinkBlock:
    def test_properties(self):
        url = 'http://localhost/image.png'
        block = ImageLinkBlock(url=url)
        assert block.type == BlockType.IMAGE_LINK
        assert block.url == url

    @pytest.mark.parametrize('attributes,raises', [
        (dict(), pytest.raises(ValidationError)),
        (dict(type='####', url='http://localhost/image.png'), pytest.raises(ValidationError)),
        (dict(url='$*(#Y$('), pytest.raises(ValidationError)),
        (dict(url='http://localhost'), does_not_raise()),
        (dict(url='http://localhost/image.png'), does_not_raise()),
    ])
    def test_validator(self, attributes, raises):
        with raises:
            ImageLinkBlock(**attributes)

    def test_to_dict(self):
        assert ImageLinkBlock(url='http://localhost/image.png').dict(exclude_none=True) == {
            "type": "image_link",
            "url": "http://localhost/image.png",
        }

    def test_to_json(self):
        assert ImageLinkBlock(url='http://localhost/image.png').json(exclude_none=True) == '{"type": "image_link", "url": "http://localhost/image.png"}'


class TestButtonBlock:
    def test_properties(self):
        text = 'hello'
        block = ButtonBlock(text=text)
        assert block.type == BlockType.BUTTON
        assert block.text == text
        assert block.style == ButtonStyle.DEFAULT
        assert block.action_type is None
        assert block.action_name is None
        assert block.value is None

    @pytest.mark.parametrize(
        'attributes,raises',
        [
            (dict(), pytest.raises(ValidationError)),
            (dict(text=""), pytest.raises(ValidationError)),
            (dict(type='####', text="msg"), pytest.raises(ValidationError)),
            (dict(text="msg", style=ButtonStyle.PRIMARY), does_not_raise()),
            (dict(text="msg", action_type=ButtonActionType.OPEN_INAPP_BROWSER, action_name='name', value='value'), does_not_raise()),
            (dict(text="msg", style=ButtonStyle.PRIMARY, action_type=ButtonActionType.OPEN_INAPP_BROWSER, action_name='name', value='value'), does_not_raise()),
            (dict(text="a" * 21), pytest.raises(ValidationError)),
        ],
    )
    def test_validator(self, attributes, raises):
        with raises:
            ButtonBlock(**attributes)

    @pytest.mark.parametrize(
        'attributes,expectation',
        [
            (dict(text='msg'), {
                'type': 'button',
                'text': 'msg',
                'style': 'default'
            }),
            (dict(
                text='hello',
                style=ButtonStyle.PRIMARY,
                action_type=ButtonActionType.OPEN_INAPP_BROWSER,
                action_name='action',
                value='value',
            ), {
                "type": "button",
                "text": "hello",
                "style": "primary",
                "action_type": "open_inapp_browser",
                "action_name": "action",
                "value": "value",
            }),
        ],
    )
    def test_to_dict(self, attributes, expectation):
        assert ButtonBlock(**attributes).dict(exclude_none=True) == expectation

    @pytest.mark.parametrize(
        'attributes,expectation',
        [
            (dict(text='msg'), '{"type": "button", "text": "msg", "style": "default"}'),
            (dict(
                text='hello',
                style=ButtonStyle.PRIMARY,
                action_type=ButtonActionType.OPEN_INAPP_BROWSER,
                action_name='action',
                value='value',
            ), '{"type": "button", "text": "hello", "style": "primary", "action_type": "open_inapp_browser", "action_name": "action", "value": "value"}'),
        ],
    )
    def test_to_json(self, attributes, expectation):
        assert ButtonBlock(**attributes).json(exclude_none=True) == expectation


class TestDividerBlock:
    def test_properties(self):
        block = DividerBlock()
        assert block.type == BlockType.DIVIDER

    @pytest.mark.parametrize(
        'attributes,raises',
        [
            (dict(type='####'), pytest.raises(ValidationError)),
            (dict(), does_not_raise()),
            (dict(type='divider'), does_not_raise()),
        ],
    )
    def test_validator(self, attributes, raises):
        with raises:
            DividerBlock(**attributes)

    def test_to_dict(self):
        assert DividerBlock().dict(exclude_none=True) == {"type": "divider"}

    def test_to_json(self):
        assert DividerBlock().json(exclude_none=True) == '{"type": "divider"}'


class TestHeaderBlock:
    def test_properties(self):
        text = 'msg'
        block = HeaderBlock(text=text)
        assert block.type == BlockType.HEADER
        assert block.text == text
        assert block.style == HeaderStyle.BLUE

    @pytest.mark.parametrize(
        'attributes,raises',
        [
            (dict(), pytest.raises(ValidationError)),
            (dict(type='####'), pytest.raises(ValidationError)),
            (dict(text=''), pytest.raises(ValidationError)),
            (dict(text="a" * 21), pytest.raises(ValidationError)),
            (dict(text="hello", style=HeaderStyle.RED), does_not_raise()),
        ],
    )
    def test_validator(self, attributes, raises):
        with raises:
            HeaderBlock(**attributes)

    @pytest.mark.parametrize(
        'attributes,expectation',
        [
            (dict(text='msg'), {
                'type': 'header',
                'text': 'msg',
                'style': 'blue'
            }),
            (dict(text='msg', style=HeaderStyle.YELLOW), {
                'type': 'header',
                'text': 'msg',
                'style': 'yellow'
            }),
        ],
    )
    def test_to_dict(self, attributes, expectation):
        assert HeaderBlock(**attributes).dict(exclude_none=True) == expectation

    @pytest.mark.parametrize(
        'attributes,expectation',
        [
            (dict(text='msg'), '{"type": "header", "text": "msg", "style": "blue"}'),
            (dict(text='msg', style=HeaderStyle.YELLOW), '{"type": "header", "text": "msg", "style": "yellow"}'),
        ],
    )
    def test_to_json(self, attributes, expectation):
        assert HeaderBlock(**attributes).json(exclude_none=True) == expectation


class TestActionBlock:
    def test_properties(self):
        elements = [ButtonBlock(text="hello")]
        block = ActionBlock(elements=elements)
        assert block.type == BlockType.ACTION
        assert block.elements == elements

    @pytest.mark.parametrize(
        'attributes,raises',
        [
            (dict(), pytest.raises(ValidationError)),
            (dict(type='####'), pytest.raises(ValidationError)),
            (dict(elements=[]), pytest.raises(ValidationError)),
            (dict(elements=[ButtonBlock(text='msg')] * 4), pytest.raises(ValidationError)),
            (dict(elements=[ButtonBlock(text='msg')]), does_not_raise()),
        ],
    )
    def test_validator(self, attributes, raises):
        with raises:
            ActionBlock(**attributes)

    @pytest.mark.parametrize(
        'attributes,expectation',
        [
            (dict(elements=[ButtonBlock(text='msg')]), {
                "type": "action",
                "elements": [{
                    "type": "button",
                    "text": "msg",
                    "style": "default"
                }],
            }),
        ],
    )
    def test_to_dict(self, attributes, expectation):
        assert ActionBlock(**attributes).dict(exclude_none=True) == expectation

    @pytest.mark.parametrize(
        'attributes,expectation',
        [
            (dict(elements=[ButtonBlock(text='msg')]), '{"type": "action", "elements": [{"type": "button", "text": "msg", "style": "default"}]}'),
        ],
    )
    def test_to_json(self, attributes, expectation):
        assert ActionBlock(**attributes).json(exclude_none=True) == expectation


class TestDescriptionBlock:
    def test_properties(self):
        content = TextBlock(text='content')
        block = DescriptionBlock(term='hello', content=content)
        assert block.type == BlockType.DESCRIPTION
        assert block.term == 'hello'
        assert block.content == content
        assert block.accent is None

    @pytest.mark.parametrize(
        'attributes,raises',
        [
            (dict(), pytest.raises(ValidationError)),
            (dict(type='####'), pytest.raises(ValidationError)),
            (dict(term="msg"), pytest.raises(ValidationError)),
            (dict(content=TextBlock(text='msg')), pytest.raises(ValidationError)),
            (dict(term="", content=TextBlock(text='msg')), pytest.raises(ValidationError)),
            (dict(term="a" * 11, content=TextBlock(text='msg')), pytest.raises(ValidationError)),
            (dict(term="msg", content=TextBlock(text='msg')), does_not_raise()),
            (dict(term="msg", content=TextBlock(text='msg'), accent=True), does_not_raise()),
            (dict(term="msg", content=TextBlock(text='msg'), accent=False), does_not_raise()),
        ],
    )
    def test_validator(self, attributes, raises):
        with raises:
            DescriptionBlock(**attributes)

    @pytest.mark.parametrize(
        'attributes,expectation',
        [
            (dict(term='msg', content=TextBlock(text='msg')), {
                "type": "description",
                "term": "msg",
                "content": {
                    "type": "text",
                    "text": "msg",
                },
            }),
            (dict(term='msg', content=TextBlock(text='msg'), accent=True), {
                "type": "description",
                "term": "msg",
                "content": {
                    "type": "text",
                    "text": "msg",
                },
                "accent": True,
            }),
        ],
    )
    def test_to_dict(self, attributes, expectation):
        assert DescriptionBlock(**attributes).dict(exclude_none=True) == expectation

    @pytest.mark.parametrize('attributes,expectation', [
        (dict(term='msg', content=TextBlock(text='msg')), '{"type": "description", "term": "msg", "content": {"type": "text", "text": "msg"}}'),
        (dict(
            term='msg',
            content=TextBlock(text='msg'),
            accent=True,
        ), '{"type": "description", "term": "msg", "content": {"type": "text", "text": "msg"}, "accent": true}'),
    ])
    def test_to_json(self, attributes, expectation):
        assert DescriptionBlock(**attributes).json(exclude_none=True) == expectation


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

    @pytest.mark.parametrize(
        'attributes,raises',
        [
            (dict(), pytest.raises(ValidationError)),
            (dict(type='####'), pytest.raises(ValidationError)),
            (dict(content=TextBlock(text='msg')), pytest.raises(ValidationError)),
            (dict(accessory=ImageLinkBlock(url='http://localhost/image.png')), pytest.raises(ValidationError)),
            (dict(content=TextBlock(text='msg'), accessory=ImageLinkBlock(url='http://localhost/image.png')), does_not_raise()),
        ],
    )
    def test_validator(self, attributes, raises):
        with raises:
            SectionBlock(**attributes)

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

    @pytest.mark.parametrize(
        'attributes,raises',
        [
            (dict(), pytest.raises(ValidationError)),
            (dict(type='####'), pytest.raises(ValidationError)),
            (dict(content=TextBlock(text='msg')), pytest.raises(ValidationError)),
            (dict(image=ImageLinkBlock(url='http://localhost/image.png')), pytest.raises(ValidationError)),
            (dict(content=TextBlock(text='msg'), image=ImageLinkBlock(url='http://localhost/image.png')), does_not_raise()),
        ],
    )
    def test_validator(self, attributes, raises):
        with raises:
            ContextBlock(**attributes)

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


class TestLabelBlock:
    def test_properties(self):
        block = LabelBlock(text="msg", markdown=True)
        assert block.type == BlockType.LABEL
        assert block.text == 'msg'
        assert block.markdown is True

    @pytest.mark.parametrize(
        'attributes,raises',
        [
            (dict(), pytest.raises(ValidationError)),
            (dict(type='####'), pytest.raises(ValidationError)),
            (dict(text='msg'), pytest.raises(ValidationError)),
            (dict(text=''), pytest.raises(ValidationError)),
            (dict(text='a' * 201), pytest.raises(ValidationError)),
            (dict(markdown=True), pytest.raises(ValidationError)),
            (dict(text='msg', markdown=True), does_not_raise()),
        ],
    )
    def test_validator(self, attributes, raises):
        with raises:
            LabelBlock(**attributes)

    def test_to_dict(self):
        assert LabelBlock(text="msg", markdown=True).dict(exclude_none=True) == {
            "type": "label",
            "text": "msg",
            "markdown": True,
        }

    def test_to_json(self):
        assert LabelBlock(text="msg", markdown=True).json(exclude_none=True) == '{"type": "label", "text": "msg", "markdown": true}'


class TestInputBlock:
    def test_properties(self):
        name = 'name'
        block = InputBlock(name=name)
        assert block.type == BlockType.INPUT
        assert block.name == name
        assert block.required is None
        assert block.placeholder is None

    @pytest.mark.parametrize(
        'attributes,raises',
        [
            (dict(), pytest.raises(ValidationError)),
            (dict(type='####'), pytest.raises(ValidationError)),
            (dict(name=''), pytest.raises(ValidationError)),
            (dict(name='name', placeholder='a' * 51), pytest.raises(ValidationError)),
            (dict(required=True), pytest.raises(ValidationError)),
            (dict(placeholder='ph'), pytest.raises(ValidationError)),
            (dict(required=True, placeholder='ph'), pytest.raises(ValidationError)),
            (dict(name='name'), does_not_raise()),
            (dict(name='name', required=True), does_not_raise()),
            (dict(name='name', placeholder='ph'), does_not_raise()),
            (dict(name='name', required=True, placeholder='ph'), does_not_raise()),
        ],
    )
    def test_validator(self, attributes, raises):
        with raises:
            InputBlock(**attributes)

    @pytest.mark.parametrize(
        'attributes,expectation',
        [
            (dict(name='name'), {
                'type': 'input',
                'name': 'name'
            }),
            (dict(name='name', required=True, placeholder='placeholder'), {
                "type": "input",
                "name": "name",
                "required": True,
                "placeholder": "placeholder",
            }),
        ],
    )
    def test_to_dict(self, attributes, expectation):
        assert InputBlock(**attributes).dict(exclude_none=True) == expectation

    @pytest.mark.parametrize(
        'attributes,expectation',
        [
            (dict(name='name'), '{"type": "input", "name": "name"}'),
            (dict(name='name', required=True, placeholder='placeholder'), '{"type": "input", "name": "name", "required": true, "placeholder": "placeholder"}'),
        ],
    )
    def test_to_json(self, attributes, expectation):
        assert InputBlock(**attributes).json(exclude_none=True) == expectation


class TestSelectBlock:
    def test_properties(self):
        name = 'name'
        options = [SelectBlockOption(text='text', value='text')]
        block = SelectBlock(
            name=name,
            options=options,
        )
        assert block.type == BlockType.SELECT
        assert block.name == name
        assert block.options == options
        assert block.required is None
        assert block.placeholder is None

    @pytest.mark.parametrize(
        'attributes,raises',
        [
            (dict(), pytest.raises(ValidationError)),
            (dict(type='####'), pytest.raises(ValidationError)),
            (dict(name=''), pytest.raises(ValidationError)),
            (dict(name='name', options=[]), pytest.raises(ValidationError)),
            (dict(options=[SelectBlockOption(text='msg', value='val')]), pytest.raises(ValidationError)),
            (dict(required=True), pytest.raises(ValidationError)),
            (dict(placeholder='ph'), pytest.raises(ValidationError)),
            (dict(required=True, placeholder='ph'), pytest.raises(ValidationError)),
            (dict(name='name', options=[SelectBlockOption(text='msg', value='val')] * 31), pytest.raises(ValidationError)),
            (dict(name='name', options=[SelectBlockOption(text='msg', value='val')], placeholder='a' * 51), pytest.raises(ValidationError)),
            (dict(name='name', options=[SelectBlockOption(text='msg', value='val')]), does_not_raise()),
            (dict(name='name', options=[SelectBlockOption(text='msg', value='val')], required=True), does_not_raise()),
            (dict(name='name', options=[SelectBlockOption(text='msg', value='val')], required=False), does_not_raise()),
            (dict(name='name', options=[SelectBlockOption(text='msg', value='val')], placeholder='ph'), does_not_raise()),
            (dict(name='name', options=[SelectBlockOption(text='msg', value='val')], required=True, placeholder='ph'), does_not_raise()),
            (dict(name='name', options=[SelectBlockOption(text='msg', value='val')], required=False, placeholder='ph'), does_not_raise()),
        ],
    )
    def test_validator(self, attributes, raises):
        with raises:
            SelectBlock(**attributes)

    @pytest.mark.parametrize(
        'attributes,expectation',
        [
            (dict(name='name', options=[SelectBlockOption(text='msg', value='val')]), {
                'type': 'select',
                'name': 'name',
                'options': [{
                    'text': 'msg',
                    'value': 'val'
                }]
            }),
            (dict(name='name', options=[SelectBlockOption(text='msg', value='val')], required=True, placeholder='ph'), {
                "type": "select",
                "name": "name",
                "options": [{
                    "text": "msg",
                    "value": "val"
                }],
                "required": True,
                "placeholder": "ph",
            }),
        ],
    )
    def test_to_dict(self, attributes, expectation):
        assert SelectBlock(**attributes).dict(exclude_none=True) == expectation

    @pytest.mark.parametrize(
        'attributes,expectation',
        [
            (dict(
                name='name',
                options=[SelectBlockOption(text='msg', value='val')],
            ), '{"type": "select", "name": "name", "options": [{"text": "msg", "value": "val"}]}'),
            (
                dict(
                    name='name',
                    options=[SelectBlockOption(text='msg', value='val')],
                    required=True,
                    placeholder='ph',
                ),
                '{"type": "select", "name": "name", "options": [{"text": "msg", "value": "val"}], "required": true, "placeholder": "ph"}',
            ),
        ],
    )
    def test_to_json(self, attributes, expectation):
        assert SelectBlock(**attributes).json(exclude_none=True) == expectation


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

        builder = BlockKitBuilder.load('/path/to/jsonfile')

        assert builder.type == BlockKitType.MESSAGE
        assert builder.text == 'hello'
        assert builder.blocks == [TextBlock(text='block', markdown=False)]
