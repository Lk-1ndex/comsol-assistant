import requests
from bs4 import BeautifulSoup
import time

def scrape_comsol_case(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 提取标题
    title = soup.find("h1")
    title_text = title.get_text(strip=True) if title else "无标题"
    
    # 提取正文内容
    content = soup.find("div", class_="content") or soup.find("main") or soup.find("article")
    content_text = content.get_text(separator="\n", strip=True) if content else ""
    
    return f"# {title_text}\n\n{content_text}"

# 先测试一个案例页面
url = "https://www.comsol.com/model/optical-ring-resonator-sensitivity-analysis-12221"
print("正在抓取...")
result = scrape_comsol_case(url)
print(result[:500])  # 先看前500个字符