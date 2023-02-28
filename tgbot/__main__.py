"""
The main file responsible for launching the bot
"""

import asyncio

import nats
from aiogram import Bot, Dispatcher
from loguru import logger

from config import settings
from handlers import client
from tgbot.fsm.entry import NatsStorage


async def main() -> None:
    """
    The main function responsible for launching the bot
    :return:
    """
    logger.add("../debug.log", format="{time} {level} {message}", level="DEBUG")
    logger.info("LAUNCHING BOT")

    nc = await nats.connect()
    js = nc.jetstream()

    kv_states = await js.key_value('fsm_states_aiogram')
    kv_data = await js.key_value('fsm_data_aiogram')

    bot = Bot(token=settings.API_TOKEN, parse_mode="HTML")
    disp = Dispatcher(storage=NatsStorage(nc, kv_states, kv_data))

    disp.include_router(client.router)
    # disp.include_router(errors.router)

    try:
        # await set_commands(bot)
        await disp.start_polling(bot, allowed_updates=disp.resolve_used_update_types(), nc=nc, js=js)
    finally:
        await disp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (SystemExit, KeyboardInterrupt, ConnectionRefusedError):
        logger.warning("SHUTDOWN BOT")

