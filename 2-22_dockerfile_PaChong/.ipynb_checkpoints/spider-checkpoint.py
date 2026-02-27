import requests
from bs4 import BeautifulSoup
import csv
import time

# 设置基础URL和请求头
base_url = 'https://movie.douban.com/top250'  # 添加这一行
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 创建一个空列表来存储所有电影信息
all_movies = []

# 设置请求头，模拟浏览器访问，这是为了避免被豆瓣服务器拒绝 [citation:1][citation:2]
for start in range(0, 250, 25):
    url = f'{base_url}?start={start}'
    print(f'正在抓取: {url}')

    # 2. 发送请求，获取网页内容
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
    except requests.exceptions.RequestException as e:
        print(f'请求失败: {e}')
        continue # 如果当前页面请求失败，则跳过，继续尝试下一页

    # 3. 使用BeautifulSoup解析HTML [citation:1][citation:2]
    soup = BeautifulSoup(response.text, 'html.parser')

    # 4. 找到所有电影条目，它们都在class为'item'的div标签里
    movie_items = soup.find_all('div', class_='item')

    # 5. 遍历每个电影条目，提取需要的信息
    for item in movie_items:
        # 电影名称 (中文名)
        title = item.find('span', class_='title').text

        # 评分
        rating = item.find('span', class_='rating_num').text

        # 导演、主演等信息都藏在一个段落里，需要进一步处理 [citation:2]
        info_p = item.find('div', class_='bd').find('p').text.strip()
        # 按行分割，第一行通常是导演和主演信息
        info_lines = info_p.split('\n')
        # 提取导演和主演（这里为了简化，只取了第一行）
        director_actors = info_lines[0].strip() if len(info_lines) > 0 else ''
        
        # 提取年份（年份通常在第二行，并且包含很多空格，需要清理）
        year_line = info_lines[1].strip() if len(info_lines) > 1 else ''
        # 使用split()和strip()提取出干净的年份，例如'1994'
        year = year_line.split('/')[0].strip() if year_line else ''

        # 电影类型 (在<p>标签后的一个<span>里)
        genre_tag = item.find('span', class_='genre')
        genre = genre_tag.text.strip() if genre_tag else ''

        # 将当前电影的信息存入字典
        movie_data = {
            '名称': title,
            '评分': rating,
            '导演/主演': director_actors,
            '年份': year,
            '类型': genre
        }
        all_movies.append(movie_data)

    # 6. 礼貌地暂停一下，避免请求频率过高被封IP [citation:1][citation:7]
    time.sleep(2)

print('所有页面抓取完成！')

# 定义CSV文件的列名
fieldnames = ['名称', '评分', '导演/主演', '年份', '类型']

# 将数据写入CSV文件 [citation:2][citation:3][citation:6]
with open('douban_top250.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()  # 写入列名
    writer.writerows(all_movies)  # 写入所有电影数据

print(f'数据已保存到 douban_top250.csv，共 {len(all_movies)} 部电影。')