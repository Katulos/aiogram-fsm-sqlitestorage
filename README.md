# Yet Another FSM SQLite Storage

![PyPI - Wheel](https://img.shields.io/pypi/wheel/aiogram-fsm-sqlitestorage?logo=pypi)
![PyPI - Version](https://img.shields.io/pypi/v/aiogram-fsm-sqlitestorage?logo=pypi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiogram-fsm-sqlitestorage?logo=pypi)
![PyPI - License](https://img.shields.io/pypi/l/aiogram-fsm-sqlitestorage?logo=pypi)
![release](https://github.com/Katulos/aiogram-fsm-sqlitestorage/actions/workflows/release.yml/badge.svg)
![develop](https://github.com/Katulos/aiogram-fsm-sqlitestorage/actions/workflows/develop.yml/badge.svg?branch=develop)

> [!NOTE]
> When it was necessary for my project, I did not find such projects as [osf4/sqlitestorage](https://github.com/osf4/sqlitestorage) or [sashaferrum/aiogram_sqlite_storage](https://github.com/sashaferrum/aiogram_sqlite_storage) :sob: and adapted [this fork](https://github.com/LehaSex/SQLiteStorage) to my needs.
> More forks to the God of forks! :laughing:

Simple aiogram FSM storage, stores all FSM data in SQLite database

Intended to replace `MemoryStorage` for simple cases where you want to keep states between bot restarts.

Implements just [basic BaseStorage methods](https://docs.aiogram.dev/en/dev-3.x/dispatcher/finite_state_machine/storages.html#aiogram.fsm.storage.base.BaseStorage) such as:

- set_state()
- get_state()
- set_data()
- get_data()
- close()

Tests are based on [original aiogram tests v3.13.1](https://github.com/aiogram/aiogram/blob/v3.13.1/tests/test_contrib/test_fsm_storage/test_storage.py).

## Installation

```bash
pip install aiogram-fsm-sqlitestorage
```

## Usage

Include the following in your script:

```python
# import aiogram and the rest
from aiogram_fsm_sqlitestorage import SQLiteStorage

dp = Dispatcher(bot, storage=SQLiteStorage())
```

Using `SQLiteStorage()` instead of `MemoryStorage()` makes your FSM data persistent between bot restarts.
