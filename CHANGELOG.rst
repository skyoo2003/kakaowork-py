Kakaowork 0.5.0 (2021-11-05)
============================

New Features
------------

- Added Kakaowork API: messages.send_by_email (`#130 <https://github.com/skyoo2003/kakaowork-py/issues/130>`_)


Enhancement
-----------

- Support for TextBlock API format changed from KakaoWork 1.7 or higher (`#131 <https://github.com/skyoo2003/kakaowork-py/issues/131>`_)


Kakaowork 0.4.1 (2021-10-13)
============================

Miscellaneous
-------------

- Python 3.10 support (`#127 <https://github.com/skyoo2003/kakaowork-py/issues/127>`_)


Kakaowork 0.4.0 (2021-08-04)
============================

New Features
------------

- Support Reactive Web API (`#89 <https://github.com/skyoo2003/kakaowork-py/issues/89>`_)


Enhancement
-----------

- Client-side rate limiting according to official documentation. (`#94 <https://github.com/skyoo2003/kakaowork-py/issues/94>`_)


Miscellaneous
-------------

- Changed aiosonic dependency (`#85 <https://github.com/skyoo2003/kakaowork-py/issues/85>`_)

  - aiosonic>=0.10,<0.14


Kakaowork 0.3.3 (2021-06-29)
============================

Bug Fixes
---------

- Fixed an exception occurs when missing fields from the models (`#82 <https://github.com/skyoo2003/kakaowork-py/issues/82>`_)


Kakaowork 0.3.2 (2021-06-28)
============================

Bug Fixes
---------

- Fixed import error


Kakaowork 0.3.1 (2021-06-20)
============================

New Features
------------

- Added BlockKitBuilder API to load from JSON file (`#37 <https://github.com/skyoo2003/kakaowork-py/issues/37>`_)


Documentation
-------------

- Added docstrings for APIs documentation (`#32 <https://github.com/skyoo2003/kakaowork-py/issues/32>`_)


Kakaowork 0.3.0 (2021-05-21)
============================

New Features
------------

- Added AsyncKakaowork for asyncio support (`#42 <https://github.com/skyoo2003/kakaowork-py/issues/42>`_)


Enhancement
-----------

- Changed limit option to IntRange type (`#47 <https://github.com/skyoo2003/kakaowork-py/issues/47>`_)
- Updated API specific error codes and unknown. (`#57 <https://github.com/skyoo2003/kakaowork-py/issues/57>`_)
- Fields' to_dict method is returned as a dict, not an OrderedDict. Also, it's a timestamp, not a datetime. (`#58 <https://github.com/skyoo2003/kakaowork-py/pull/58>`_)


Documentation
-------------

- Added CLI documentation to help to use it (`#33 <https://github.com/skyoo2003/kakaowork-py/issues/33>`_)


Miscellaneous
-------------

- Changed dependencies (`#60 <https://github.com/skyoo2003/kakaowork-py/issues/60>`_)

  - pytz>=2015.7
  - click^7.0.0


Kakaowork 0.2.1 (2021-05-03)
============================

Enhancement
-----------

- Change urllib3 minimum required version (`#39 <https://github.com/skyoo2003/kakaowork-py/issues/39>`_)
- Update the project classifiers

Kakaowork 0.2.0 (2021-04-30)
============================

Breaking Changes
----------------

- Replace block_type with type in Blocks and kit_type with type BlockKitBuilder (`#31 <https://github.com/skyoo2003/kakaowork-py/issues/31>`_)


New Features
------------

- Add blocks option in messages send command (`#31 <https://github.com/skyoo2003/kakaowork-py/issues/31>`_)


Enhancement
-----------

- Support command aliases (`#34 <https://github.com/skyoo2003/kakaowork-py/issues/34>`_)


Kakaowork 0.1.3 (2021-04-26)
============================

Enhancement
-----------

- Update imports in __init__.py (`#29 <https://github.com/skyoo2003/kakaowork-py/issues/29>`_)


Bug Fixes
---------

- Fix client/model and update tests (`#27 <https://github.com/skyoo2003/kakaowork-py/issues/27>`_)
- Fixed timezone crash issue (`#28 <https://github.com/skyoo2003/kakaowork-py/issues/28>`_)


Documentation
-------------

- Project documentation via Sphinx (`#24 <https://github.com/skyoo2003/kakaowork-py/issues/24>`_)


Kakaowork 0.1.2 (2021-04-21)
============================

New Features
------------

- Add Kakaowork CLI (`#7 <https://github.com/skyoo2003/kakaowork-py/issues/7>`_)


Enhancement
-----------

- Update init imports (`#9 <https://github.com/skyoo2003/kakaowork-py/issues/9>`_)
- Add unit tests and improve code quality (`#12 <https://github.com/skyoo2003/kakaowork-py/issues/12>`_)
- Returns an error if CLI is not supported (`#19 <https://github.com/skyoo2003/kakaowork-py/issues/19>`_)


Documentation
-------------

- Update README (`#8 <https://github.com/skyoo2003/kakaowork-py/issues/8>`_)


Kakaowork 0.1.1 (2021-04-07)
============================

New Features
------------

- Implement Kakaowork BlockKits
- Implement Kakaowork Client API (`#2 <https://github.com/skyoo2003/kakaowork-py/issues/2>`_)
