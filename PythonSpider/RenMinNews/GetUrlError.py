import urllib.request
import lxml
from lxml import etree
import re
import sys
import os
from queue import Queue

def GetURL():
    url = ""
    for year in range(2014,2018):#年份
        for month in range(1,13):#月份
            if year%400==0 or (year%4==0 and year%100!=0) and month==2: #判断闰年二月
                for date in range(1, 30):
                    url = "http://news.people.com.cn/GB/28053/review/" + str(year) + str(month).zfill(2) + str(
                        date).zfill(2) + ".html"
                    GetInfo(url)
            elif year%400!=0 and month==2:#判断平年二月
                for date in range(1,29):
                    url = "http://news.people.com.cn/GB/28053/review/" + str(year) + str(month).zfill(2) + str(
                        date).zfill(2) + ".html"
                    GetInfo(url)
            elif month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12: #判断大月份
                for date in range(1,32):
                    url = "http://news.people.com.cn/GB/28053/review/" + str(year) + str(month).zfill(2) + str(
                        date).zfill(2) + ".html"
                    GetInfo(url)
            else:
                for date in range(1,31):
                    url = "http://news.people.com.cn/GB/28053/review/" + str(year) + str(month).zfill(2) + str(
                        date).zfill(2) + ".html"
                    GetInfo(url)

def GetInfo(url):
    try:
        page=''
        page = urllib.request.urlopen(url).read().decode('gbk')
    except BaseException as e:
        f=open(os.path.join(sys.path[0],'错误网页.txt'),'a')
        f.write(url+'\n')
        f.close()
        print(url)
        print(e)

if __name__=='__main__':
    GetURL()
