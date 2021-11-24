from kakaowork import Kakaowork

if __name__ == '__main__':
    client = Kakaowork(app_key='<your_app_key>')
    ret = client.conversations.list(limit=10)
    print(ret.plain())
    while ret.cursor:
        ret = client.conversations.list(cursor=ret.cursor)
        print(ret.plain())
