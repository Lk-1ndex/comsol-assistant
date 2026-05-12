from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# 1. 把知识库切成小段
with open("knowledge.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]

# 2. 向量化
print("正在加载模型...")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
embeddings = model.encode(chunks)

# 3. 建立索引
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

print(f"知识库已建立，共 {len(chunks)} 个片段")

# 4. 搜索测试
query = "光学微腔网格怎么设置"
query_vec = model.encode([query])
D, I = index.search(np.array(query_vec), k=2)

print(f"\n问题：{query}")
print("最相关的片段：")
for i in I[0]:
    print(f"- {chunks[i][:100]}...")