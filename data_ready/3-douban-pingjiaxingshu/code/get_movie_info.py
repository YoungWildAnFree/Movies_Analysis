from movie import Movie
import requests
import time

# 控制当前循环是否使用代理ip
use_proxy = True
# 抓取结果存储于list，元素类型为Movie
result = []

for year in range(1991, 2018):
    print("movies in %d" % year)

    filename = 'movies/movies-%d.txt' % year
    fobj = open(filename, 'r')
    content = fobj.readlines()

    for i in range(len(content)):
        time.sleep(2)
        # 交替使用代理ip
        use_proxy = not use_proxy

        movie_name = content[i].strip()

        # 使用代理的情况
        if use_proxy:
            proxy = '111.13.109.27:80'
            proxies = {
                'http': 'http://' + proxy, 
                'https': 'https://' + proxy
            }

            try:
                url = 'https://api.douban.com/v2/movie/search?q=%s' % movie_name
                req = requests.get(url, proxies=proxies)
                data = req.json()
                average_rating = data['subjects'][0]['rating']['average']
                id_number = data['subjects'][0]['id']
                print(movie_name, average_rating, id_number)
                result.append(Movie(movie_name, average_rating, id_number, year))
            except:
                pass

        # 不使用代理的情况
        else:
            try:
                url = 'https://api.douban.com/v2/movie/search?q=%s' % movie_name
                req = requests.get(url)
                data = req.json()
                average_rating = data['subjects'][0]['rating']['average']
                id_number = data['subjects'][0]['id']
                print(movie_name, average_rating, id_number)
                result.append(Movie(movie_name, average_rating, id_number, year))
            except:
                pass
    fobj.close()

# 保存数据
fobj = open('ratings.txt', 'w')
for i in range(len(result)):
    current = result[i]
    fobj.write(current.name + '\t')
    fobj.write(str(current.rating) + '\t')
    fobj.write(current.id_number + '\t')
    fobj.write(str(current.year) + '\n')
fobj.close()
