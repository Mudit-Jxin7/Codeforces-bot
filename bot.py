import asyncio
import logging
import os

from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from handlers.callback_handlers import handle_button_click
from handlers.command_handlers import start
from handlers.message_handlers import handle_text
from utils.db_utils import init_db

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

async def error_handler(update, context):
    logger.error(
        f"❌ Exception while handling update: {update}", exc_info=context.error
    )

async def main():
    await init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.add_error_handler(error_handler)

    print("🤖 Bot started")
    logger.info("Bot started successfully.")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if str(e).startswith("This event loop is already running"):
            import nest_asyncio

            nest_asyncio.apply()
            asyncio.get_event_loop().run_until_complete(main())
        else:
            raise
