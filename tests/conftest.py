import os
from typing import AsyncGenerator

import bson
import pytest
from aiogram.fsm.storage.base import StorageKey

from sqlitestorage.storage import SQLiteStorage


@pytest.fixture()  # type: ignore
async def storage() -> AsyncGenerator[SQLiteStorage, None]:
    db_filename = str(bson.ObjectId()) + ".db"
    database = SQLiteStorage(db_path=db_filename)
    try:
        yield database
    finally:
        await database.close()
        # await database.wait_closed() # raise PermissionError
        os.remove(db_filename)


@pytest.fixture()  # type: ignore
async def storage_key() -> StorageKey:
    return StorageKey(bot_id=123456789, chat_id=123, user_id=456)
