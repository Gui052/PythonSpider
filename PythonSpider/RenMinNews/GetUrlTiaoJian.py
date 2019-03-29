import urllib.request
import lxml
from lxml import etree
import re
import sys
import os
from queue import Queue

def GetURL():
    url = ""
    for year in range(2007,2011):#年份
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
        url = 'http://news.people.com.cn/GB/28053/review/20110104.html'
        page = urllib.request.urlopen(url).read().decode('gbk','ignore')
        html=etree.HTML(page)
        tablenum=html.xpath('/html/body/center/table')
        if len(tablenum)==3:
            #20070101 类似网页只有3个table的
            str0='//table[1]//tr[1]/td[2]/table[3]//tr[2]//a/@href'
            str1='//table[1]//tr[1]/td[2]/table[3]//tr['
            str2=']/td['
            str3=']/table[2]//a/@href'
            str4='//table[1]//tr[1]/td[2]/table[3]//tr['
            str5=']/table[1]//td[2]/text()'
        else:
            # 20170101 类似网页有5个table的
            str0 = '//table[5]/tr[1]/td[2]/table[2]//td[2]//a/@href'
            #str1 = '//table[5]//table[4]//tr['
            str1='//table[5]//tr[1]/td[2]/table[3]//tr['
            str2 = ']/td['
            str3 = ']/table[2]//a/@href'
            #str4 = '//table[5]//table[4]//tr['
            str4='//table[5]//tr[1]/td[2]/table[3]//tr['
            str5 = ']/table[1]//td[2]/text()'

        if len(html.xpath(str0))==0:
            str0='//table[5]//tr[1]/td[2]/table[3]//td[2]//a/@href'
            str1='//table[5]//tr[1]/td[2]/table[4]//tr['
            str4='//table[5]//tr[1]/td[2]/table[4]//tr['

        title1=[]
        title2=[]
        for i in range(1,16):
            try:
                if len(html.xpath(str4+str(i)+str2+'1'+str5))!=0:
                    title1.append(''.join(html.xpath(str4+str(i)+str2+'1'+str5)[0].split()))  # 标题 去空格
                    title2.append(''.join(html.xpath(str4+str(i)+str2+'2'+str5)[0].split()))  # 标题 去空格
            except Exception as e:
                print(e)

        text='旅游'
        index=1
        for i in title1:
            if i==text:
                try:
                    nvxing=html.xpath(str1+str(index)+str2+'1'+str3)
                    Write(nvxing,i)
                    print("su")
                    break
                except Exception as e:
                    print(e)
            else:
                index+=1

        index=1
        for i in title2:
            if i==text:
                try:
                    nvxing=html.xpath(str1+str(index)+str2+'1'+str3)
                    Write(nvxing,i)
                    print("su")
                    break
                except Exception as e:
                    print(e)
            else:
                index+=1

    except BaseException as e:
        print(url)
        print(e)

def Write(strlist,filename):
    if filename!='':
        str=""
        f=open(os.path.join(sys.path[0]+'/URL',filename+'.txt'),'a')
        for i in strlist:
            str=str+i+'\n'
        f.write(str)
        f.close()


if __name__=='__main__':
    GetURL()
