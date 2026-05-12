import fitz  # pymupdf
import os

def read_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# 读取docs文件夹里所有PDF
docs_folder = "docs"
all_text = ""

for filename in os.listdir(docs_folder):
    if filename.endswith(".pdf"):
        path = os.path.join(docs_folder, filename)
        print(f"正在读取：{filename}")
        text = read_pdf(path)
        all_text += f"\n\n# 案例：{filename}\n\n{text}"

# 追加到知识库
with open("knowledge.txt", "a", encoding="utf-8") as f:
    f.write(all_text)

print(f"\n完成！共导入 {len(os.listdir(docs_folder))} 个文件")
print(f"知识库现在共 {len(all_text)} 个字符")