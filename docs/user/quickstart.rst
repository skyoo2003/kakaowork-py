Quickstart
==========

For Python
----------

.. code-block:: python3

    from kakaowork import Kakaowork


    def main():
      client = Kakaowork(app_key="your_app_key")
      r = client.users.list(limit=10)  # get a response of users using limit
      print(r.users)
      while r.cursor:  # loop until it does not to exist
        print(r.users)
        r = client.users.list(cursor=r.cursor)  # get a response of users using cursor

    if __name__ == '__main__':
      main()

.. code-block:: python3

    import asyncio

    from kakaowork import AsyncKakaowork


    async def main():
        client = AsyncKakaowork(app_key="your_app_key")
        r = await client.users.list(limit=10)  # get a response of users using limit
        print(r.users)
        while r.cursor:  # loop until it does not to exist
            print(r.users)
            r = await client.users.list(cursor=r.cursor)  # get a response of users using cursor

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

For Command Line
----------------

If you have installed it with the extras 'cli', you can use the command line below in your shell.

.. code-block:: text

    Usage: kakaowork [OPTIONS] COMMAND [ARGS]...

    Options:
      -k, --app-key TEXT
      --help              Show this message and exit.

    Commands:
      bots
      conversations
      departments
      messages
      spaces
      users

An example below.

.. code-block:: sh

    $ kakaowork -k <your_app_key> bots info
    ID:     1
    Name:   Test
    Status: activated
