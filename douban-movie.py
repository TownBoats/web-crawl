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
    for start in range(0, 250, 25):
        # 构造每页的URL
        url = f"{base_url}?start={start}"
        print(f"正在爬取第{start//25 + 1}页...")
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            movie_list = soup.find_all('div', class_='item')

            for movie in movie_list:
                title = movie.find('span', class_='title').text
                info = movie.find('div', class_='bd').find('p').text.strip()
                rating = movie.find('span', class_='rating_num').text
                # 获取评价人数
                vote_count = movie.find('div', class_='star').find_all('span')[-1].text.strip('人评价')
                # 获取一句话评价（如果有的话）
                quote = movie.find('span', class_='inq')
                quote = quote.text if quote else "无"

                info_split = info.split('\n')
                director = info_split[0].split('导演: ')[-1].split('主')[0].strip()
                year = info_split[1].strip().split('/')[0].strip()
                # 获取国家/地区
                country = info_split[1].strip().split('/')[-2].strip()
                
                movie_dict = {
                    '排名': start + len(movies_data) + 1,
                    '电影名': title,
                    '导演': director,
                    '年份': year,
                    '国家/地区': country,
                    '评分': rating,
                    '评价人数': vote_count,
                    '一句话评价': quote
                }
                movies_data.append(movie_dict)

            # 添加延时
            # time.sleep(1)
            
        except Exception as e:
            print(f"爬取第{start//25 + 1}页时出错：{str(e)}")
            continue

    # 保存数据
    df = pd.DataFrame(movies_data)
    df.to_csv('douban_movies_full.csv', index=False, encoding='utf-8-sig')
    return df

if __name__ == "__main__":
    movies_df = get_movies()
    print("\n爬取完成！数据预览：")
    print(movies_df.head())
    print(f"\n总共爬取了 {len(movies_df)} 部电影")