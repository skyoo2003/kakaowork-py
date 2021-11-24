import asyncio
import tempfile

from kakaowork import (
    AsyncKakaowork as Kakaowork,
    BlockKitType,
    BlockKitBuilder,
    HeaderBlock,
    HeaderStyle,
    TextBlock,
    TextInline,
    TextInlineColor,
    TextInlineType,
    DividerBlock,
    ButtonBlock,
    ButtonActionType,
    ButtonStyle,
)

blockkit_json = """
{
    "type": "message",
    "blocks": [
        {"type": "header", "text": "TITLE", "style": "blue"},
        {"type": "text", "text": "BODY"},
        {"type": "divider"},
        {"type": "button", "text": "BUTTON", "style": "default"}
    ]
}
"""


async def main():
    client = Kakaowork(app_key='b829f770.41fc2a26ba1a466fa4fe81dbd612b2e5')

    # CASE1: Using the BlockKitBuilder.add_block
    builder = BlockKitBuilder(type=BlockKitType.MESSAGE)
    builder.add_block(HeaderBlock(text='TITLE', style=HeaderStyle.YELLOW))
    builder.add_block(
        TextBlock(
            text='BODY',
            inlines=[
                TextInline(type=TextInlineType.STYLED, text='INLINE', bold=True, italic=True, strike=True, color=TextInlineColor.RED),
            ],
        ))
    builder.add_block(DividerBlock())
    builder.add_block(ButtonBlock(
        text='BUTTON',
        style=ButtonStyle.PRIMARY,
        action_type=ButtonActionType.OPEN_SYSTEM_BROWSER,
        value='https://daum.net',
    ))
    ret = await client.messages.send(conversation_id=1093137, text='Hello, World!', blocks=builder.blocks)
    print(ret.plain())

    # CASE2: Using the BlockKitBuilder.load
    with tempfile.NamedTemporaryFile('w+') as f:
        f.write(blockkit_json)
        f.seek(0)
        builder = BlockKitBuilder.load(f.name)  # NOTE: Recommend to use asyncio supported io library (https://github.com/Tinche/aiofiles)
    ret = await client.messages.send(conversation_id=1093137, text='Hello, World!', blocks=builder.blocks)
    print(ret.plain())

    # CASE3: Using Block instances directly
    blocks = [
        HeaderBlock(text='TITLE', style=HeaderStyle.RED),
        TextBlock(text='BODY'),
        DividerBlock(),
        ButtonBlock(
            text='BUTTON',
            style=ButtonStyle.DANGER,
            action_type=ButtonActionType.OPEN_SYSTEM_BROWSER,
            value='https://daum.net',
        ),
    ]
    ret = await client.messages.send(conversation_id=1093137, text='Hello, World!', blocks=blocks)
    print(ret.plain())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())