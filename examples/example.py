import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardRemove,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from sqlitestorage.storage import SQLiteStorage

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

API_TOKEN = "YOUR_TOKEN_HERE"

router = Router()


class Phase(StatesGroup):
    START = State()
    SECOND = State()
    FIN = State()


@router.message(F.text.startswith("Get values"), Phase.SECOND)
async def get_value_phase_second(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    await message.answer(f"State is {current_state}")

    data = await state.get_data()
    text = "\n".join(f"{key}: {value}" for key, value in data.items())
    await message.answer(
        f"Values of data is:\n{text}",
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.set_state(Phase.FIN)


@router.message(Phase.FIN)
async def get_value_phase_fin(message: types.Message, state: FSMContext):
    await message.answer(f"State is {await state.get_state()}")
    if message.text == "/start":
        await state.set_state(Phase.START)
    else:
        await message.answer("Good bye!")


@router.message(Phase.SECOND)
async def save_value_phase_second(message: types.Message, state: FSMContext):
    await message.answer(f"State is {await state.get_state()}")
    if "=" not in message.text:
        await message.answer("Enter pair of args in format: <key>=<values>")
        return

    key, value = message.text.split("=")
    data = {key: value}
    await state.update_data(**data)

    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Get values"))
    builder.adjust(1)

    markup = builder.as_markup(one_time_keyboard=False, resize_keyboard=True)

    await message.answer(f"Saved! {key}: {value}.", reply_markup=markup)
    await state.set_state(Phase.SECOND)


@router.message()
async def save_value_phase_all(message: types.Message, state: FSMContext):
    await message.answer(f"State is {await state.get_state()}")
    if "=" not in message.text:
        await message.answer("Enter pair of args in format: <key>=<values>")
        await state.set_state(Phase.START)
        return

    key, value = message.text.split("=")
    data = {key: value}
    await state.update_data(data)

    text = (
        f"Saved! {key}: {value}.\nYou can add new pair of key-value to data"
    )
    await message.answer(text)
    await state.set_state(Phase.SECOND)


async def shutdown(
    dp: Dispatcher,
    bot: Bot,
) -> None:
    await bot.session.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.info("Storage is closed!")


def main():
    dp = Dispatcher(storage=SQLiteStorage())
    bot = Bot(
        token=API_TOKEN,
    )

    dp.include_router(router)
    dp.shutdown.register(shutdown)

    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
