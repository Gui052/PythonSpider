# -*- coding: utf-8 -*-
'''
    >  Filename : get_detial_urls
    >  Author   : lan
        __
       /\ \
       \ \ \            __       ___
        \ \ \         /'__'\ /\/' _'\
         \ \ \__ __  /\/  \ \\/\ \/\ \
          \ \__  _ _\\ \ __\ \\ \_\ \_\
           \/__ __ _/ \/__ /_'/\/_/\/_/
    >  Date     : 18/03/13 - 15:00
'''
from urllib import request
from lxml import etree
import pymysql
import random
import re
import hashlib
import requests
import time
import sys
import os
import json
from selenium import webdriver
from queue import Queue

class get_url:
    pageNumber=0
    sec=0
    def __init__(self):
        with open(os.path.join(sys.path[0],'connectDB.json'), 'r',encoding='utf8') as f:
            profile = json.load(f)
        self.db = pymysql.connect(host=profile['host'], port=profile['port'],
                             user=profile['user'], passwd=profile['passwd'],
                             db=profile['database'], charset='utf8')
        print('连接数据库成功')
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

        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'}
        self.session = requests.Session()
        self.session.headers = headers

    def __del__(self):
        self.db.close()
        print('数据库关闭')

    def get_urls(self,q,ct,dg,fg,so,pi,f='1',po='0'):
        '''
        获取详细解答的链接
        参数含义是：
        知识点（q=pk）
        题型（ct）
        难度（dg）
        题类（fg）
        来源（so）
        页数（pi）
        检索方式(f=1按考点，f=0按章节)
        排序（po=0综合排序）
        :return:链接队列
        '''
        result=[]
        lbs = ''
        pd = '1'
        so2 = '0'
        url = 'http://www.jyeoo.com/math/ques/partialques?q=' + q + '&f=' + f
        url += '&ct=' + ct
        url += '&dg=' + dg
        url += '&fg=' + fg
        url += '&po=' + po
        url += '&pd=' + pd
        url += '&pi=' + str(pi)
        url += '&lbs=' + lbs
        url += '&so=' + so
        url += '&so2=' + so2
        url += '&r=' +str(random.uniform(0,1))

        print("请求网址为："+url)
        htmltext = self.url_request(url)
        text = etree.HTML(htmltext)

        # pageNumText=text.xpath('//*[@id="pchube"]/text()')
        pageNumText = re.findall('共计<.*?>(\d+)</em>道相关试题',htmltext)
        if len(pageNumText)!=0:
            self.pageNumber=int(pageNumText[0])/10
        else:
            self.pageNumber=0 # 如果没有页码就需要重置了
        urls = text.xpath('//li[@class="QUES_LI"]/span[1]/a[1]/@href')
        result.extend(urls)
        return result

    def url_request(self,url):
        '''
        网页请求函数
        :param url:
        :return:
        '''
        cookies = {}
        for i in self.cookie:
            name = i['name']
            value = i['value']
            cookies[name] = value

        # if self.sec >= 20:
            # self.session.cookies.clear()
        self.session.cookies.update(cookies) # 测试是否需要cookie
        html = self.session.get(url)
        htmldetial = html.content.decode()
        return htmldetial

    def insert_to_database(self,urls,sql):
        '''
        插入数据
        :param db:数据库实例
        :param urls:数据列表
        :param table:数据表
        '''
        cursor = self.db.cursor()

        try:
            cursor.executemany(sql,urls)
            print(cursor.rowcount)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    def get_node(self,url):
        '''获取知识点节点标号'''
        # gr.get_node('http://www.jyeoo.com/math/ques/partialcategory?a=undefined&q=1~1~11&f=1&r=0.7803788482896095')
        html=request.urlopen(url).read().decode('utf8')
        text=etree.HTML(html)
        node=text.xpath('//a[@onclick="nodeClick(this,2)"]/..')
        nodes=""
        for i in node:
            temp1=i.xpath('a/@pk')[0]
            # temp2=i.xpath('a/text()')[0]
            nodes+=temp1+'\n'
        with open(os.path.join(sys.path[0],'Point.txt'), 'w',encoding='utf8') as f:
            f.write(nodes)

    def load_files(self,filename):
        '''加载配置文件'''
        with open(os.path.join(sys.path[0],filename), 'r',encoding='utf8') as f:
            profile = json.load(f)
        return profile

def start(iq=0,ict=0,idg=0,ifg=0,iso=0):
    '''
    参数的意义是，防止中途出现错误，重新开始之后，需要手动调整参数
    :param iq:知识点
    :param ict:题型
    :param idg:难度
    :param ifg:题类
    :param iso:来源
    :return:
    '''
    gr = get_url()
    pfile = gr.load_files('Param.json')
    Q = []
    with open(os.path.join(sys.path[0], 'Point.txt'), 'r', encoding='utf8') as f:
        pk = f.readlines()
    for i in pk:
        Q.append(i[:-1])

    Ct = ['选择题', '填空题', '解答题']
    Dg = ['基础题', '中档题', '难题']
    Fg = ['常考题', '易错题', '好题', '压轴题']
    So = ['中考真题', '自主招生', '中考模拟', '中考复习', '期末试题', '期中考试', '月考试题',
          '单元测验', '同步练习', '竞赛试题', '假期作业']

    continuesNum = 0

    while iq<len(Q):
        q=Q[iq]
        iq +=1
        while ict<len(Ct):
            ct=Ct[ict]
            ict +=1
            while idg<len(Dg):
                dg=Dg[idg]
                idg +=1
                while ifg<len(Fg):
                    fg=Fg[ifg]
                    ifg +=1
                    while iso<len(So):
                        so=So[iso]
                        iso +=1
                        pi=0
                        while pi <= gr.pageNumber:
                            pi += 1
                            Insert=[]
                            print(str(iq-1) + "->" + str(ict-1) + "->" + str(idg-1) + "->" + str(ifg-1) +
                                  "->" + str(iso-1) + "->" + str(pi) + "页")
                            urls = gr.get_urls(q, pfile[ct], pfile[dg], pfile[fg], pfile[so], pi)
                            print(urls)
                            if len(urls)!=0:
                                for OneUrl in urls:
                                    temp=[hashlib.md5(OneUrl.encode('utf-8')).hexdigest(),
                                                OneUrl,ct,dg,fg,so]
                                    Insert.append(temp)
                                sql = "insert into links (`MD5`,`链接`,`题型`,`难度`,`题类`,`来源`) values(%s,%s,%s,%s,%s,%s)"
                                gr.insert_to_database(Insert, sql)
                            time.sleep(round(random.uniform(1, 3), 3))
                            # 清除cookie计数
                            if gr.sec<=20:
                                gr.sec +=1
                            else:
                                gr.sec=0
                    iso = 0
                ifg = 0
            idg = 0
        ict = 0

if __name__ == '__main__':
    start()
































