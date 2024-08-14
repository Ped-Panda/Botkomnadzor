import sys
import asyncio
import logging

from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message

from censure import Censor

TOKEN = "7213621846:AAEzKd7UdAMSusc5-uSFkHS2La3kGYP4iks"

dp = Dispatcher()

sys.path.append('./censure')
censure_ru = Censor.get(lang='ru')


@dp.message()
async def exo(message: Message) -> None:
    line_info = censure_ru.clean_line(message.text)
    _word = line_info[3][0] if line_info[1] else line_info[4][0] if line_info[2] else None

    check_result = None

    if _word is not None:
        check_result = [_word, line_info]

    if check_result:
        await message.delete()
        await message.answer(f"Пользователь {message.from_user.first_name} написал непристойность")


async def main() -> None:
    session = AiohttpSession(proxy="http://proxy.server:3128")
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())