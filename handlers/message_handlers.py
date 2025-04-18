import requests
from models.user_model import is_verified
from services.codeforces_api import get_user_info
from telegram.ext import ContextTypes
from utils.user_state import user_state
import aiosqlite
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_state.get(user_id) == "awaiting_handle":
        handle = update.message.text.strip()
        api_url = f"https://codeforces.com/api/user.info?handles={handle}"

        response = requests.get(api_url)
        if response.status_code == 200 and response.json().get("status") == "OK":
            user_info = response.json()["result"][0]
            username = (
                user_info.get("firstName", "") + " " + user_info.get("lastName", "")
            )
            username = username.strip() or user_info.get("handle", handle)

            async with aiosqlite.connect("users.db") as db:
                await db.execute(
                    "INSERT OR REPLACE INTO users (user_id, handle) VALUES (?, ?)",
                    (user_id, handle),
                )
                await db.commit()

            await update.message.reply_text(
                f"✅ Handle '{handle}' verified successfully!"
            )

            keyboard = [
                [
                    InlineKeyboardButton(
                        "🎯 Get Daily Problems", callback_data="get_problems"
                    )
                ],
                [InlineKeyboardButton("🔥 Track Streak", callback_data="streak")],
                [InlineKeyboardButton("⏰ Set Reminder", callback_data="reminder")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                f"👋 Hi {username}!\nHere's what you can do next:",
                reply_markup=reply_markup,
            )

            user_state.pop(user_id, None)
        else:
            await update.message.reply_text(
                "❌ Invalid Codeforces handle. Try again or click /start to cancel."
            )
