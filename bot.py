import asyncio
import os

from handlers.callback_handlers import handle_button_click
from handlers.command_handlers import start
from handlers.message_handlers import handle_text
from telegram.ext import ApplicationBuilder , CommandHandler, CallbackQueryHandler, MessageHandler, filters
from utils.db_utils import init_db

from config import BOT_TOKEN

async def main():
    await init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🤖 Bot started")
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
