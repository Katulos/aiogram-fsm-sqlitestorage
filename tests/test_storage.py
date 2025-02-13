from aiogram.fsm.storage.base import BaseStorage, StorageKey


async def test_set_get(
    storage: BaseStorage,
    storage_key: StorageKey,
) -> None:
    assert await storage.get_data(storage_key) == {}
    await storage.set_data(storage_key, data={"foo": "bar"})
    assert await storage.get_data(storage_key) == {"foo": "bar"}


async def test_reset(
    storage: BaseStorage,
    storage_key: StorageKey,
) -> None:
    await storage.set_data(storage_key, data={"foo": "bar"})
    await storage.set_state(storage_key, state="SECOND")

    await storage.set_data(storage_key, data={})
    assert await storage.get_state(storage_key) == "SECOND"


async def test_reset_empty(
    storage: BaseStorage,
    storage_key: StorageKey,
) -> None:
    await storage.set_data(storage_key, data={})
    assert await storage.get_data(storage_key) == {}
