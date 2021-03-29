from kakaowork.blockkit import (
    BlockType,
    ButtonStyle,
    ButtonActionType,
    HeaderStyle,
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
)


def test_text_block_properties():
    text = '"hello"'
    block = TextBlock(text=text, markdown=False)
    assert block.block_type == BlockType.TEXT
    assert block.text == text
    assert block.markdown is False


def test_text_block_validate():
    assert TextBlock(text="", markdown=False).validate() is False
    assert TextBlock(text="a" * 501, markdown=False).validate() is False
    assert TextBlock(text="hello", markdown=False).validate() is True


def test_text_block_to_dict():
    block = TextBlock(text="hello", markdown=False)
    assert block.to_dict() == {
        'type': 'text',
        'text': 'hello',
        'markdown': False,
    }


def test_text_block_to_json():
    block = TextBlock(text="hello", markdown=False)
    assert block.to_json() == '{"type": "text", "text": "hello", "markdown": false}'


def test_image_link_block_properties():
    url = "http://localhost/image.png"
    block = ImageLinkBlock(url=url)
    assert block.block_type == BlockType.IMAGE_LINK
    assert block.url == url


def test_image_link_block_validate():
    assert ImageLinkBlock(url="").validate() is False
    assert ImageLinkBlock(url="$*(#Y$(").validate() is False
    assert ImageLinkBlock(url="http://localhost").validate() is False
    assert ImageLinkBlock(url="http://localhost/").validate() is False
    assert ImageLinkBlock(url="http://localhost/image.png").validate() is True


def test_image_link_block_to_dict():
    url = "http://localhost/image.png"
    block = ImageLinkBlock(url=url)
    assert block.to_dict() == {
        "type": "image_link",
        "url": "http://localhost/image.png",
    }


def test_image_link_block_to_json():
    url = "http://localhost/image.png"
    block = ImageLinkBlock(url=url)
    assert block.to_json() == '{"type": "image_link", "url": "http://localhost/image.png"}'


def test_button_block_properties():
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


def test_button_block_validate():
    assert ButtonBlock(text="", style=ButtonStyle.DEFAULT).validate() is False
    assert ButtonBlock(text="a" * 21, style=ButtonStyle.PRIMARY).validate() is False
    assert ButtonBlock(text="hello", style=ButtonStyle.PRIMARY).validate() is True


def test_button_block_to_dict():
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


def test_button_block_to_json():
    block = ButtonBlock(
        text='hello',
        style=ButtonStyle.PRIMARY,
        action_type=ButtonActionType.OPEN_INAPP_BROWSER,
        action_name='action',
        value='value',
    )
    expected_json = '{"type": "button", "text": "hello", "style": "primary", "action_type": "open_inapp_browser", "action_name": "action", "value": "value"}'
    assert block.to_json() == expected_json


def test_divider_block_properties():
    block = DividerBlock()
    assert block.block_type == BlockType.DIVIDER


def test_divider_block_validate():
    assert DividerBlock().validate() is True


def test_divider_block_to_dict():
    block = DividerBlock()
    assert block.to_dict() == {"type": "divider"}


def test_divider_block_to_json():
    block = DividerBlock()
    assert block.to_json() == '{"type": "divider"}'


def test_header_block_properties():
    block = HeaderBlock(text="hello", style=HeaderStyle.YELLOW)
    assert block.block_type == BlockType.HEADER
    assert block.text == 'hello'
    assert block.style == HeaderStyle.YELLOW


def test_header_block_validate():
    assert HeaderBlock(text="", style=HeaderStyle.BLUE).validate() is False
    assert HeaderBlock(text="a" * 21, style=HeaderStyle.YELLOW).validate() is False
    assert HeaderBlock(text="hello", style=HeaderStyle.RED).validate() is True


def test_header_block_to_dict():
    block = HeaderBlock(text="hello", style=HeaderStyle.YELLOW)
    assert block.to_dict() == {
        "type": "header",
        "text": "hello",
        "style": "yellow",
    }


def test_header_block_to_json():
    block = HeaderBlock(text="hello", style=HeaderStyle.YELLOW)
    assert block.to_json() == '{"type": "header", "text": "hello", "style": "yellow"}'


