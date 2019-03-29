from lxml import etree
from urllib import request
import os
import sys

def get_html(url):
    return request.urlopen(url).read().decode('gbk','ignore')

def get_urls(text):
    html=etree.HTML(text)
    urls=html.xpath('//h3[@class="vrTitle"]//a/@href')
    write_file(urls)

def get_next(text):
    html=etree.HTML(text)
    next=html.xpath('//a[@id="sogou_next"]/@href')
    if len(next)!=0:
        return next[0]
    else:
        return []

def write_file(urls):
    str=""
    file=open(os.path.join(sys.path[0],'wangyi.txt'),'a')
    for i in urls:
        str = str + i + '\n'
    file.write(str)
    file.close()

if __name__ == '__main__':
    url='?query=site:163.com%20%CB%BC%D5%FE+%CB%BC%CF%EB%D5%FE%D6%CE&manual=true&mode=2&sort=1&p=42230302'
    while 1:
        if len(url)!=0:
            html=get_html('http://news.sogou.com/news'+url)
            get_urls(html)
            url=get_next(html)
        else:
            break
    print("结束")