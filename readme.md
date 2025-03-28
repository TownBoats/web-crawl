# DBLP论文数据爬取工具

## 工作原理
1. 通过三级流水线处理架构：
   - 第一级：从DBLP获取论文元数据（标题/作者/链接）
   - 第二级：根据链接爬取IEEE Xplore的详细内容（摘要/关键词）
   - 第三级：数据格式转换与清洗

2. 技术栈：
   - Python + BeautifulSoup + Requests
   - JSON/CSV双输出格式
   - 支持断点续爬（通过JSON Lines中间格式）

## 操作顺序
```mermaid
graph TD
    A[get-paper-list.py] -->|生成| B(paperslist_期刊名.json)
    B --> C[get-papers-maininfo-by-json.py]
    C -->|生成| D(论文详情.jsonl)
    D --> E[convert-json-2-csv.py]
    E -->|输出| F(最终结果.csv)