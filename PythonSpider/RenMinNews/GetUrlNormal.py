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
        #url="http://news.people.com.cn/GB/28053/review/20070911.html"
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
        try:
            MeiRiPaiHang=html.xpath(str0)
            Write(MeiRiPaiHang,'每日排行')
            ShiZheng    = html.xpath(str1+'1'+str2+'1'+str3) #以下的tr是一行，td是竖着，table是内分页
            GongChanDang= html.xpath(str1+'1'+str2+'2'+str3)
            name1 = ''.join(html.xpath(str4+'1'+str2+'1'+str5)[0].split())  # 标题 去空格
            name2 = ''.join(html.xpath(str4+'1'+str2+'2'+str5)[0].split())
            Write(ShiZheng,name1)
            Write(GongChanDang,name2)
        except Exception as e:
            print(e)

        try:
            GuanDian    = html.xpath(str1+'2'+str2+'1'+str3)
            LiLun       = html.xpath(str1+'2'+str2+'2'+str3)
            name1 = ''.join(html.xpath(str4 + '2' + str2 + '1' + str5)[0].split())  # 标题 去空格
            name2 = ''.join(html.xpath(str4 + '2' + str2 + '2' + str5)[0].split())
            Write(GuanDian,name1)
            Write(LiLun,name2)
        except Exception as e:
            print(e)

        try:
            GuoJi       = html.xpath(str1+'3'+str2+'1'+str3)
            JingJi      = html.xpath(str1+'3'+str2+'2'+str3)
            name1 = ''.join(html.xpath(str4 + '3' + str2 + '1' + str5)[0].split())  # 标题 去空格
            name2 = ''.join(html.xpath(str4 + '3' + str2 + '2' + str5)[0].split())
            Write(GuoJi,name1)
            Write(JingJi,name2)
        except Exception as e:
            print(e)

        try:
            JunShi      = html.xpath(str1+'4'+str2+'1'+str3)
            JiaoYu      = html.xpath(str1+'4'+str2+'2'+str3)
            name1 = ''.join(html.xpath(str4 + '4' + str2 + '1' + str5)[0].split())  # 标题 去空格
            name2 = ''.join(html.xpath(str4 + '4' + str2 + '2' + str5)[0].split())
            Write(JunShi,name1)
            Write(JiaoYu,name2)
        except Exception as e:
            print(e)

        try:
            IT          = html.xpath(str1+'5'+str2+'1'+str3)
            KeJi        = html.xpath(str1+'5'+str2+'2'+str3)
            name1 = ''.join(html.xpath(str4 + '5' + str2 + '1' + str5)[0].split())  # 标题 去空格
            name2 = ''.join(html.xpath(str4 + '5' + str2 + '2' + str5)[0].split())
            Write(IT,name1)
            Write(KeJi,name2)
        except Exception as e:
            print(e)

        try:
            WenHua      = html.xpath(str1+'6'+str2+'1'+str3)
            YuLe        = html.xpath(str1+'6'+str2+'2'+str3)
            name1 = ''.join(html.xpath(str4 + '6' + str2 + '1' + str5)[0].split())  # 标题 去空格
            name2 = ''.join(html.xpath(str4 + '6' + str2 + '2' + str5)[0].split())
            Write(WenHua,name1)
            Write(YuLe,name2)
        except Exception as e:
            print(e)

        try:
            HaiXiaLiangAn= html.xpath(str1+'7'+str2+'1'+str3)
            GangAo      = html.xpath(str1+'7'+str2+'2'+str3)
            name1 = ''.join(html.xpath(str4 + '7' + str2 + '1' + str5)[0].split())  # 标题 去空格
            name2 = ''.join(html.xpath(str4 + '7' + str2 + '2' + str5)[0].split())
            Write(HaiXiaLiangAn,name1)
            Write(GangAo,name2)
        except Exception as e:
            print(e)

        try:
            RenDaXinWen = html.xpath(str1+'8'+str2+'1'+str3)
            ZhongGuoZhengFu= html.xpath(str1+'8'+str2+'2'+str3)
            name1 = ''.join(html.xpath(str4 + '8' + str2 + '1' + str5)[0].split())  # 标题 去空格
            name2 = ''.join(html.xpath(str4 + '8' + str2 + '2' + str5)[0].split())
            Write(RenDaXinWen,name1)
            Write(ZhongGuoZhengFu,name2)
        except Exception as e:
            print(e)

        try:
            HuanBao     = html.xpath(str1+'9'+str2+'1'+str3)
            LvYou       = html.xpath(str1+'9'+str2+'2'+str3)
            name1 = ''.join(html.xpath(str4 + '9' + str2 + '1' + str5)[0].split())  # 标题 去空格
            name2 = ''.join(html.xpath(str4 + '9' + str2 + '2' + str5)[0].split())
            Write(HuanBao,name1)
            Write(LvYou,name2)
        except Exception as e:
            print(e)

        try:
            NvXing      = html.xpath(str1+'10'+str2+'1'+str3)
            JianKang    = html.xpath(str1+'10'+str2+'2'+str3)
            name1 = ''.join(html.xpath(str4 + '10' + str2 + '1' + str5)[0].split())  # 标题 去空格
            name2 = ''.join(html.xpath(str4 + '10' + str2 + '2' + str5)[0].split())
            Write(NvXing,name1)
            Write(JianKang,name2)
        except Exception as e:
            print(e)

        try:
            FangChan    = html.xpath(str1+'11'+str2+'1'+str3)
            QiChe       =html.xpath(str1+'11'+str2+'2'+str3)
            name1 = ''.join(html.xpath(str4 + '11' + str2 + '1' + str5)[0].split())  # 标题 去空格
            name2 = ''.join(html.xpath(str4 + '11' + str2 + '2' + str5)[0].split())  # 标题 去空格
            Write(FangChan,name1)
            Write(QiChe, name2)
        except Exception as e:
            print(e)

        try:
            SheHui      = html.xpath(str1+'12'+str2+'1'+str3)
            ChuanMei    = html.xpath(str1+'12'+str2+'2'+str3)
            name1 = ''.join(html.xpath(str4 + '12' + str2 + '1' + str5)[0].split())  # 标题 去空格
            name2 = ''.join(html.xpath(str4 + '12' + str2 + '2' + str5)[0].split())
            Write(SheHui,name1)
            Write(ChuanMei,name2)
        except Exception as e:
            print(e)

        try:
            RenMinKuanPin = html.xpath(str1+'13'+str2+'1'+str3)
            TiYu        = html.xpath(str1+'13'+str2+'2'+str3)
            name1 = ''.join(html.xpath(str4 + '13' + str2 + '1' + str5)[0].split())  # 标题 去空格
            name2 = ''.join(html.xpath(str4 + '13' + str2 + '2' + str5)[0].split())
            Write(RenMinKuanPin,name1)
            Write(TiYu,name2)
        except Exception as e:
            print(e)

        #有的网页只有13页，所以，需要判断是不是第14个为空
        try:
            NanShi      = html.xpath(str1+'14'+str2+'1'+str3)
            ZhongGuoYangQiXinWen = html.xpath(str1+'14'+str2+'2'+str3)
            if len(NanShi)!=0:
                name1 = ''.join(html.xpath(str4 + '14' + str2 + '1' + str5)[0].split())  # 标题 去空格
                Write(NanShi, name1)
            if len(ZhongGuoYangQiXinWen)!=0:
                name2 = ''.join(html.xpath(str4 + '14' + str2 + '2' + str5)[0].split())
                Write(ZhongGuoYangQiXinWen,name2)
        except Exception as e:
            print(e)
        print("success")

    except BaseException as e:
        f=open(os.path.join(sys.path[0],'错误网页.txt'),'a')
        f.write(url+'\n')
        f.close()
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
