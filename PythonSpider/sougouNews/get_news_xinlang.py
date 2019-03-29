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
    file=open(os.path.join(sys.path[0],'xinlang.txt'),'r')
    urls=file.readlines()
    for i in urls:
        url.put(i[:-1])
#------写文件-------
def write_info(date,info,title):
    dates=date.replace(' ','-').replace(':','-')
    #gbk强行转码
    file=codecs.open(os.path.join(sys.path[0]+'/xinlang',dates+'.txt'),'w','utf-8')
    str=title+'\n'
    for i in info:
        str=str+i+'\n'
    file.write(str)
    file.close()


def get_info():
    while url.empty()==0:
        URL=url.get()
        print(URL)
        try:
            html=request.urlopen(URL).read().decode('utf-8')
        except:
            html = request.urlopen(URL).read().decode('gbk')
        code=etree.HTML(html)
        date = re.findall('\d{4}年\d{1,2}月\d{1,2}日 \d{2}:\d{2}', html)  # 日期都一样，所以使用正则表达式
        if len(date)==0:
            date = re.findall('\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}', html)
        if len(date) == 0:  # 如果找不到日期直接结束
            continue
        title=code.xpath('//*[@id="artibody"]//h1/text()')
        info=code.xpath('//*[@id="artibody"]/div[3]//text()')
        if len(title)==0:
            title=code.xpath('//*[@id="artibodyTitle"]/text()')
            info=code.xpath('//*[@id="artibody"]//text()')
        if len(title)==0:
            title=code.xpath('//*[@id="main_title"]/text()')
        write_info(date[0],info,title[0])

if __name__ == '__main__':
    read_url()
    get_info()