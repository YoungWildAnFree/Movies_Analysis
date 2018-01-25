from time import sleep
import random
import requests

# 载入所有电影名称与ID
input_file = 'weighted_ratings.txt'
fobj = open(input_file, 'r')
movie_names = fobj.readlines()
fobj.close()

names = []
ids = []
for i in range(len(movie_names)):
    movie_names[i] = movie_names[i].strip().split('\t')
    names.append(movie_names[i][0])
    ids.append(movie_names[i][1])

assert len(names) == len(ids)

# 输出文件准备
output_file = 'movies_information.txt'
fobj = open(output_file, 'w')

# 请求所用信息准备
headers = [0] * 3
headers[0] = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 
    # 'Accept-Encoding': 'gzip, deflate, br', 
    # 'Accept-Language': 'en-US,en;q=0.9', 
    'Cache-Control': 'max-age=0', 
    'Connection': 'keep-alive', 
    'Cookie': 'll="108296"; bid=2yiDbcdtnp4; _pk_id.100001.4cf6=bf5b402c017e9249.1513653598.1.1513653598.1513653598.; _pk_ses.100001.4cf6=*; __utma=30149280.329777834.1513653599.1513653599.1513653599.1; __utmb=30149280.0.10.1513653599; __utmc=30149280; __utmz=30149280.1513653599.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.280159767.1513653599.1513653599.1513653599.1; __utmb=223695111.0.10.1513653599; __utmc=223695111; __utmz=223695111.1513653599.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _vwo_uuid_v2=1F50D1E7A134235D6DEA56C71D30745C|1a1045a242ee0397b6328d37242b8349', 
    # 'Host': 'movie.douban.com', 
    'Upgrade-Insecure-Requests': '1', 
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}

headers[1] = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 
    # 'Accept-Encoding': 'gzip, deflate, br', 
    # 'Accept-Language': 'en-US,en;q=0.9', 
    'Cache-Control': 'max-age=0', 
    'Connection': 'keep-alive', 
    'Cookie': 'll="108296"; bid=2yiDbcdtnp4; _pk_ses.100001.4cf6=*; __utma=30149280.329777834.1513653599.1513653599.1513653599.1; __utmb=30149280.0.10.1513653599; __utmc=30149280; __utmz=30149280.1513653599.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.280159767.1513653599.1513653599.1513653599.1; __utmb=223695111.0.10.1513653599; __utmc=223695111; __utmz=223695111.1513653599.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _vwo_uuid_v2=1F50D1E7A134235D6DEA56C71D30745C|1a1045a242ee0397b6328d37242b8349; _pk_id.100001.4cf6=bf5b402c017e9249.1513653598.1.1513656322.1513653598.', 
    'Upgrade-Insecure-Requests': '1', 
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}

headers[2] = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 
    # 'Accept-Encoding': 'gzip, deflate, br', 
    # 'Accept-Language': 'en-US,en;q=0.9', 
    'Cache-Control': 'max-age=0', 
    'Connection': 'keep-alive',
    'Cookie': 'll="108296"; bid=2yiDbcdtnp4; _pk_ses.100001.4cf6=*; __utma=30149280.329777834.1513653599.1513653599.1513653599.1; __utmc=30149280; __utmz=30149280.1513653599.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.280159767.1513653599.1513653599.1513653599.1; __utmb=223695111.0.10.1513653599; __utmc=223695111; __utmz=223695111.1513653599.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _vwo_uuid_v2=1F50D1E7A134235D6DEA56C71D30745C|1a1045a242ee0397b6328d37242b8349; __utmt=1; __utmb=30149280.2.10.1513653599; _pk_id.100001.4cf6=bf5b402c017e9249.1513653598.1.1513656569.1513653598.', 
    'Upgrade-Insecure-Requests': '1', 
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}

# 根据电影名称与ID获取其部分信息的函数
def fetch_movie_info(movie_name, movie_id, header):
    print('==============================')
    # 根据ID查询电影详细信息
    try:
        sleep(2)
        movie_url = 'https://api.douban.com/v2/movie/subject/%s' % movie_id
        req = requests.get(movie_url, headers=header)
        data = req.json()
        print(movie_name)
        print(movie_id)
        print('评分人数: ', data['ratings_count'])
        print('想看人数: ', data['wish_count'])
        print('看过人数: ', data['collect_count'])
        print('年代: ', data['year'])
        print('短评数量: ', data['comments_count'])
        print('影评数量: ', data['reviews_count'])
        print('影片类型: ', data['genres'])
    except:
        print(movie_name + ' failed in information fetching')
    # 将信息写入文件
    try:
        fobj.write(movie_name + '\t')
        fobj.write(movie_id + '\t')
        fobj.write(str(data['ratings_count']) + '\t')
        fobj.write(str(data['wish_count']) + '\t')
        fobj.write(str(data['collect_count']) + '\t')
        fobj.write(str(data['year']) + '\t')
        fobj.write(str(data['comments_count']) + '\t')
        fobj.write(str(data['reviews_count']) + '\t')
        for tag in data['genres']:
            fobj.write(tag + '\t')
        fobj.write('\n')
    except:
        print(movie_name + ' failed in file writing')
        fobj.write('\n')

# 根据电影名称与ID获取其部分信息的函数（利用代理ip）
def fetch_movie_info_with_proxy(movie_name, movie_id):
    print('==============================')
    # 根据ID查询电影详细信息
    try:
        proxy = [
            '180.105.192.26:808', '115.193.50.25:8123', '112.67.162.46:9797', '219.136.172.57:9797', 
            '58.253.100.117:8080', '222.132.145.122:53281'
        ]
        proxies = {
            'http': 'http://' + random.choice(proxy), 
            'https': 'https://' + random.choice(proxy)
        }
        sleep(2)
        movie_url = 'https://api.douban.com/v2/movie/subject/%s' % movie_id
        req = requests.get(movie_url, proxies=proxies)
        data = req.json()
        print(movie_name)
        print(movie_id)
        print('评分人数: ', data['ratings_count'])
        print('想看人数: ', data['wish_count'])
        print('看过人数: ', data['collect_count'])
        print('年代: ', data['year'])
        print('短评数量: ', data['comments_count'])
        print('影评数量: ', data['reviews_count'])
        print('影片类型: ', data['genres'])
    except:
        print(movie_name + ' failed in information fetching')
    # 将信息写入文件
    try:
        fobj.write(movie_name + '\t')
        fobj.write(movie_id + '\t')
        fobj.write(str(data['ratings_count']) + '\t')
        fobj.write(str(data['wish_count']) + '\t')
        fobj.write(str(data['collect_count']) + '\t')
        fobj.write(str(data['year']) + '\t')
        fobj.write(str(data['comments_count']) + '\t')
        fobj.write(str(data['reviews_count']) + '\t')
        for tag in data['genres']:
            fobj.write(tag + '/')
        fobj.write('\n')
    except:
        print(movie_name + ' failed in file writing')
        fobj.write('\n')

# 根据输入文件中读取到的内容，执行处理函数fetch_movie_info
for i in range(len(names)):
    if i % 2 == 0:
        fetch_movie_info(names[i], ids[i], headers[i % 3])
    else:
        fetch_movie_info_with_proxy(names[i], ids[i])

# 结束工作
print('DONE')
fobj.close()
