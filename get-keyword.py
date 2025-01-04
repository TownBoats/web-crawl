#这个文件使用soup把html的内容保存到本地，html骨架中有需要的内容，验证了爬取的可行性
import requests
from bs4 import BeautifulSoup

def get_paper_details(ieee_url):
    """从 IEEE Xplore 页面提取论文的标题、摘要和关键词"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(ieee_url, headers=headers)
    response.raise_for_status()
    
    # 使用 BeautifulSoup 解析页面内容
    soup = BeautifulSoup(response.text, 'html.parser')
    # # 保存 response 的内容到文件
    with open(f"paper-soup.html", "w", encoding="utf-8") as soupfile:
        soupfile.write(soup.prettify())
    # 提取标题
    title_tag = soup.find('h1', class_='document-title')
    if title_tag:
        title = title_tag.find('span').text.strip()
    else:
        title = "No Title Found"

    # 提取摘要
    abstract_tag = soup.find('div', class_='abstract-text')
    if abstract_tag:
        abstract = abstract_tag.text.strip()
    else:
        abstract = "No Abstract Found"
    
    # 提取关键词
    keywords_section = soup.find('ul', class_='doc-keywords-list')
    if keywords_section:
        keywords = [kw.text.strip() for kw in keywords_section.find_all('a')]
        keywords = ', '.join(keywords)
    else:
        keywords = "No Keywords Found"
    
    return {
        "title": title,
        "abstract": abstract,
        "keywords": keywords
    }

# 示例使用
ieee_url = "https://doi.org/10.1109/TVCG.2024.3456332"  # 替换为具体的 IEEE URL
paper_details = get_paper_details(ieee_url)

print("Paper Details:")
print(f"Title: {paper_details['title']}")
print(f"Abstract: {paper_details['abstract']}")
print(f"Keywords: {paper_details['keywords']}")
