import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# Bot configuration
BOT_TOKEN = "7428393298:AAFJf8kB_Uiaz-lCYK7MRqBcA_Ianzbzitk"
CHANNEL_LINK = "https://t.me/your_channel"  # Replace with your actual channel
TWITTER_LINK = "https://twitter.com/your_profile"  # Replace with your Twitter

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    """Send welcome message with inline buttons"""
    try:
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
            [InlineKeyboardButton("🐦 Follow Twitter", url=TWITTER_LINK)],
            [InlineKeyboardButton("✅ I've Joined", callback_data="joined")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🚀 *Welcome to the Airdrop Bot!*\n\n"
            "To participate in our test airdrop:\n"
            "1. Join our Telegram channel\n"
            "2. Follow our Twitter account\n"
            "3. Submit your Solana wallet address\n\n"
            "Click ✅ I've Joined after completing the steps",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in start: {e}")

async def handle_joined(update: Update, context: CallbackContext) -> None:
    """Handle the joined callback"""
    try:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            "🎯 *Almost there!*\n\n"
            "Please send me your Solana wallet address now.\n"
            "Example: `7sP6...` (any text will work for this test)",
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in handle_joined: {e}")

async def handle_wallet(update: Update, context: CallbackContext) -> None:
    """Handle wallet submission"""
    try:
        wallet_address = update.message.text
        response = (
            "🎉 *Congratulations!*\n\n"
            "You've successfully claimed *10 SOL* in this test!\n\n"
            f"`Wallet:` {wallet_address}\n\n"
            "Note: This is a test bot. No actual SOL will be sent.\n"
            "Thank you for participating!"
        )
        
        await update.message.reply_text(
            response,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in handle_wallet: {e}")

def main() -> None:
    """Start the bot"""
    try:
        application = Application.builder().token(BOT_TOKEN).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(handle_joined, pattern="^joined$"))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet))

        logger.info("Bot is starting...")
        application.run_polling()
    except Exception as e:
        logger.error(f"Bot failed: {e}")

if __name__ == "__main__":
    main()