def test_action_block_properties():
    button = ButtonBlock(text="hello", style=ButtonStyle.DEFAULT)
    block = ActionBlock(
        elements=[button],
    )
    assert block.block_type == BlockType.ACTION
    assert block.elements == [button]


def test_action_block_validate():
    button = ButtonBlock(text="hello", style=ButtonStyle.DEFAULT)
    assert ActionBlock(elements=[]).validate() is False
    assert ActionBlock(elements=[button]).validate() is True


def test_action_block_to_dict():
    button = ButtonBlock(text="hello", style=ButtonStyle.DEFAULT)
    block = ActionBlock(
        elements=[button],
    )
    assert block.to_dict() == {
        "type": "action",
        "elements": [button],
    }


def test_action_block_to_json():
    button = ButtonBlock(text="hello", style=ButtonStyle.DEFAULT)
    block = ActionBlock(
        elements=[button],
    )
    assert block.to_json() == '{"type": "action", "elements": [{"type": "button", "text": "hello", "style": "default"}]}'


def test_description_block_properties():
    content = TextBlock(text='content')
    block = DescriptionBlock(term='hello', content=content, accent=True)
    assert block.block_type == BlockType.DESCRIPTION
    assert block.term == 'hello'
    assert block.content == content
    assert block.accent is True


def test_description_block_validate():
    content = TextBlock(text='content')
    assert DescriptionBlock(term="", content=content, accent=False).validate() is False
    assert DescriptionBlock(term="a" * 11, content=content, accent=False).validate() is False
    assert DescriptionBlock(term="hello", content=content, accent=False).validate() is True


def test_description_block_to_dict():
    content = TextBlock(text='content')
    block = DescriptionBlock(term='hello', content=content, accent=True)
    assert block.to_dict() == {
        "type": "description",
        "term": "hello",
        "content": content,
        "accent": True,
    }


def test_description_block_to_json():
    content = TextBlock(text='content')
    block = DescriptionBlock(term='hello', content=content, accent=True)
    expected_json = '{"type": "description", "term": "hello", "content": {"type": "text", "text": "content", "markdown": false}, "accent": true}'
    assert block.to_json() == expected_json


def test_section_block_properties():
    content = TextBlock(text='hello')
    accessory = ImageLinkBlock(url='http://localhost/image.png')
    block = SectionBlock(
        content=content,
        accessory=accessory,
    )
    assert block.block_type == BlockType.SECTION
    assert block.content == content
    assert block.accessory == accessory


def test_section_block_validate():
    content = TextBlock(text='hello')
    accessory = ImageLinkBlock(url='http://localhost/image.png')
    assert SectionBlock(content=content, accessory=accessory).validate() is True


def test_section_block_to_dict():
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


def test_section_block_to_json():
    content = TextBlock(text='hello')
    accessory = ImageLinkBlock(url='http://localhost/image.png')
    block = SectionBlock(
        content=content,
        accessory=accessory,
    )
    expected_json = (
        '{"type": "section", "content": {"type": "text", "text": "hello", "markdown": false},'
        ' "accessory": {"type": "image_link", "url": "http://localhost/image.png"}}'
    )
    assert block.to_json() == expected_json


def test_context_block_properties():
    content = TextBlock(text='hello')
    image = ImageLinkBlock(url='http://localhost/image.png')
    block = ContextBlock(
        content=content,
        image=image,
    )
    assert block.block_type == BlockType.CONTEXT
    assert block.content == content
    assert block.image == image


def test_context_block_validate():
    content = TextBlock(text='hello')
    image = ImageLinkBlock(url='http://localhost/image.png')
    assert ContextBlock(content=content, image=image).validate() is True


def test_context_block_to_dict():
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


def test_context_block_to_json():
    content = TextBlock(text='hello')
    image = ImageLinkBlock(url='http://localhost/image.png')
    block = ContextBlock(
        content=content,
        image=image,
    )
    expected_json = (
        '{"type": "context", "content": {"type": "text", "text": "hello", "markdown": false},'
        ' "image": {"type": "image_link", "url": "http://localhost/image.png"}}'
    )
    assert block.to_json() == expected_json


def test_label_block_properties():
    block = LabelBlock(text="hello", markdown=True)
    assert block.block_type == BlockType.LABEL
    assert block.text == 'hello'
    assert block.markdown is True


def test_label_block_validate():
    pass
