# kakaowork-py

(Unofficial) Kakaowork Python client

[![CI](https://github.com/skyoo2003/kakaowork-py/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/skyoo2003/kakaowork-py/actions/workflows/ci.yml) [![codecov](https://codecov.io/gh/skyoo2003/kakaowork-py/branch/master/graph/badge.svg?token=J6NQHDJEMZ)](https://codecov.io/gh/skyoo2003/kakaowork-py)

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

## Usage

```python
from kakaowork import Kakaowork

client = Kakaowork(app_key="your_app_key")
r = client.users.list(limit=10) # get a response of users using limit
while r.cursor: # loop until it does not to exist
  print(r.users)
  r = client.users.list(cursor=r.cursor) # get a response of users using cursor
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## [License](LICENSE)

Copyright (c) 2021 Sung-Kyu Yoo.

This project is MIT license.
