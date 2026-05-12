import requests
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")

# 建立知识库索引
with open("knowledge.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
embeddings = model.encode(chunks)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

def search(question, k=2):
    vec = model.encode([question])
    D, I = index.search(np.array(vec), k=k)
    return "\n\n".join([chunks[i] for i in I[0]])

def ask(question):
    context = search(question)
    system_prompt = f"""你是一个专业的 COMSOL 仿真助手。
请根据以下参考资料回答问题：

{context}

如果参考资料不足，再根据自己的知识补充。"""

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

print("COMSOL 助手已启动（RAG版）")
while True:
    q = input("\n你的问题：")
    if q == "quit":
        break
    print(ask(q))