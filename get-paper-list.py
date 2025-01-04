import requests
from bs4 import BeautifulSoup
import json
import csv

# 定义请求头，模拟浏览器访问
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 发送 HTTP 请求
# url = "https://dblp.org/db/journals/tvcg/tvcg31.html"
url = "https://dblp.org/db/conf/cvpr/cvpr2024.html"
response = requests.get(url, headers=headers)
response.raise_for_status()  # 检查请求是否成功

# 解析 HTML 内容
soup = BeautifulSoup(response.text, "html.parser")

# 定义论文信息列表
papers = []

# 提取期刊信息
journal_info = {
    "journal_name": soup.find('h1').text.strip() if soup.find('h1') else "No Journal Name Found",
    "volume": soup.find('header', class_='h2').text.strip() if soup.find('header', class_='h2') else "No Volume Found"
}

# 解析论文条目
for entry in soup.find_all('li', class_='entry'):
    # 提取标题
    title_tag = entry.find('span', class_='title')
    title = title_tag.text.strip() if title_tag else "No Title Found"
    
    # 提取论文链接
    link_tag = entry.find('a', href=True)  # 找到第一个带有 href 的 <a> 标签
    link = link_tag['href'] if link_tag else "No Link Found"
    
    # 提取作者
    authors = ', '.join([author.text.strip() for author in entry.find_all('span', itemprop='author')])
    
    # 提取年份
    year_tag = entry.find('meta', itemprop='datePublished')
    year = year_tag['content'] if year_tag else "N/A"
    
    # 将论文信息添加到列表中
    papers.append({
        "title": title,
        "link": link,
        "authors": authors,
        "year": year
    })

# 将期刊信息与论文信息合并
data = {
    "journal_info": journal_info,
    "papers": papers
}

# 保存为 JSON 文件
with open('paperslist{journal_info}.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("JSON 文件已生成: papers.json")

# 保存为 CSV 文件
with open(f'paperslist{journal_info}.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'link', 'authors', 'year']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for paper in papers:
        writer.writerow(paper)

print("CSV 文件已生成: papers.csv")