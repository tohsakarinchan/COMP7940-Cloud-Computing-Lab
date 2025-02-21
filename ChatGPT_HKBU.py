# ChatGPT_HKBU.py
# 依赖：requests, configparser

import configparser
import requests

class HKBU_ChatGPT:
    def __init__(self, config=None):
        """
        初始化ChatGPT配置。
        支持传入配置文件路径或直接传入ConfigParser对象。
        """
        if isinstance(config, str):
            # 如果传入的是配置文件路径
            self.config = configparser.ConfigParser()
            self.config.read(config)
        elif isinstance(config, configparser.ConfigParser):
            # 如果直接传入ConfigParser对象
            self.config = config
        else:
            # 默认从当前目录读取config.ini
            self.config = configparser.ConfigParser()
            self.config.read('config.ini')

    def submit(self, message):
        """
        向HKBU ChatGPT API提交消息并获取回复。
        """
        try:
            # 构建API请求URL
            url = (
                f"{self.config['CHATGPT']['BASTCURL']}/deployments/"
                f"{self.config['CHATGPT']['MODELNAME']}/chat/completions/"
                f"?api-version={self.config['CHATGPT']['APIVERSION']}"
            )

            # 请求头（包含API Key）
            headers = {
                "Content-Type": "application/json",
                "api-key": self.config['CHATGPT']['ACCESS_TOKEN']
            }

            # 请求体（用户消息）
            payload = {
                "messages": [
                    {"role": "user", "content": message}
                ]
            }

            # 发送POST请求
            response = requests.post(url, json=payload, headers=headers)

            # 处理响应
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                return f"Error: API request failed (Status Code: {response.status_code})"

        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == '__main__':
    # 测试代码
    chatgpt = HKBU_ChatGPT()

    while True:
        try:
            user_input = input("Typing anything to ChatGPT (Press Ctrl+C to exit):\t")
            response = chatgpt.submit(user_input)
            print(f"ChatGPT: {response}\n")
        except KeyboardInterrupt:
            print("\nExiting...")
            break