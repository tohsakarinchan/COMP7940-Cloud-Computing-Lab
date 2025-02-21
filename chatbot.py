# chatbot.py
# 依赖：python-telegram-bot==13.7, urllib3==1.26.18

import telegram
from telegram.ext import Updater, MessageHandler, Filters
import configparser
import logging

# 配置日志格式
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def echo(update, context):
    """将用户消息转为大写并回复"""
    user_message = update.message.text
    reply_message = user_message.upper()  # 转为大写
    
    # 记录日志（可选）
    logger.info(f"Received message: {user_message}")
    logger.info(f"Reply message: {reply_message}")
    
    # 发送回复
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply_message
    )

def main():
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['TELEGRAM']['ACCESS_TOKEN']  # 从config.ini获取Token
    
    # 初始化Updater和Dispatcher
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    
    # 添加消息处理器：监听非命令的文本消息
    echo_handler = MessageHandler(
        Filters.text & (~Filters.command),  # 过滤纯文本且非指令的消息
        echo
    )
    dispatcher.add_handler(echo_handler)
    
    # 启动机器人
    updater.start_polling()
    logger.info("Bot started! Press Ctrl+C to stop.")
    updater.idle()  # 保持运行直到手动停止

if __name__ == '__main__':
    main()