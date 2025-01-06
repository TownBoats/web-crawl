import requests
from bs4 import BeautifulSoup
import re
import json
import time
from tqdm import tqdm
import os

def get_paper_details(ieee_url):
    """从 IEEE Xplore 页面提取论文的标题、摘要、关键词和作者信息"""
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
            'keywords': "No Keywords Found",
            'authors': "No Authors Found"
        }
    
    # 使用 BeautifulSoup 解析页面内容
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 提取标题
    title_tag = soup.find('title')  # 找到 <title> 标签
    title = title_tag.text.split('|')[0].strip() if title_tag else "No Title Found"
    
    # 提取摘要、关键词和作者信息
    script_tag = soup.find('script', string=re.compile(r'xplGlobal\.document\.metadata='))
    abstract = "No Abstract Found"
    keywords = "No Keywords Found"
    authors = "No Authors Found"
    
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
                    
                    # 提取作者信息
                    authors_list = metadata.get('authors', [])
                    if authors_list:
                        authors = ', '.join([author['name'] for author in authors_list])
                    else:
                        authors = "No Authors Found"
                    
                except json.JSONDecodeError as e:
                    print("JSON 解码失败:", e)
    
    # 将结果存入字典
    paper_details = {
        'title': title,
        'abstract': abstract,
        'keywords': keywords,
        'authors': authors
    }
    
    return paper_details

def process_papers(json_file_path, output_file_path):
    """处理 papers.json 文件，提取每篇论文的详细信息，并保存到输出文件"""
    # 读取 papers.json
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"文件 {json_file_path} 未找到。")
        return
    except json.JSONDecodeError as e:
        print(f"读取 JSON 文件失败: {e}")
        return
    
    papers = data.get('papers', [])
    
    # 检查输出文件是否已存在，若存在则继续追加，否则创建新文件
    is_append = os.path.exists(output_file_path)
    try:
        with open(output_file_path, 'a', encoding='utf-8') as outfile:
            if not is_append:
                # 如果是新文件，写入开头的方括号（如果需要）
                # 对于 JSON Lines 格式，不需要
                pass
            
            # 使用 tqdm 添加进度条
            for index, paper in enumerate(tqdm(papers, desc="Processing Papers", unit="paper")):
                print(f"\n正在处理第 {index + 1} 篇论文: {paper.get('title', 'No Title')}")
                ieee_url = paper.get('link')
                if not ieee_url:
                    print("没有找到链接，跳过这篇论文。")
                    continue
                
                details = get_paper_details(ieee_url)
                
                # 将详情写入 JSON Lines 文件
                outfile.write(json.dumps(details, ensure_ascii=False) + '\n')
                
                # 为避免过于频繁的请求，建议在每次请求后暂停一段时间
                time.sleep(2)  # 暂停 2 秒
        print(f"\n所有论文的详细信息已保存到 {output_file_path}")
    except IOError as e:
        print(f"保存文件失败: {e}")

# 示例使用
if __name__ == "__main__":
    input_json = "cvpr-论文列表.json"  # 输入的 JSON 文件路径
    output_jsonl = "cvpr-extracted_papers_details.json"  # 输出的 JSON Lines 文件路径
    process_papers(input_json, output_jsonl)
