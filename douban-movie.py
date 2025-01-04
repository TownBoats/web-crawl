import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

def get_movies():
    base_url = "https://movie.douban.com/top250"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    movies_data = []

    # 遍历所有页面
    for page in range(10):  # 0-9 共10页
        start = page * 25
        url = f"{base_url}?start={start}"
        print(f"正在爬取第{page + 1}页...")
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            movie_list = soup.find_all('div', class_='item')

            # # 保存 response 的内容到文件
            # with open(f"douban_top250_pages/response_page_{page + 1}.html", "w", encoding="utf-8") as response_file:
            #     response_file.write(response.text)
            
            # # 保存 soup 的内容到文件
            # with open(f"douban_top250_pages/soup_page_{page + 1}.html", "w", encoding="utf-8") as soup_file:
            #     soup_file.write(soup.prettify())
            
            # print(movie_list)

            for movie in movie_list:
                # 直接从电影条目的序号标签获取排名
                rank = movie.find('em').text
                title = movie.find('span', class_='title').text
                info = movie.find('div', class_='bd').find('p').text.strip()
                rating = movie.find('span', class_='rating_num').text
                vote_count = movie.find('div', class_='star').find_all('span')[-1].text.strip('人评价')
                quote = movie.find('span', class_='inq')
                quote = quote.text if quote else "无"

                info_split = info.split('\n')
                director = info_split[0].split('导演: ')[-1].split('主')[0].strip()
                year = info_split[1].strip().split('/')[0].strip()
                country = info_split[1].strip().split('/')[-2].strip()
                
                movie_dict = {
                    '排名': int(rank),  # 转换为整数以确保排序正确
                    '电影名': title,
                    '导演': director,
                    '年份': year,
                    '国家/地区': country,
                    '评分': rating,
                    '评价人数': vote_count,
                    '一句话评价': quote
                }
                movies_data.append(movie_dict)

            time.sleep(1)
            
        except Exception as e:
            print(f"爬取第{page + 1}页时出错：{str(e)}")
            continue

    # 将数据转换为DataFrame并按排名排序
    df = pd.DataFrame(movies_data)
    df = df.sort_values(by='排名')  # 确保按排名排序
    df.to_csv('douban_movies_full.csv', index=False, encoding='utf-8-sig')
    return df

if __name__ == "__main__":
    movies_df = get_movies()
    print("\n爬取完成！数据预览：")
    print(movies_df.head())
    print(f"\n总共爬取了 {len(movies_df)} 部电影")