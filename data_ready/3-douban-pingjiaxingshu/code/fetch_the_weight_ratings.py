from lxml import etree
from movie import Movie
from time import sleep
from threading import Thread
import requests

# 输入文件
input_file = 'ratings.txt'
input_fobj = open(input_file, 'r')
content = input_fobj.readlines()
input_fobj.close()

# 输出文件
output_file = 'weighted_ratings.txt'
output_fobj = open(output_file, 'w')

# 检查数据缺失情况
zero_movie = 0
# 轮换是否使用代理IP的控制变量
use_proxy = False
movies = []

# 抓取过程函数，轮换使用代理IP
def fetch_weighted_rating(movie_obj, use_proxy):
    assert isinstance(movie_obj, Movie)

    id_number = movie_obj.id_number
    url = 'https://movie.douban.com/subject/%s/?from=showing' % id_number
    
    # 使用代理IP的情况
    if use_proxy:
        proxy = '111.13.109.27:80'
        proxies = {
            'http': 'http://' + proxy, 
            'https': 'https://' + proxy
        }

        try:
            req = requests.get(url, proxies=proxies)
            html = req.text
            tree = etree.HTML(html)
            print(tree)

            print(movie_obj.name)
            # 获取评价人数，所有property属性为v:votes的span标签的内容
            total_people = tree.xpath('//span[@property="v:votes"]/text()')
            print(total_people)
            # 获取评价星级分布，所有class属性为rating_per的span标签的内容
            ratings_weight = tree.xpath('//span[@class="rating_per"]/text()')
            print(ratings_weight)

            # 抓取到的评分是string类型的list, 将其转为float或者int类型
            for i in range(len(ratings_weight)):
                ratings_weight[i] = eval(ratings_weight[i][:-1])

            # 为Movie对象设置评价人数以及评分分布
            movie_obj.set_amount(total_people[0])
            movie_obj.set_weighted_ratings(ratings_weight)

            movies.append(movie_obj)
        except:
            pass

    # 不使用代理IP的情况
    else:
        try:
            req = requests.get(url)
            html = req.text
            tree = etree.HTML(html)
            print(tree)

            print(movie_obj.name)
            # 获取评价人数，所有property属性为v:votes的span标签的内容
            total_people = tree.xpath('//span[@property="v:votes"]/text()')
            print(total_people)
            # 获取评价分布，所有class属性为rating_per的span标签的内容
            ratings_weight = tree.xpath('//span[@class="rating_per"]/text()')
            print(ratings_weight)

            # 抓取到的评分是string类型的list, 将其转为float或者int类型
            for i in range(len(ratings_weight)):
                ratings_weight[i] = eval(ratings_weight[i][:-1])

            # 设置评价人数以及评分分布
            movie_obj.set_amount(total_people[0])
            movie_obj.set_weighted_ratings(ratings_weight)

            movies.append(movie_obj)
        except:
            pass


# 读取电影数据后创建Movie对象，并多线程执行详细数据的抓取与更新
for i in range(len(content)):
    data = content[i].strip().split('\t')
    print(content[i])
    print(data)
    # 倘若当前电影无评分，则跳过当前的影片的数据抓取与整理工作
    data[1] = float(data[1])
    if data[1] == 0:
        zero_movie += 1
        continue

    current_movie = Movie(data[0], data[1], data[2], data[3])

    # 轮换是否使用代理
    use_proxy = not use_proxy
    sleep(1)
    Thread(target=fetch_weighted_rating, args=(current_movie, use_proxy)).start()

# 输出数据缺失情况
print("=======================")
print(zero_movie)
print("=======================")

# 将所有信息写入文件
for i in range(len(movies)):
    current_movie = movies[i]
    output_fobj.write(str(current_movie.name) + '\t')
    output_fobj.write(str(current_movie.id_number) + '\t')
    output_fobj.write(str(current_movie.year) + '\t')
    output_fobj.write(str(current_movie.rating) + '\t')
    output_fobj.write(str(current_movie.amount) + '\t')
    for item in current_movie.weighted_ratings:
        output_fobj.write(str(item) + '\t')
    output_fobj.write('\n')
output_fobj.close()
