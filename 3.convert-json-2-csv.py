import pandas as pd
import json
import os

# 输入文件路径
input_file_path = "cvpr-extracted_papers_details.json"
# 输出文件路径
output_file_path = "cvpr-extracted_papers_details_corrected.json"

# 用于存储解析后的 JSON 对象
data = []

# 逐行读取文件并解析 JSON 对象
with open(input_file_path, "r", encoding="utf-8") as file:
    for line in file:
        # 去除行首尾的空白字符
        line = line.strip()
        if line:  # 确保行不为空
            try:
                # 解析每行的 JSON 对象
                json_obj = json.loads(line)
                data.append(json_obj)
            except json.JSONDecodeError as e:
                print(f"解析错误：{e}，行内容：{line}")

# 将解析后的数据写入新的 JSON 文件
with open(output_file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"标准格式的 JSON 文件已保存为 {output_file_path}")

# 检查文件是否存在
if not os.path.exists(output_file_path):
    print(f"错误：文件 {output_file_path} 不存在！")
    exit()

try:
    # 从 JSON 文件中加载数据
    with open(output_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # 将 JSON 数据转换为 Pandas DataFrame
    df = pd.DataFrame(data)

    # 将 DataFrame 保存为 CSV 文件
    output_csv_path = "cvpr-extracted_papers_details.csv"
    df.to_csv(output_csv_path, index=False, encoding="utf-8")

    print(f"CSV 文件已保存为 {output_csv_path}")

except json.JSONDecodeError as e:
    print(f"JSON 文件格式错误：{e}")
except Exception as e:
    print(f"发生未知错误：{e}")