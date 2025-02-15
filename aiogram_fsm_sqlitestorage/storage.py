import json
import logging
import sqlite3
from typing import Any, Dict, Optional, Tuple, Union

from aiogram.fsm.state import State
from aiogram.fsm.storage.base import (
    BaseStorage,
    DefaultKeyBuilder,
    KeyBuilder,
    StateType,
    StorageKey,
)

logging.basicConfig(level=logging.INFO)


class SQLiteStorage(BaseStorage):
    """Simple SQLite based storage for Finite State Machine.

    Intended to replace MemoryStorage for simple cases where you want to keep states
    between bot restarts.
    """

    def __init__(
        self,
        db_path: str = "fsm_storage.db",
        key_builder: Optional[KeyBuilder] = None,
    ):
        if key_builder is None:
            key_builder = DefaultKeyBuilder(with_destiny=True)
        self.db_path: str = db_path
        self._conn: Optional[sqlite3.Connection] = None
        self._key_builder = key_builder
        self._init_db()

    def _init_db(self) -> None:
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

    def _get_connection(self) -> Optional[Union[sqlite3.Connection, None]]:
        if self._conn is None:
            try:
                self._conn = sqlite3.connect(self.db_path)
            except sqlite3.Error as e:
                logging.error(e)
                return None
        return self._conn

    async def set_state(
        self,
        key: StorageKey,
        state: StateType = None,
    ) -> None:
        conn = self._get_connection()
        if conn is None:
            raise RuntimeError(
                "The connection to the database was not established.",
            )
        key_str = self._key_builder.build(key)
        resolved_state = self.resolve_state(
            state,
        )

        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO fsm_data
                    (key, state, data)
                    VALUES (?, ?, COALESCE((SELECT data FROM fsm_data WHERE key = ?), '{}'))
                    """,
                    (key_str, resolved_state, key_str),
                )
        except sqlite3.Error as e:
            logging.error(e)
            raise RuntimeError(f"Error executing query: {e}") from e

    async def get_state(self, key: StorageKey) -> Optional[str]:
        conn = self._get_connection()
        if conn is None:
            raise RuntimeError(
                "The connection to the database was not established.",
            )

        key_str = self._key_builder.build(key)

        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT state FROM fsm_data WHERE key = ?",
                    (key_str,),
                )
                result: Optional[Tuple[Any, ...]] = cursor.fetchone()
                state: Optional[str] = (
                    result[0] if result and result[0] else None
                )
        except sqlite3.Error as e:
            logging.error(e)
            raise RuntimeError(f"Error executing query: {e}") from e

        return state

    async def set_data(
        self,
        key: StorageKey,
        data: Dict[str, Any],
    ) -> None:
        conn = self._get_connection()
        if conn is None:
            raise RuntimeError(
                "The connection to the database was not established.",
            )

        key_str = self._key_builder.build(key)
        data_json = json.dumps(data)

        try:
            with conn:
                cursor = conn.cursor()
                if not data:
                    cursor.execute(
                        "DELETE FROM fsm_data WHERE key = ?",
                        (key_str,),
                    )
                    return
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO fsm_data (key, state, data)
                    VALUES (?, COALESCE((SELECT state FROM fsm_data WHERE key = ?), ''), ?)
                    """,
                    (key_str, key_str, data_json),
                )
        except sqlite3.Error as e:
            logging.error(e)
            raise RuntimeError(f"Error executing query: {e}") from e

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        conn = self._get_connection()
        if conn is None:
            raise RuntimeError(
                "The connection to the database was not established.",
            )

        key_str = self._key_builder.build(key)

        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT data FROM fsm_data WHERE key = ?",
                    (key_str,),
                )
                result: Optional[Tuple[Any, ...]] = cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(e)
            raise RuntimeError(f"Error executing query: {e}") from e

        if result:
            data = json.loads(result[0])
            if isinstance(data, dict):
                return data
        return {}

    async def close(self) -> None:
        if self._conn is not None:
            try:
                self._conn.close()
            finally:
                self._conn = None

    async def wait_closed(self) -> bool:
        conn = self._get_connection()
        if conn is None:
            return True
        try:
            conn.execute("SELECT 1")
            return False
        except sqlite3.ProgrammingError as e:
            logging.error(e)
            return True

    @staticmethod
    def resolve_state(
        value: Optional[Union[str, State, None]],
    ) -> Optional[Union[str, State, None]]:
        if value is None:
            return None

        if isinstance(value, str):
            return value

        if isinstance(value, State):
            return value.state

        return str(value)
