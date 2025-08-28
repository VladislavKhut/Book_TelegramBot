import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.config import Config, load_config
from database.database import init_db
from handlers.other import other_router
from handlers.user import user_router
from keyboards.menu_commands import set_main_menu
from services.file_handling import prepare_book


logger = logging.getLogger(__name__)

async def main():
    config: Config = load_config()

    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.format,
    )

    logger.info("Starting bot")

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()

    logger.info("Preparing book")
    book = prepare_book("book/book.txt")
    logger.info("The book is uploaded. Total pages: %d", len(book))

    db: dict = init_db()

    db.workflow_data.update(book=book, db=db)

    await set_main_menu(bot)

    dp.include_router(user_router)
    dp.include_router(other_router)

if __name__ == "__main__":
    asyncio.run(main())