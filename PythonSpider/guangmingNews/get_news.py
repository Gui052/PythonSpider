# coding=utf-8
from urllib import request
import os
from lxml import etree
from queue import Queue
import re
import sys
import codecs

url=Queue()
#------读取url-----
def read_url():
    file=open(os.path.join(sys.path[0],'guangming.txt'),'r')
    urls=file.readlines()
    for i in urls:
        url.put(i[:-1])

#------写文件-------
def write_info(date,info,title):
    dates=date.replace(' ','-').replace(':','-')
    #gbk强行转码
    file=codecs.open(os.path.join(sys.path[0]+'/news',dates+'.txt'),'a','utf-8')
    str=title+'\n'
    for i in info:
        str=str+i+'\n'
    str=re.sub('[A-Za-z\[\`\@\#\$\^\&\*\(\)\=\|\{\}\]\<\>\/\'\+\~\\\%]', '', str)
    file.write(str)
    file.close()


def get_info():
    while url.empty()==0:
        URL=url.get()
        try:
            html=request.urlopen(URL).read().decode('utf-8','ignore')
        except:
            html = request.urlopen(URL).read().decode('gbk','ignore')
        code=etree.HTML(html)
        date = re.findall('\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}', html) #日期都一样，所以使用正则表达式
        if len(date) == 0:  # 如果找不到日期直接结束
            date=re.findall('\d{4}年\d{1,2}月\d{1,2}日', html)
        if len(date) == 0:
            continue
        title=code.xpath('//*[@id="articleTitle"]//text()')
        info=code.xpath('//*[@id="contentMain"]//text()')
        if len(info)==0:
            info=code.xpath('//div[@class="c_c"]//text()')
        if len(title)==0:
            title=code.xpath('//h1/text()')
        if len(info)!=0 and len(title)!=0:
            write_info(date[0],info,title[0])
            print(URL)
if __name__ == '__main__':
    read_url()
    get_info()