import asyncio

from kakaowork import AsyncKakaowork as Kakaowork


async def main():
    client = Kakaowork(app_key='<your_app_key>')
    ret = await client.conversations.list(limit=10)
    print(ret.plain())
    while ret.cursor:
        ret = await client.conversations.list(cursor=ret.cursor)
        print(ret.plain())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
