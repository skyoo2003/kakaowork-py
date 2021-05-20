Kakaowork 0.3.0 (2021-05-21)Kakaowork 0.3.0 (2021-05-21)
============================



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
