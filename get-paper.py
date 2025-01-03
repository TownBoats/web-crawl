import requests
from bs4 import BeautifulSoup
import csv

# 定义请求头，模拟浏览器访问
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 发送 HTTP 请求
url = "https://dblp.org/db/journals/tvcg/tvcg31.html"
response = requests.get(url, headers=headers)
response.raise_for_status()  # 检查请求是否成功

# 解析 HTML 内容
soup = BeautifulSoup(response.text, "html.parser")

# 定义论文信息列表
papers = []

# 解析论文条目
for entry in soup.find_all('li', class_='entry'):
    title = entry.find('span', class_='title').text.strip()
    authors = ', '.join([author.text.strip() for author in entry.find_all('span', itemprop='author')])
    year = entry.find('span', itemprop='datePublished').text.strip() if entry.find('span', itemprop='datePublished') else "N/A"
    venue = entry.find('span', class_='venue').text.strip() if entry.find('span', class_='venue') else "N/A"
    if year in ['2022', '2023', '2024']:
        papers.append([year, title, authors, venue])

# 保存为 CSV 文件
with open('open_vocabulary_papers_2022_2024.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Year", "Title", "Authors", "Venue"])
    writer.writerows(papers)

print("CSV 文件已生成: open_vocabulary_papers_2022_2024.csv")
