from __future__ import annotations

import json
import sqlite3
import typing
from typing import Any

from aiogram.fsm.storage.base import BaseStorage, StorageKey


class SQLiteStorage(BaseStorage):
    """Simple SQLite based storage for Finite State Machine.

    Intended to replace MemoryStorage for simple cases where you want to keep states
    between bot restarts.
    """

    async def update_data(
        self,
        *,
        key: StorageKey,
        data: dict[Any, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        existing_data = await self.get_data(key=key)
        if data:
            existing_data.update(data)
        existing_data.update(**kwargs)

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO fsm_data (key, state, data)
            VALUES (?, COALESCE((SELECT state FROM fsm_data WHERE key = ?), '{}'), ?)
        """,
            (
                str(key.chat_id) + ":" + str(key.user_id),
                str(key.chat_id) + ":" + str(key.user_id),
                json.dumps(existing_data),
            ),
        )
        conn.commit()

    async def update_bucket(
        self,
        *,
        key: StorageKey,
        bucket: dict | None = None,
        **kwargs,
    ):
        pass

    async def set_bucket(
        self,
        *,
        key: StorageKey,
        bucket: dict | None = None,
    ) -> None:
        pass

    async def get_bucket(
        self,
        *,
        key: StorageKey,
        default: dict | None | None = None,
    ) -> dict | None:
        pass

    def __init__(self, db_path: str = "fsm_storage.db"):
        self.db_path = db_path
        self._conn = None
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS fsm_data (
                key TEXT PRIMARY KEY,
                state TEXT,
                data TEXT
            )
        """,
        )
        conn.commit()
        conn.close()

    def _get_connection(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
        return self._conn

    async def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    async def wait_closed(self) -> None:
        pass

    async def set_state(
        self,
        *,
        key: StorageKey,
        state: typing.AnyStr | None = None,
        **kwargs,
    ):
        conn = self._get_connection()
        cursor = conn.cursor()
        # print('Set state')
        # print(f'chat: {chat}')
        # print(f'user: {user}')
        # print(f'state: {self.resolve_state(state)}')
        cursor.execute(
            """
            INSERT OR REPLACE INTO fsm_data
            (key, state, data)
            VALUES (?, ?, COALESCE((SELECT data FROM fsm_data WHERE key = ?), '{}'))
        """,
            (
                str(key.chat_id) + ":" + str(key.user_id),
                self.resolve_state(state),
                str(key.chat_id) + ":" + str(key.user_id),
            ),
        )
        conn.commit()

    async def get_state(
        self,
        *,
        key: StorageKey,
        default: str | None = None,
    ) -> typing.Coroutine[Any, Any, str | None]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT state FROM fsm_data WHERE key = ?",
            (str(key.chat_id) + ":" + str(key.user_id),),
        )
        result = cursor.fetchone()
        # print('Get state')
        # print(f'chat: {chat}')
        # print(f'user: {user}')
        # print(f'raw state: {result[0]}')
        # print(f'resolved state: {self.resolve_state(result[0])}')
        if result:
            pass
        else:
            pass
        if result and len(result[0]) > 0:
            state = result[0]
        else:
            state = None
        # print(f'result: {what}')
        # print(f'state: {state}')
        return state

    async def set_data(
        self,
        *,
        key: StorageKey,
        data: dict | None = None,
    ):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO fsm_data (key, state, data)
            VALUES (?, COALESCE((SELECT state FROM fsm_data WHERE key = ?), ''), ?)
        """,
            (
                str(key.chat_id) + ":" + str(key.user_id),
                str(key.chat_id) + ":" + str(key.user_id),
                json.dumps(data),
            ),
        )
        conn.commit()

    async def get_data(
        self,
        *,
        key: StorageKey,
        default: dict | None = None,
    ) -> dict:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT data FROM fsm_data WHERE key = ?",
            (str(key.chat_id) + ":" + str(key.user_id),),
        )
        result = cursor.fetchone()
        return json.loads(result[0]) if result else {}

    async def reset_data(
        self,
        *,
        key: StorageKey,
    ):
        await self.set_data(key=key, data={})

    async def reset_state(
        self,
        *,
        key: StorageKey,
        with_data: bool | None = True,
    ):
        #        await self.set_state(chat=chat, user=user, state=None)
        #        if with_data:
        #            await self.set_data(chat=chat, user=user, data={})
        self._cleanup(key)

    def _cleanup(self, key):
        #        chat, user = self.resolve_address(chat=chat, user=user)
        #        if self.get_state(chat=chat, user=user) == None:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM fsm_data WHERE key = ?",
            (str(key.chat_id) + ":" + str(key.user_id),),
        )
        conn.commit()

    @staticmethod
    def resolve_state(value):
        from aiogram.filters.state import State

        if value is None:
            return

        if isinstance(value, str):
            return value

        if isinstance(value, State):
            return value.state

        return str(value)
