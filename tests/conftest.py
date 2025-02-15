import os
import uuid
from typing import AsyncGenerator

import pytest
from aiogram.fsm.storage.base import StorageKey

from aiogram_fsm_sqlitestorage import SQLiteStorage
from tests.mocked_bot import MockedBot

CHAT_ID = -42
USER_ID = 42


@pytest.fixture()  # type: ignore
def bot():
    return MockedBot()


@pytest.fixture(name="storage_key")  # type: ignore
def create_storage_key(bot: MockedBot):
    return StorageKey(chat_id=CHAT_ID, user_id=USER_ID, bot_id=bot.id)


@pytest.fixture()  # type: ignore
async def sqlite_storage() -> AsyncGenerator[SQLiteStorage, None]:
    db_filename = str(uuid.uuid4()) + ".db"
    storage = SQLiteStorage(db_path=db_filename)
    try:
        yield storage
    finally:
        await storage.close()
        os.remove(db_filename)
