from lxml import etree
import requests

for year in range(1991, 2018):
    try: 
        # 请求页面，抓取电影名称
        url = 'http://www.1905.com/mdb/film/calendaryear/%s' % str(year)
        req = requests.get(url)
        html = req.text
        tree = etree.HTML(html)
        # 选取所有class属性为film的a标签中的内容
        movies_names = tree.xpath('//a[@class="film"]/text()')
        
        # 数据输出
        output_file = 'movies/movies-%s.txt' % str(year)
        fobj = open(output_file, 'w')
        for movie in movies_names:
            fobj.write(movie + '\n')
        fobj.close()
        print(str(year) + ' completed successfully')
    except:
        print('Failure in ' + str(year))
