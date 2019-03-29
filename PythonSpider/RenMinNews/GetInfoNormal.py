import sys
import os
from urllib import request
from lxml import etree
from queue import Queue
import re

URL=Queue()
filename=[]
Error=open(os.path.join(sys.path[0],'error.txt'),'a')

#创建文件夹以及读取目录下文件
def readfilename():
    global filename
    path=os.path.join(sys.path[0])
    filename=os.listdir(path+'/URL')
    for i in filename:
        dirname=i.split('.')[0]
        haveDir=os.path.exists(path+'/'+dirname)
        if not haveDir:
            os.makedirs(path+'/'+dirname)

#读取文件
def readurl(FileName):
    url=open(os.path.join(sys.path[0]+'/URL',FileName),'r')
    urltext=url.readlines()
    for i in urltext:
        if i[len(i) - 1] == '\n':
            URL.put(i[:-1])
        else:
            URL.put(i)
    url.close()

#----------写入文件------------------------------------------------
def writefile(title,Date,text,DirName):
    '''写文件'''
    Title=title[0].replace('\t', '').replace('\n', '').replace(' ', '')

    Text=Title+'\n'
    for i in text:
        tem=i.replace('\t','').replace('\n','').replace('\r','').replace(' ','')
        tem=re.sub('[A-Za-z\[\`\@\#\$\^\&\*\(\)\=\|\{\}\]\<\>\/\'\+\~\\\%]', '', tem)
        if len(tem)!=0:
            Text = Text +tem+'\n'

    file = open(os.path.join(sys.path[0]+'/'+DirName, Date[0]+'.txt'), 'a')
    file.write(Text)
    file.close()
    print("success")
#-----------------------------------------------------------------

def getinfo(FileName):
    while URL.empty() == 0:
        try:
            url=URL.get()
            html=request.urlopen(url).read().decode('gbk','ignore')
            code = etree.HTML(html)
            DirName=FileName.split('.')[0]
            date = re.findall('\d{4}年\d{1,2}月\d{1,2}日\d{2}:\d{2}', html) #日期都一样，所以使用正则表达式
            if len(date)==0: #如果找不到日期直接结束
                continue
            #society社会  opinion观点  world国际  finance经济  military军事
            #edu教育  itIT  scitech科技  culture文化
            title=code.xpath('//*[@id="p_title"]//text()')
            if len(title)!=0:
                text=code.xpath('//*[@id="p_content"]//text()')
                if len(text)==0:
                    text=code.xpath('//*[@class="c3"]//text()')
                writefile(title,date,text,DirName)
                continue
            #politics时政
            title = code.xpath('//h1//text()')
            if len(title)!=0:
                text=code.xpath('//font[@id="zoom"]//text()')
                writefile(title, date, text, DirName)
                continue
            #cpc共产党新闻  theory理论（前面的子网）
            title=code.xpath('//*[@class="ftitle"]//text()')
            if len(title)!=0:
                text=code.xpath('//*[@class="fbody"]//text()')
                writefile(title, date, text, DirName)
                continue
            #cpc 时政热点
            title=code.xpath('//*[@class="twbcbt18"]//text()')
            if len(title)!=0:
                text=code.xpath('//*[@class="fbody"]//text()')
                writefile(title, date, text, DirName)
                continue
            #finance 快讯
            title=code.xpath('//table[3]//font[1]/div/font/b/text()')
            if len(title)!=0:
                text=code.xpath('//table[3]//td//text()')
                writefile(title, date, text, DirName)
                continue
            #finance 评论观察
            title=code.xpath('//*[@id="table142"]//tr[1]/td/p/font[2]/text()')
            if len(title)!=0:
                text=code.xpath('//*[@id="table142"]//tr[2]//text()')
                writefile(title, date, text, DirName)
                continue
            #finance 理论观察
            title = code.xpath('//*[@id="table1"]//tr[1]/td[2]/p/b/font/text()')
            if len(title) != 0:
                text = code.xpath('//*[@id="table1"]//text()')
                writefile(title, date, text, DirName)
                continue
            title=code.xpath('//*[@id="table1"]//tr[1]/td/div/text()')
            if len(title)!=0:
                text=code.xpath('//*[@id="table1"]//text()')
                writefile(title, date, text, DirName)
                continue
            #finance 理财
            title=code.xpath('//*[@id="table8"]//tr[1]/td/p/i/font[1]/text()')
            if len(title)!=0:
                text=code.xpath('//*[@id="table1"]//text()')
                writefile(title, date, text, DirName)
                continue
            #没有标题的情况
            text=code.xpath('//table[3]//text()')
            if len(text)!=0:
                writefile([''], date, text,DirName)
                continue
            Error.write(url+'\n') #输出没有找到的网页
        except BaseException as e:
            print(e)

if __name__ == '__main__':
    readfilename()
    f=open(os.path.join(sys.path[0],'LOG.txt'),'a')
    for name in filename:
        f.write(name)
        readurl(name)
        getinfo(name)
        if os.name == 'posix':
            os.system('clear')
        elif os.name == 'nt':
            os.system('cls')
    f.close()
    Error.close()

