from __future__ import annotations

import os
from typing import AsyncGenerator

import bson
import pytest

from sqlitestorage.storage import SQLiteStorage


@pytest.fixture()
async def storage() -> AsyncGenerator[SQLiteStorage, None]:
    db_filename = str(bson.ObjectId()) + ".db"
    database = SQLiteStorage(db_path=db_filename)
    try:
        yield database
    finally:
        await database.close()
        await database.wait_closed()
        os.remove(db_filename)
