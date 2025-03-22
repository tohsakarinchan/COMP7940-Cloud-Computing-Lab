import os
import logging
from ncatbot.core import BotClient
from ncatbot.core.message import PrivateMessage
from ncatbot.utils.config import config
from ChatGPT_HKBU import HKBU_ChatGPT  # 复用你的 ChatGPT 代码

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config.set_bot_uin("2841817963")  # 设置 bot qq 号 (必填)
config.set_ws_uri("ws://localhost:3001")  # 设置 napcat websocket server 地址
config.set_token("") # 设置 token (napcat 服务器的 token)

# 初始化 Bot
bot = BotClient()

# 初始化 ChatGPT
chatgpt = HKBU_ChatGPT(
    base_url=os.getenv("CHATGPT_BASE_URL"),
    model=os.getenv("CHATGPT_MODEL"),
    api_version=os.getenv("CHATGPT_API_VERSION"),
    access_token=os.getenv("CHATGPT_ACCESS_TOKEN"),
)

@bot.private_event()
async def handle_private_message(msg: PrivateMessage):
    """处理私聊消息"""
    user_msg = msg.raw_message  # 获取消息内容
    user_id = msg.user_id

    logger.info(f"📩 收到 QQ 消息: {user_msg}")

    # 让 ChatGPT 生成回复（强制中文）
    reply = chatgpt.submit(f"请用中文回答: {user_msg}") or "抱歉，我无法理解你的问题。"
    logger.info(f"💬 ChatGPT 回复: {reply}")

    # 发送回复，使用 API 直接发送
    try:
        await bot.api.post_private_msg(user_id, text=reply)
        logger.info(f"✅ 成功发送回复: {reply}")
    except Exception as e:
        logger.error(f"❌ 发送失败: {e}")

# 启动 Bot
if __name__ == "__main__":
    bot.run()
