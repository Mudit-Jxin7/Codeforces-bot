from models.user_model import is_verified
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, ContextTypes
from models.user_model import is_verified
from services.codeforces_api import get_user_info

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    verified = await is_verified(user_id)

    if verified:
        keyboard = [
            [
                InlineKeyboardButton(
                    "🎯 Get Daily Problems", callback_data="get_problems"
                )
            ],
            [InlineKeyboardButton("🔥 Track Streak", callback_data="streak")],
            [InlineKeyboardButton("⏰ Set Reminder", callback_data="reminder")],
        ]
        text = "👋 Welcome back! Choose an option below:"
    else:
        keyboard = [
            [InlineKeyboardButton("✅ Verify Handle", callback_data="verify_handle")],
        ]
        text = "👋 Welcome to Codeforces Bot! Please verify your handle first."

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)
