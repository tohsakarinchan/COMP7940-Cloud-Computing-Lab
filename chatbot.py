# chatbot.py
# 依赖：python-telegram-bot==13.7, redis, requests

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import configparser
import logging
import redis
from ChatGPT_HKBU import HKBU_ChatGPT  # 导入ChatGPT模块

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 全局变量
global redis1
global chatgpt

def main():
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read('config.ini')

    # 初始化Redis连接
    global redis1
    redis1 = redis.Redis(
        host=config['REDIS']['HOST'],
        password=config['REDIS']['PASSWORD'],
        port=config['REDIS']['REDISPORT'],
        decode_responses=config['REDIS'].getboolean('DECODE_RESPONSE'),
        username=config['REDIS']['USER_NAME']
    )

    # 初始化ChatGPT
    global chatgpt
    chatgpt = HKBU_ChatGPT(config)

    # 初始化Telegram Bot
    updater = Updater(token=config['TELEGRAM']['ACCESS_TOKEN'], use_context=True)
    dispatcher = updater.dispatcher

    # 注册命令处理器
    dispatcher.add_handler(CommandHandler("add", add))  # /add 命令
    dispatcher.add_handler(CommandHandler("help", help_command))  # /help 命令

    # 注册消息处理器（禁用原回声功能，启用ChatGPT回复）
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)

    # 启动机器人
    updater.start_polling()
    logger.info("Bot started! Press Ctrl+C to stop.")
    updater.idle()

# ChatGPT回复功能
def equiped_chatgpt(update: Update, context: CallbackContext):
    """使用ChatGPT回复用户消息"""
    user_message = update.message.text
    reply_message = chatgpt.submit(user_message)  # 调用ChatGPT API
    logger.info(f"User: {user_message}, ChatGPT: {reply_message}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

# /add 命令：统计关键词频率
def add(update: Update, context: CallbackContext):
    """统计关键词频率"""
    try:
        keyword = context.args[0]  # 获取用户输入的关键词
        redis1.incr(keyword)  # 增加关键词计数
        count = redis1.get(keyword)  # 获取当前计数
        update.message.reply_text(f'You have said "{keyword}" for {count} times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')

# /help 命令：显示帮助信息
def help_command(update: Update, context: CallbackContext):
    """显示帮助信息"""
    update.message.reply_text('Available commands:\n'
                             '/add <keyword> - Count the frequency of a keyword\n'
                             '/help - Show this help message')

if __name__ == '__main__':
    main()