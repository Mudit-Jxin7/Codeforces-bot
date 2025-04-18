import logging

from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from models.user_model import is_verified
from utils.user_state import user_state

logger = logging.getLogger(__name__)

async def handle_button_click(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):  

    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    logger.info(f"Button clicked: {data}, by user_id={user_id}")
    await query.answer()

    if data == "verify_handle":
        user_state[user_id] = "awaiting_handle"
        await query.edit_message_text("🔍 Send your Codeforces handle to verify:")
        return

    verified = await is_verified(user_id)
    if not verified:
        logger.warning(f"Unauthorized access attempt by user_id={user_id} for {data}")
        await query.edit_message_text(
            "🚫 Please verify your Codeforces handle first by clicking '✅ Verify Handle' on /start."
        )
        return

    if data == "get_problems":
        await query.edit_message_text(
            "📚 Here are your daily problems!")
    elif data == "streak":
        await query.edit_message_text(
            "🔥 Here's your current streak!")
    elif data == "reminder":
        await query.edit_message_text(
            "⏰ Let's set a reminder!"
        ) 
