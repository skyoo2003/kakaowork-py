# kakaowork-py

(Unofficial) Kakaowork Python client

[![CI](https://github.com/skyoo2003/kakaowork-py/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/skyoo2003/kakaowork-py/actions/workflows/ci.yml) [![Documentation Status](https://readthedocs.org/projects/kakaowork-py/badge/?version=stable)](https://kakaowork-py.readthedocs.io/en/stable)
 [![codecov](https://codecov.io/gh/skyoo2003/kakaowork-py/branch/master/graph/badge.svg?token=J6NQHDJEMZ)](https://codecov.io/gh/skyoo2003/kakaowork-py)

__Table of Contents__

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
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

## Usage

```python
from kakaowork import Kakaowork

client = Kakaowork(app_key="your_app_key")
r = client.users.list(limit=10) # get a response of users using limit
print(r.users)
while r.cursor: # loop until it does not to exist
  print(r.users)
  r = client.users.list(cursor=r.cursor) # get a response of users using cursor
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
