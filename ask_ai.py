import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")

# 读取知识库
with open("knowledge.txt", "r", encoding="utf-8") as f:
    knowledge = f.read()

def ask(question):
    system_prompt = f"""你是一个专业的 COMSOL 仿真助手。
请优先根据以下知识库内容回答问题：

{knowledge}

如果知识库中没有相关内容，再根据你自己的知识回答。"""

    response = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        }
    )
    return response.json()["choices"][0]["message"]["content"]

while True:
    q = input("你的问题：")
    if q == "quit":
        break
    print(ask(q))
    print()