# kakaowork-py

(Unofficial) Kakaowork Python client

[![PyPI](https://img.shields.io/pypi/v/kakaowork)](https://pypi.org/project/kakaowork)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kakaowork)](https://pypi.org/project/kakaowork)
[![Downloads](https://pepy.tech/badge/kakaowork)](https://pepy.tech/project/kakaowork)
[![GitHub](https://img.shields.io/github/license/skyoo2003/kakaowork-py)](LICENSE)
[![Documentation Status](https://readthedocs.org/projects/kakaowork-py/badge/?version=latest)](https://kakaowork-py.readthedocs.io/en/latest)
[![CI](https://github.com/skyoo2003/kakaowork-py/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/skyoo2003/kakaowork-py/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/skyoo2003/kakaowork-py/branch/master/graph/badge.svg?token=J6NQHDJEMZ)](https://codecov.io/gh/skyoo2003/kakaowork-py)

__Table of Contents__

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usages](#usages)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- Python >= 3.6.1

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install kakaowork-py

```bash
pip install kakaowork
```

If you want to use CLI, install with the extras 'cli'

```bash
pip install kakaowork[cli]
```

## Usages

```python
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
```

```python
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
```

If you have installed it with the extras 'cli', you can use the command line below in your shell.

```sh
$ kakaowork --help
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

$ kakaowork -k <your_app_key> bots info
ID:     1
Name:   Test
Status: activated
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## [License](LICENSE)

Copyright (c) 2021 Sung-Kyu Yoo.

This project is MIT license.
