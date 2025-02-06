import typing

from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType


class SQLiteStorage(BaseStorage):
    """Simple SQLite based storage for Finite State Machine.

    Intended to replace MemoryStorage for simple cases where you want to keep states
    between bot restarts.
    """

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        pass

    async def get_state(self, key: StorageKey) -> typing.Optional[str]:
        pass

    async def set_data(self, key: StorageKey, data: typing.Dict[str, typing.Any]) -> None:
        pass

    async def get_data(self, key: StorageKey) -> typing.Dict[str, typing.Any]:
        pass

    async def close(self) -> None:
        pass
