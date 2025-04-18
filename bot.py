import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, ContextTypes)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎯 Get Daily Problems", callback_data="get_problems")],
        [InlineKeyboardButton("✅ Verify Handle", callback_data="verify_handle")],
        [InlineKeyboardButton("🔥 Track Streak", callback_data="streak")],
        [InlineKeyboardButton("⏰ Set Reminder", callback_data="reminder")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Welcome to Codeforces Bot!\nChoose an option below:",
        reply_markup=reply_markup,
    )

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"You clicked: {query.data}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button_click))

    print("🤖 Bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
