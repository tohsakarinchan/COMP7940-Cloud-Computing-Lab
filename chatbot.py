import os
import logging
import redis
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from ChatGPT_HKBU import HKBU_ChatGPT

# 配置日志
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# 全局变量
global redis1
global chatgpt


def add(update: Update, context: CallbackContext):
    """统计关键词频率"""
    try:
        keyword = context.args[0]
        redis1.incr(keyword)
        count = redis1.get(keyword)
        update.message.reply_text(f'You have said "{keyword}" for {count} times.')
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /add <keyword>")


def help_command(update: Update, context: CallbackContext):
    """显示帮助信息"""
    update.message.reply_text(
        "Available commands:\n"
        "/add <keyword> - Count the frequency of a keyword\n"
        "/help - Show this help message"
    )


def hello_command(update: Update, context: CallbackContext):
    """Responds to the /hello command"""
    if context.args:
        name = context.args[0]
        update.message.reply_text(f"Good day, {name}!")
    else:
        update.message.reply_text("Usage: /hello <name>")


def equiped_chatgpt(update: Update, context: CallbackContext):
    """使用 ChatGPT 回复用户消息"""
    user_message = update.message.text
    reply_message = chatgpt.submit(user_message)
    logger.info(f"User: {user_message}, ChatGPT: {reply_message}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


def main():
    # 读取 Redis 连接 URL
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        logger.error("❌ REDIS_URL is not set!")
        raise ValueError("REDIS_URL is missing!")

    # 初始化 Redis 连接
    global redis1
    redis1 = redis.Redis.from_url(redis_url, decode_responses=True)

    try:
        redis1.ping()
        logger.info("✅ Connected to Redis successfully!")
    except redis.exceptions.ConnectionError:
        logger.error("❌ Failed to connect to Redis.")
        raise

    # 读取 Telegram Token
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    if not telegram_token:
        logger.error("❌ TELEGRAM_TOKEN is not set!")
        raise ValueError("TELEGRAM_TOKEN is missing!")

    # 初始化 ChatGPT
    global chatgpt
    chatgpt = HKBU_ChatGPT(
        base_url=os.getenv("CHATGPT_BASE_URL"),
        model=os.getenv("CHATGPT_MODEL"),
        api_version=os.getenv("CHATGPT_API_VERSION"),
        access_token=os.getenv("CHATGPT_ACCESS_TOKEN"),
    )

    # 初始化 Telegram Bot
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher

    # 注册命令处理器
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello_command))

    # 注册消息处理器（ChatGPT 回复）
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)

    # 启动 Bot
    updater.start_polling()
    logger.info("🤖 Bot started! Press Ctrl+C to stop.")
    updater.idle()

if __name__ == "__main__":
    main()
