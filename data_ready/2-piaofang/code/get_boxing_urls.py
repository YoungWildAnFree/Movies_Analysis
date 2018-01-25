from lxml import etree
import requests
import time

names = []
# 装载电影名称信息文件
input_file = 'movies_names.txt'
fobj = open(input_file, 'r')
content = fobj.readlines()
for i in range(len(content)):
    content[i] = content[i].strip()
    names.append(content[i])
fobj.close()

# 将电影名称与票房信息链接存入文件中
output_file = 'boxing_urls.txt'
fobj = open(output_file, 'a')

proxy = '111.13.109.27:80'
proxies = {
    'http': 'http://' + proxy, 
    'https': 'https://' + proxy
}

# 根据电影名称获取票房查询链接
boxing_url = []
for name in names:
    time.sleep(1)
    search_url = 'http://www.cbooo.cn/search?k=%s' % name
    try:
        # 访问含有票房链接的页面
        req = requests.get(search_url, proxies=proxies)
        html = req.text
        tree = etree.HTML(html)
        # 抓取target属性为_blank的<a>标签下的href属性的信息
        boxing_urls = tree.xpath('//a[@target="_blank"]/@href')
        print(name + '\t' + boxing_urls[1])
        boxing_url.append(boxing_urls[1])
        fobj.write(name + '\t' + boxing_url[-1] + '\n')
    except:
        print(name + " in exception")
        boxing_url.append(None)
        fobj.write(name + '\t' + 'NA' + '\n')

assert len(names) == len(boxing_url)
fobj.close()
