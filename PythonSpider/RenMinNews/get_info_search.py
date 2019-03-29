import sys
import os
from urllib import request
from lxml import etree
from queue import Queue
import re
import codecs

URL=Queue()

#读取文件
def readurl():
    url=open(os.path.join(sys.path[0],'RenMinWang.txt'),'r')
    urltext=url.readlines()
    for i in urltext:
        if i[len(i) - 1] == '\n':
            URL.put(i[:-1])
        else:
            URL.put(i)
    url.close()

#----------写入文件------------------------------------------------
def write_info(date,info,title):
    dates=date.replace(' ','-').replace(':','-')
    #gbk强行转码
    file=codecs.open(os.path.join(sys.path[0]+'/Info',dates+'.txt'),'w','utf-8')
    str=title+'\n'
    for i in info:
        str=str+i+'\n'
    file.write(str)
    file.close()
    print('success')
#-----------------------------------------------------------------
def write_error(url):
    #gbk强行转码
    file=codecs.open(os.path.join(sys.path[0],'error.txt'),'a','utf-8')
    file.write(url)
    file.close()
    print(url)


def getinfo():
    while URL.empty() == 0:
        try:
            url=URL.get()
            html=request.urlopen(url).read().decode('gbk','ignore')
            code = etree.HTML(html)
            date = re.findall('\d{4}年\d{1,2}月\d{1,2}日\d{2}:\d{2}', html) #日期都一样，所以使用正则表达式
            if len(date)==0: #如果找不到日期直接结束
                continue
            title = code.xpath('//h1//text()')
            text=code.xpath('//*[@id="rwb_zw"]//text()')
            if len(text)!=0 and len(title)!=0:
                write_info(date[0], text, title[0])
                continue

            text=code.xpath('//div[@class="show_text"]//text()')
            if len(text) != 0 and len(title) != 0:
                write_info(date[0], text, title[0])
                continue

            text = code.xpath('//div[@class="box_con"]//text()')
            if len(text) != 0 and len(title) != 0:
                write_info(date[0], text, title[0])
                continue

            text = code.xpath('//div[@class="text_show"]//text()')
            if len(text) != 0 and len(title) != 0:
                write_info(date[0], text, title[0])
                continue

            title = code.xpath('//*[@id="p_title"]//text()')
            text = code.xpath('//*[@id="p_content"]//text()')
            if len(text) != 0 and len(title) != 0:
                write_info(date[0], text, title[0])
                continue

            write_error(url)

        except BaseException as e:
            print(e)

if __name__ == '__main__':
    readurl()
    getinfo()