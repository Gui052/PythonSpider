from lxml import etree
import re
import sys
import os
import hashlib
import pymysql
import json
import random
from urllib import request
import time
from queue import Queue

def process_stem(stem,Is_option=False):
    stem=stem.replace('</td></tr><tr><td>','/')#替换为除号
    stem=stem.replace('<sup>','**')  #
    stem = stem.replace('&nbsp;', '')
    #stem = stem.replace('&nbsp;', '')
    stem=stem.replace('\r\n','**')
    fill_blank=re.findall('(<div class="sanwser">.*?</div>)',stem)
    for blank in fill_blank:
        stem=stem.replace(blank,'')
    stem=re.findall('>(.*?)<',stem)
    question_item=''
    if Is_option==False:
        for i in range(len(stem)):
            question_item+=stem[i]
    else:
        for i in range(len(stem)):
            question_item+=stem[i]+" "
    return question_item
def insert_to_database(db,lists,sql):
    cursor = db.cursor()
    try:
        cursor.executemany(sql,lists)
        # print(cursor.rowcount) # 输出实际插入数量
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
def select_from_database(db,sql):
    cursor=db.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

if __name__ == '__main__':
    with open(os.path.join(sys.path[0], 'connectDB.json'), 'r', encoding='utf8') as f:
        profile = json.load(f)
    with open(os.path.join(sys.path[0], 'IP.txt'), 'r', encoding='utf8') as f:
        IP=f.readlines()
        IPList=Queue()
        for i in IP:
            if i[-1] == '\n':
                IPList.put(i[:-1])
            else:
                IPList.put(i)


    db = pymysql.connect(host=profile['host'], port=profile['port'],
                              user=profile['user'], passwd=profile['passwd'],
                              db=profile['database'], charset='utf8')
    print('连接数据库成功')
    urllists=['http://www.jyeoo.com/math/report/detail/bbdbb109-015b-4915-a54d-e6325eb36ad0',
              'http://www.jyeoo.com/math/report/detail/170c10a7-5150-4315-531f-18f525e5ee6c',
              'http://www.jyeoo.com/math/report/detail/d521021d-1515-15f8-9b5b-25bc7418e0d6',
              'http://www.jyeoo.com/math/report/detail/ee103dde-8315-4151-51f3-32b113c2519a',
              'http://www.jyeoo.com/math/report/detail/ca51033f-15a6-4515-5306-7a259c9ddf75',
              'http://www.jyeoo.com/math/report/detail/f258110d-b156-152a-ae54-cc2551c145d1',
              'http://www.jyeoo.com/math/report/detail/56c107e1-15fd-4915-9567-425d0283d725',
              'http://www.jyeoo.com/math/report/detail/13361013-1158-152f-5480-95ace310b25c'
              ]
    seconds=0
    # 这是代理IP
    ip=IPList.get()
    while IPList.empty() == 0: #IPList.empty()返回false
        seconds +=1
        index=random.randint(0,7)
        ##设置ｉｐ代理
        # 访问网址
        url = urllists[index]
        # 设置代理ip访问方式，http和https
        proxy = {'http': ip, 'https': ip}
        # 创建ProxyHandler
        proxy_support = request.ProxyHandler(proxy)
        # 创建Opener
        opener = request.build_opener(proxy_support)
        # 添加User Angent
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0')]
        # 安装OPener
        request.install_opener(opener)
        # 使用自己安装好的Opener
        try:
            response = request.urlopen(url,timeout=10) # 设置10秒
        except Exception as e:
            print(e)
            continue
        finally:
            ip = IPList.get()

        # 读取相应信息并解码
        html = response.read().decode("utf-8")
        text=etree.HTML(html)
        # 试卷标题，以及一些信息。
        titletemp=text.xpath('//*[@id="pchube"]//h1/text()')
        # 如果试卷没有标题就直接不管
        if len(titletemp)>=1:
            title=titletemp[0]
            score=text.xpath('//*[@id="pchube"]/div[2]/div[1]/div[3]/text()')

            thisMD5 = hashlib.md5(title.encode('utf-8')).hexdigest()
            sql = "SELECT MD5 FROM testpaper WHERE MD5= '"+thisMD5+"'"
            # 用于检测是否有重复
            MD5 = select_from_database(db, sql)

            if len(MD5)==0:
                divnum=len(text.xpath('//*[@id="pchube"]/div[2]/div[2]/div')) # 寻找到div的数量

                subjectList=[[] for i in range(divnum-1)]
                titleList=[[] for i in range(divnum-1)]
                infoList=[[] for i in range(divnum-1)]


                for i in range(1,divnum):
                    subjectTitle = text.xpath('//*[@id="pchube"]/div[2]/div[2]/h3[{0}]/text()'.format(i))
                    subjectText = text.xpath('//div[@class="rpt_b"]/div[{0}]//div[@class="pt1"]'.format(i))
                    subjectInfo = text.xpath('//div[@class="rpt_b"]/div[{0}]/span'.format(i))
                    # 题目列表
                    subjectList[i-1] = subjectText
                    # 大题列表
                    titleList[i-1] = subjectTitle
                    # 题目信息列表
                    infoList[i-1] = subjectInfo

                insertList=[]
                for i in range(divnum-1):
                    for j in range(len(subjectList[i])):
                        if len(subjectList[i])==len(infoList[i]): #防止两个列表不一样报错
                            subtext= process_stem(etree.tostring(subjectList[i][j],encoding='unicode'))
                            subinfo=re.findall('<em style="color:red">(.*?)</em>',etree.tostring(infoList[i][j],encoding='unicode'))
                            # subinfo按照 难度，真题，组卷进行排列的
                            subLink=infoList[i][j].xpath('a[1]/@href')
                            # 题目，难度，真题，组卷，链接，试卷名称
                            insertList.append([titleList[i],subtext,subinfo[0],subinfo[1],subinfo[2],subLink[0],title])

                testpaperinsert=[thisMD5,
                                 title,
                                 score[0].split('：')[1],
                                 score[1].split('：')[1],
                                 score[2].split('：')[1],
                                 score[3].split('：')[1]]
                sql1 = "insert into Radom (`类型`,`题目`,`难度`,`真题`,`组卷`,`链接`,`试卷名称`) values(%s,%s,%s,%s,%s,%s,%s)"
                insert_to_database(db,insertList,sql1)

                sql2 = "insert into testpaper (`MD5`,`名称`,`总分`,`难度`,`浏览`,`下载`) values(%s,%s,%s,%s,%s,%s)"
                insert_to_database(db, [testpaperinsert], sql2)
            else:
                print('试卷已存在')
        else:
            print('无标题试卷')

        print(seconds)
        time.sleep(round(random.uniform(1, 2), 3))
