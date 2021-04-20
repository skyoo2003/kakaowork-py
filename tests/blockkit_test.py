import pytest

from kakaowork.blockkit import (
    BlockType,
    ButtonStyle,
    ButtonActionType,
    HeaderStyle,
    BlockKitType,
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
from kakaowork.exceptions import InvalidBlockType


class TestTextBlock:
    def test_text_block_properties(self):
        text = '"hello"'
        block = TextBlock(text=text, markdown=False)
        assert block.block_type == BlockType.TEXT
        assert block.text == text
        assert block.markdown is False

    def test_text_block_validate(self):
        assert TextBlock(text="", markdown=False).validate() is False
        assert TextBlock(text="a" * 501, markdown=False).validate() is False
        assert TextBlock(text="hello", markdown=False).validate() is True

    def test_text_block_to_dict(self):
        block = TextBlock(text="hello", markdown=False)
        assert block.to_dict() == {
            'type': 'text',
            'text': 'hello',
            'markdown': False,
        }

    def test_text_block_to_json(self):
        block = TextBlock(text="hello", markdown=False)
        assert block.to_json() == '{"type": "text", "text": "hello", "markdown": false}'


class TestImageLinkBlock:
    def test_image_link_block_properties(self):
        url = "http://localhost/image.png"
        block = ImageLinkBlock(url=url)
        assert block.block_type == BlockType.IMAGE_LINK
        assert block.url == url

    def test_image_link_block_validate(self):
        assert ImageLinkBlock(url="").validate() is False
        assert ImageLinkBlock(url="$*(#Y$(").validate() is False
        assert ImageLinkBlock(url="http://localhost").validate() is False
        assert ImageLinkBlock(url="http://localhost/").validate() is False
        assert ImageLinkBlock(url="http://localhost/image.png").validate() is True

    def test_image_link_block_to_dict(self):
        url = "http://localhost/image.png"
        block = ImageLinkBlock(url=url)
        assert block.to_dict() == {
            "type": "image_link",
            "url": "http://localhost/image.png",
        }

    def test_image_link_block_to_json(self):
        url = "http://localhost/image.png"
        block = ImageLinkBlock(url=url)
        assert block.to_json() == '{"type": "image_link", "url": "http://localhost/image.png"}'


class TestButtonBlock:
    def test_button_block_properties(self):
        text = "hello"
        block = ButtonBlock(
            text=text,
            style=ButtonStyle.DEFAULT,
        )
        assert block.block_type == BlockType.BUTTON
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
        assert block.block_type == BlockType.BUTTON
        assert block.text == text
        assert block.style == ButtonStyle.PRIMARY
        assert block.action_type == ButtonActionType.OPEN_INAPP_BROWSER
        assert block.action_name == action_name
        assert block.value == value

    def test_button_block_validate(self):
        assert ButtonBlock(text="", style=ButtonStyle.DEFAULT).validate() is False
        assert ButtonBlock(text="a" * 21, style=ButtonStyle.PRIMARY).validate() is False
        assert ButtonBlock(text="hello", style=ButtonStyle.PRIMARY).validate() is True

    def test_button_block_to_dict(self):
        block = ButtonBlock(
            text='hello',
            style=ButtonStyle.PRIMARY,
            action_type=ButtonActionType.OPEN_INAPP_BROWSER,
            action_name='action',
            value='value',
        )
        assert block.to_dict() == {
            "type": "button",
            "text": "hello",
            "style": "primary",
            "action_type": "open_inapp_browser",
            "action_name": "action",
            "value": "value",
        }

    def test_button_block_to_json(self):
        block = ButtonBlock(
            text='hello',
            style=ButtonStyle.PRIMARY,
            action_type=ButtonActionType.OPEN_INAPP_BROWSER,
            action_name='action',
            value='value',
        )
        expected_json = ('{"type": "button", "text": "hello", "style": "primary", '
                         '"action_type": "open_inapp_browser", "action_name": "action", "value": "value"}')
        assert block.to_json() == expected_json


class TestDividerBlock:
    def test_divider_block_properties(self):
        block = DividerBlock()
        assert block.block_type == BlockType.DIVIDER

    def test_divider_block_validate(self):
        assert DividerBlock().validate() is True

    def test_divider_block_to_dict(self):
        block = DividerBlock()
        assert block.to_dict() == {"type": "divider"}

    def test_divider_block_to_json(self):
        block = DividerBlock()
        assert block.to_json() == '{"type": "divider"}'


class TestHeaderBlock:
    def test_header_block_properties(self):
        block = HeaderBlock(text="hello", style=HeaderStyle.YELLOW)
        assert block.block_type == BlockType.HEADER
        assert block.text == 'hello'
        assert block.style == HeaderStyle.YELLOW

    def test_header_block_validate(self):
        assert HeaderBlock(text="", style=HeaderStyle.BLUE).validate() is False
        assert HeaderBlock(text="a" * 21, style=HeaderStyle.YELLOW).validate() is False
        assert HeaderBlock(text="hello", style=HeaderStyle.RED).validate() is True

    def test_header_block_to_dict(self):
        block = HeaderBlock(text="hello", style=HeaderStyle.YELLOW)
        assert block.to_dict() == {
            "type": "header",
            "text": "hello",
            "style": "yellow",
        }

    def test_header_block_to_json(self):
        block = HeaderBlock(text="hello", style=HeaderStyle.YELLOW)
        assert block.to_json() == '{"type": "header", "text": "hello", "style": "yellow"}'


class TestActionBlock:
    def test_action_block_properties(self):
        button = ButtonBlock(text="hello", style=ButtonStyle.DEFAULT)
        block = ActionBlock(elements=[button])
        assert block.block_type == BlockType.ACTION
        assert block.elements == [button]

    def test_action_block_validate(self):
        button = ButtonBlock(text="hello", style=ButtonStyle.DEFAULT)
        assert ActionBlock(elements=[]).validate() is False
        assert ActionBlock(elements=[button]).validate() is True

    def test_action_block_to_dict(self):
        button = ButtonBlock(text="hello", style=ButtonStyle.DEFAULT)
        block = ActionBlock(elements=[button])
        assert block.to_dict() == {
            "type": "action",
            "elements": [button],
        }

    def test_action_block_to_json(self):
        button = ButtonBlock(text="hello", style=ButtonStyle.DEFAULT)
        block = ActionBlock(elements=[button])
        assert block.to_json() == '{"type": "action", "elements": [{"type": "button", "text": "hello", "style": "default"}]}'


class TestDescriptionBlock:
    def test_description_block_properties(self):
        content = TextBlock(text='content')
        block = DescriptionBlock(term='hello', content=content, accent=True)
        assert block.block_type == BlockType.DESCRIPTION
        assert block.term == 'hello'
        assert block.content == content
        assert block.accent is True

    def test_description_block_validate(self):
        content = TextBlock(text='content')
        assert DescriptionBlock(term="", content=content, accent=False).validate() is False
        assert DescriptionBlock(term="a" * 11, content=content, accent=False).validate() is False
        assert DescriptionBlock(term="hello", content=content, accent=False).validate() is True

    def test_description_block_to_dict(self):
        content = TextBlock(text='content')
        block = DescriptionBlock(term='hello', content=content, accent=True)
        assert block.to_dict() == {
            "type": "description",
            "term": "hello",
            "content": content,
            "accent": True,
        }

    def test_description_block_to_json(self):
        content = TextBlock(text='content')
        block = DescriptionBlock(term='hello', content=content, accent=True)
        expected_json = '{"type": "description", "term": "hello", "content": {"type": "text", "text": "content", "markdown": false}, "accent": true}'
        assert block.to_json() == expected_json


class TestSectionBlock:
    def test_section_block_properties(self):
        content = TextBlock(text='hello')
        accessory = ImageLinkBlock(url='http://localhost/image.png')
        block = SectionBlock(
            content=content,
            accessory=accessory,
        )
        assert block.block_type == BlockType.SECTION
        assert block.content == content
        assert block.accessory == accessory

    def test_section_block_validate(self):
        content = TextBlock(text='hello')
        accessory = ImageLinkBlock(url='http://localhost/image.png')
        assert SectionBlock(content=content, accessory=accessory).validate() is True

    def test_section_block_to_dict(self):
        content = TextBlock(text='hello')
        accessory = ImageLinkBlock(url='http://localhost/image.png')
        block = SectionBlock(
            content=content,
            accessory=accessory,
        )
        assert block.to_dict() == {
            'type': 'section',
            'content': content,
            'accessory': accessory,
        }

    def test_section_block_to_json(self):
        content = TextBlock(text='hello')
        accessory = ImageLinkBlock(url='http://localhost/image.png')
        block = SectionBlock(
            content=content,
            accessory=accessory,
        )
        expected_json = ('{"type": "section", "content": {"type": "text", "text": "hello", "markdown": false},'
                         ' "accessory": {"type": "image_link", "url": "http://localhost/image.png"}}')
        assert block.to_json() == expected_json


class TestContextBlock:
    def test_context_block_properties(self):
        content = TextBlock(text='hello')
        image = ImageLinkBlock(url='http://localhost/image.png')
        block = ContextBlock(
            content=content,
            image=image,
        )
        assert block.block_type == BlockType.CONTEXT
        assert block.content == content
        assert block.image == image

    def test_context_block_validate(self):
        content = TextBlock(text='hello')
        image = ImageLinkBlock(url='http://localhost/image.png')
        assert ContextBlock(content=content, image=image).validate() is True

    def test_context_block_to_dict(self):
        content = TextBlock(text='hello')
        image = ImageLinkBlock(url='http://localhost/image.png')
        block = ContextBlock(
            content=content,
            image=image,
        )
        assert block.to_dict() == {
            'type': 'context',
            'content': content,
            'image': image,
        }

    def test_context_block_to_json(self):
        content = TextBlock(text='hello')
        image = ImageLinkBlock(url='http://localhost/image.png')
        block = ContextBlock(
            content=content,
            image=image,
        )
        expected_json = ('{"type": "context", "content": {"type": "text", "text": "hello", "markdown": false},'
                         ' "image": {"type": "image_link", "url": "http://localhost/image.png"}}')
        assert block.to_json() == expected_json


class TestLabelBlock:
    def test_label_block_properties(self):
        block = LabelBlock(text="hello", markdown=True)
        assert block.block_type == BlockType.LABEL
        assert block.text == 'hello'
        assert block.markdown is True

    def test_label_block_validate(self):
        assert LabelBlock(text="", markdown=False).validate() is False
        assert LabelBlock(text="a" * 201, markdown=False).validate() is False
        assert LabelBlock(text="hello", markdown=True).validate() is True

    def test_label_block_to_dict(self):
        block = LabelBlock(text="hello", markdown=True)
        assert block.to_dict() == {
            "type": "label",
            "text": "hello",
            "markdown": True,
        }

    def test_label_block_to_json(self):
        block = LabelBlock(text="hello", markdown=True)
        assert block.to_json() == '{"type": "label", "text": "hello", "markdown": true}'


class TestInputBlock:
    def test_input_block_properties(self):
        block = InputBlock(
            name="name",
            required=True,
        )
        assert block.block_type == BlockType.INPUT
        assert block.name == 'name'
        assert block.required is True
        assert block.placeholder is None

        block = InputBlock(name="name", required=True, placeholder="placeholder")
        assert block.block_type == BlockType.INPUT
        assert block.name == 'name'
        assert block.required is True
        assert block.placeholder == 'placeholder'

    def test_input_block_validate(self):
        assert InputBlock(name="", required=False).validate() is False
        assert InputBlock(name="name", required=False, placeholder='a' * 51).validate() is False
        assert InputBlock(name="name", required=True, placeholder='placeholder').validate() is True

    def test_input_block_to_dict(self):
        block = InputBlock(name="name", required=True, placeholder="placeholder")
        assert block.to_dict() == {
            "type": "input",
            "name": "name",
            "required": True,
            "placeholder": "placeholder",
        }

    def test_input_block_to_json(self):
        block = InputBlock(name="name", required=True, placeholder="placeholder")
        assert block.to_json() == '{"type": "input", "name": "name", "required": true, "placeholder": "placeholder"}'


class TestSelectBlock:
    def test_select_block_properties(self):
        options = [SelectBlockOption(text='text', value='text')]

        block = SelectBlock(
            name='name',
            options=options,
        )
        assert block.block_type == BlockType.SELECT
        assert block.options == options
        assert block.required is False
        assert block.placeholder is None

        block = SelectBlock(name='name', options=options, required=True, placeholder="placeholder")
        assert block.block_type == BlockType.SELECT
        assert block.options == options
        assert block.required is True
        assert block.placeholder == 'placeholder'

    def test_select_block_validate(self):
        options = [SelectBlockOption(text='text', value='text')]
        assert SelectBlock(name="", options=options).validate() is False
        assert SelectBlock(name="name", options=[]).validate() is False
        assert SelectBlock(name="name", options=options, placeholder="a" * 51).validate() is False
        assert SelectBlock(
            name="name",
            options=options,
            placeholder="placeholder",
            required=True,
        ).validate() is True

    def test_select_block_to_dict(self):
        options = [SelectBlockOption(text='text', value='text')]
        block = SelectBlock(name='name', options=options, required=True, placeholder="placeholder")
        assert block.to_dict() == {
            "type": "select",
            "name": "name",
            "options": options,
            "required": True,
            "placeholder": "placeholder",
        }

    def test_select_block_to_json(self):
        options = [SelectBlockOption(text='text', value='text')]
        block = SelectBlock(name='name', options=options, required=True, placeholder="placeholder")
        assert block.to_json() == '{"type": "select", "name": "name", "options": [["text", "text"]], "required": true, "placeholder": "placeholder"}'


class TestBlockKitBuilder:
    def test_blockkit_builder_message_properties(self):
        builder = BlockKitBuilder(kit_type=BlockKitType.MESSAGE)
        assert builder.kit_type == BlockKitType.MESSAGE
        assert builder.kit_vars == {'blocks': []}

        divider = DividerBlock()
        builder.text = 'hello'
        builder.blocks = [divider]
        assert builder.kit_vars == {
            'text': 'hello',
            'blocks': [divider],
        }
        assert builder.text == 'hello'
        assert builder.blocks == [divider]

        with pytest.raises(InvalidBlockType):
            builder.title = 'title'
        assert 'title' not in builder.kit_vars

        with pytest.raises(InvalidBlockType):
            builder.accept = 'ok'
        assert 'accept' not in builder.kit_vars

        with pytest.raises(InvalidBlockType):
            builder.decline = 'cancel'
        assert 'decline' not in builder.kit_vars

        with pytest.raises(InvalidBlockType):
            builder.value = 'value'
        assert 'value' not in builder.kit_vars

    def test_blockkit_builder_modal_properties(self):
        builder = BlockKitBuilder(kit_type=BlockKitType.MODAL)
        assert builder.kit_type == BlockKitType.MODAL
        assert builder.kit_vars == {'blocks': []}

        divider = DividerBlock()
        builder.title = 'title'
        builder.accept = 'ok'
        builder.decline = 'cancel'
        builder.value = 'value'
        builder.blocks = [divider]
        assert builder.kit_vars == {
            'title': 'title',
            'accept': 'ok',
            'decline': 'cancel',
            'value': 'value',
            'blocks': [divider],
        }
        assert builder.title == 'title'
        assert builder.accept == 'ok'
        assert builder.decline == 'cancel'
        assert builder.value == 'value'
        assert builder.blocks == [divider]

        with pytest.raises(InvalidBlockType):
            builder.text = 'hello'
        assert 'text' not in builder.kit_vars

    def test_blockkit_builder_add_block(self):
        divider = DividerBlock()

        builder = BlockKitBuilder(kit_type=BlockKitType.MESSAGE)
        builder.add_block(divider)
        assert builder.blocks == [divider]

        builder = BlockKitBuilder(kit_type=BlockKitType.MODAL)
        builder.add_block(divider)
        assert builder.blocks == [divider]
