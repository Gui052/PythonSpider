# -*- coding: utf-8 -*-
from urllib import request
from lxml import etree
from selenium import webdriver
import time
import os
import json
import requests

class get_urls_zhongkao:
    def __init__(self):
        if os.path.exists('cookie') == 0:
            print("没有cookie文件，即将调用浏览器登录")
            browser = webdriver.Chrome()
            browser.get('http://www.jyeoo.com/')  # 调用浏览器打开登录界面
            browser.implicitly_wait(10)
            time.sleep(40)
            cookie = browser.get_cookies()

            with open('cookie', "w") as output:
                json.dump(cookie, output)
                print("=" * 50)
                print("已在同目录下生成cookie文件：")
            browser.quit()

        if os.path.exists('cookie'):
            with open('cookie', "r") as f:
                self.cookie = json.load(f)
                print("载入cookie")

    def get_grade_zhongkao(self,continueIndex=0):
        # 年份
        yearNoText=['2018','2017','2016','2015','2014','2013','2012','2011','2010',
                    '2009','2008','2007','2006','2005','2004','其他年份']
        for yearNo in range(17):
            url1='http://www.jyeoo.com/math/report/search?pa=1&pb={0}&po=3&pd=1'.format(yearNo)
            html = request.urlopen(url1).read().decode('utf8')
            numsource=etree.HTML(html)
            num=numsource.xpath('//dl[@class="Navtree"]//a/@href')
            select=numsource.xpath('//dl[@class="Navtree"]//a/text()')

            # 左边选项
            i = continueIndex
            while i<len(num):
                while 1:
                    page=0
                    urls='http://www.jyeoo.com/'+num[i]+'&p={0}'.format(page)
                    html=self.url_request(urls)
                    print("当前完成--"+yearNoText[i]+"--"+select[i]+"--参数为"+str(i))
                    next=self.xpath_analysis(html)
                    if next==1:
                        page+=1
                    elif next==0:
                        break
                    else:
                        print("达到访问限制，请更换账号")
                        return 0
                i += 1

    def url_request(self,url):
            cookies = {}
            for i in self.cookie:
                name = i['name']
                value = i['value']
                cookies[name] = value
            headers = {
                'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'}
            session = requests.Session()
            session.headers = headers
            session.cookies.update(cookies)
            html = session.get(url)
            htmldetial = html.content.decode()
            return htmldetial


    def xpath_analysis(self,html):
        yearsource = etree.HTML(html)
        years = yearsource.xpath('//table[@class="report-tab"]/tr/td[2]/a/@href')
        title = yearsource.xpath('//table[@class="report-tab"]/tr/td[2]/a/text()')
        if len(years)!=0:
            isContinue = self.get_page_detail(years,title)
            if isContinue==0:
                return 2
            return 1
        else:
            return 0

    def get_page_detail(self,urls,title):
        # 网页编码更改
        for i in range(len(urls)):
            html=request.urlopen(urls[i]).read().decode('utf8')
            page=etree.HTML(html)
            thistitle=page.xpath('//*[@id="pchube"]/div[2]/div[1]/h1/text()')
            if thistitle!=title[i]: # 达到访问限制
                return 0
            sub=page.xpath('//*[@class="quesborder"]')
            for i in sub:
                subject=etree.tostring(i,encoding='utf8',method='html').decode('utf8')
                print(subject)
        return 1


if __name__ == '__main__':
    g=get_urls_zhongkao()
    g.get_grade_zhongkao()



























