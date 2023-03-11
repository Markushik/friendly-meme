"""
The main file responsible for launching the bot
"""

import asyncio

import nats
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from loguru import logger
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine

from config import settings
from handlers import client
from tgbot.database.base import BaseModel
from tgbot.database.engine import proceed_schemas, get_session_maker
from tgbot.fsm.entry import NatsStorage
from tgbot.handlers import errors


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/exchange", description="Актуальный курс юаня")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


async def main() -> None:
    """
    The main function responsible for launching the bot
    :return:
    """
    logger.add("../debug.log", format="{time} {level} {message}", level="DEBUG")
    logger.info("LAUNCHING BOT")

    nats_conn = await nats.connect()
    jetstream = nats_conn.jetstream()

    kv_states = await jetstream.key_value('fsm_states_aiogram')
    kv_data = await jetstream.key_value('fsm_data_aiogram')

    database_url = URL.create(
        drivername="postgresql+asyncpg", host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT, username=settings.POSTGRES_USERNAME,
        password=settings.POSTGRES_PASSWORD, database=settings.POSTGRES_DATABASE,
    )

    bot = Bot(token=settings.API_TOKEN, parse_mode="HTML")
    disp = Dispatcher(storage=NatsStorage(nats_conn, kv_states, kv_data))

    disp.include_router(client.router)
    disp.include_router(errors.router)

    async_engine = create_async_engine(database_url)
    session_maker = get_session_maker(async_engine)

    try:
        await set_commands(bot)
        await proceed_schemas(async_engine, BaseModel.metadata)
        await disp.start_polling(bot,
                                 allowed_updates=disp.resolve_used_update_types(),
                                 session_maker=session_maker,
                                 nats_conn=nats_conn,
                                 jetstream=jetstream)
    finally:
        await disp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (SystemExit, KeyboardInterrupt, ConnectionRefusedError):
        logger.warning("SHUTDOWN BOT")
