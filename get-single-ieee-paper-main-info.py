# 完成了单篇论文的关键词提取
import requests
from bs4 import BeautifulSoup
import re
import json

def get_paper_details(ieee_url):
    """从 IEEE Xplore 页面提取论文的标题、摘要和关键词"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(ieee_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return {
            'title': "No Title Found",
            'abstract': "No Abstract Found",
            'keywords': "No Keywords Found"
        }
    
    # 使用 BeautifulSoup 解析页面内容
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 保存 response 的内容到文件
    with open("paper-soup.html", "w", encoding="utf-8") as soupfile:
        soupfile.write(soup.prettify())
    
    # 提取标题
    title_tag = soup.find('title')  # 找到 <title> 标签
    title = title_tag.text.split('|')[0].strip() if title_tag else "No Title Found"
    
    # 提取摘要和关键词
    script_tag = soup.find('script', string=re.compile(r'xplGlobal\.document\.metadata='))
    abstract = "No Abstract Found"
    keywords = "No Keywords Found"
    
    if script_tag:
        script_content = script_tag.string
        if script_content:
            match = re.search(r'xplGlobal\.document\.metadata=({.*});', script_content)
            if match:
                metadata_json = match.group(1)
                try:
                    metadata = json.loads(metadata_json)  # 将字符串转换为 Python 字典
                    
                    # 提取摘要
                    abstract = metadata.get('abstract', "No Abstract Found")
                    
                    # 提取关键词
                    ieee_keywords = next((kw['kwd'] for kw in metadata.get('keywords', []) if kw['type'] == 'IEEE Keywords'), [])
                    keywords = ', '.join(ieee_keywords) if ieee_keywords else "No Keywords Found"
                    
                except json.JSONDecodeError as e:
                    print("JSON 解码失败:", e)
    
    # 将结果存入字典
    paper_details = {
        'title': title,
        'abstract': abstract,
        'keywords': keywords
    }
    
    return paper_details

# 示例使用
ieee_url = "https://ieeexplore.ieee.org/document/10670523"  # 替换为具体的 IEEE URL
paper_details = get_paper_details(ieee_url)

print("Paper Details:")
print(f"Title: {paper_details['title']}")
print(f"Abstract: {paper_details['abstract']}")
print(f"Keywords: {paper_details['keywords']}")