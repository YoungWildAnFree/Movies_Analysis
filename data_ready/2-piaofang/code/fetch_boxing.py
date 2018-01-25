from lxml import etree
import requests
import time

# 读取含有票房链接的文件
input_file = 'boxing_urls.txt'
fobj = open(input_file, 'r')
content = fobj.readlines()
fobj.close()

# 清洗数据并装载电影名称与票房链接
names = []
urls = []
for i in range(len(content)):
    temp = content[i].strip().split('\t')
    name = temp[0]
    url = temp[-1]
    names.append(name)
    urls.append(url)

boxings = []

# 准备输出文件
output_file = 'boxings.txt'
fobj = open(output_file, 'a')

# # 使用代理IP
# proxy = '111.13.109.27:80'
# proxies = {
#     'http': 'http://' + proxy, 
#     'https': 'https://' + proxy
# }

# 抓取票房并同步写入文件中
for i in range(len(urls)):
    time.sleep(1)
    url = urls[i]
    name = names[i]
    try:
        # req = requests.get(url, proxies=proxies)
        req = requests.get(url)
        html = req.text
        tree = etree.HTML(html)
        # 获取class属性为m-span的span标签下的信息
        boxing_data = tree.xpath('//span[@class="m-span"]/text()')
        print(name + '\t' + boxing_data[-1])
        fobj.write(name + '\t' + boxing_data[-1] + '\n')
    except:
        print(name + ' in exception')
        fobj.write(name + '\t' + 'NA' + '\n')

fobj.close()
