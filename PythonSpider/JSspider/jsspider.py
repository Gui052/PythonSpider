import os
import re
import sys
import time
from queue import Queue

import execjs
import requests
from bs4 import BeautifulSoup as BS

import json

bookids = Queue()
booknames = Queue()

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'}
session = requests.Session()
# 预先读取mainjs数据，减少文件读取系统占用
textjs = ""
mainjs = open(os.path.join(sys.path[0], 'mainjs.txt'), 'r')
textlist = mainjs.readlines()
for i in textlist:
    textjs = textjs + i
mainjs.close()

# 读取cookie
cookieFile = os.path.join(sys.path[0], "cookies")
if os.path.exists(cookieFile):
    with open(cookieFile, 'r') as f:
        try:
            cookies = json.load(f)
        except BaseException:
            cookies = None
    f.close()


def pagenumber(id):
    '''获取书的总页数'''
    global cookies
    try:
        url = 'http://read.ccpph.com.cn/Service/?logic=PDFReaderController&call=readPDF&bookid=' + \
            id + '&page=1&html=selectText_NOINC&from=online&searchChar=undefined'
        session.cookies.update(cookies)
        session.headers = headers
        html = session.get(url)
        htmldetial = html.content.decode()
        allpage = re.findall('"pages":\d+', htmldetial)
        s = allpage[0].split(':')
        return int(s[1])
    except BaseException:
        time.sleep(2000)  # 如果获取失败是因为人数满了，需要休眠30分钟
        cookies = getcookie()  # 重新获取cookie
        return pagenumber(id)  # 重新获取页数


def getcookie():
    '''获取cookie并保存'''
    url1 = 'http://read.ccpph.com.cn/Service/?logic=PDFReaderController&call=readPDF&bookid=B_01016705_002&page=1&html=selectText_NOINC&from=online&searchChar=undefined'
    session.headers = headers
    session.get(url1)
    with open(cookieFile, 'w') as f:
        cookies = session.cookies.get_dict()
        json.dump(cookies, f)
        f.close()
    return cookies


def loadcookie():
    '''读取cookie'''
    if os.path.exists(cookieFile):
        with open(cookieFile, 'r') as f:
            try:
                cookie = json.load(f)
                return cookie
            except BaseException:
                return None
    return None


def writejs(bookid, number):
    '''构造运行的js'''
    global textjs
    global cookies
    url1 = 'http://read.ccpph.com.cn/Service/?logic=PDFReaderController&call=getJS&jsurl=' + \
        bookid + '(' + str(number) + ').js'
    session.cookies.update(cookies)
    session.headers = headers
    html = session.get(url1)
    soup = BS(html.content, 'html.parser')
    functionjs = 'function str(){' + str(soup) + str(textjs) + '}'  # 构造js函数
    return functionjs


def run():
    order = 1
    while bookids.empty() == 0:
        number = 1
        bookid = bookids.get()  # 获取ID
        bookname = booknames.get() + '.txt'  # 获取书名
        bookname.replace('\\','')
        f = open(
            os.path.join(
                sys.path[0] +
                '/Thirteen',
                'No:' +
                str(order) +
                '--' +
                bookname),
            'a')  # 打开书名文件
        finalnumber = pagenumber(bookid)  # 获取书的总页数
        bookstr = ""  # 500页字符串
        pagenumtemp = 0  # 记录每500页写入
        print(bookname + bookid)
        while number <= finalnumber:
            jsstr = writejs(bookid, number)
            try:
                ctx = execjs.compile(jsstr) #运行js代码并执行返回
                final_result = ctx.call('str')
                bookstr = bookstr + final_result + '\n'
                pagenumtemp = pagenumtemp + 1
                if pagenumtemp == 500:
                    f.write(bookstr + '\n')
                    pagenumtemp = 0
                    bookstr = ""  # 清空
            except BaseException:  # 导致错误的时候写入，以便人工检查
                f.write(
                    bookstr +
                    "\n\n\n\n\n此处出现错误，请参看源代码:页码" +
                    str(number) +
                    '\n\n\n\n\n')
                error = open(os.path.join(sys.path[0], 'error.txt'), 'a')
                error.write(bookname + ':页码数:' + str(number) + '\n\n\n\n\n')
                error.close()
                pagenumtemp = 0
                bookstr = ""
            print('成功导入' + str(number) + '页')
            number = number + 1
            # time.sleep(0.5)  # 休眠时间
        f.write(bookstr + '\n')  # 防止书本不到500页没有被写入
        log(bookid, bookname)  # 写入日志
        f.close()
        order = order + 1
        #清空控制台
        if os.name == 'posix':
            os.system('clear')
        elif os.name == 'nt':
            os.system('cls')


def getbookid():
    '''获取书的id'''
    allId = open(os.path.join(sys.path[0], 'bookid.txt'), 'r')
    bookID = allId.readlines()
    for id in bookID:
        if id[len(id) - 1] == '\n':
            bookids.put(id[:-1])
        else:
            bookids.put(id)
    allId.close()


def getbookname():
    '''获取书名，用于命名'''
    allname = open(os.path.join(sys.path[0], 'bookname.txt'), 'r')
    bookname = allname.readlines()
    for name in bookname:
        if name[len(name) - 1] == '\n':
            booknames.put(name[:-1])
        else:
            booknames.put(name)
    allname.close()


def log(bookid, bookname):
    '''日志记录'''
    logfile = open(os.path.join(sys.path[0], 'log.txt'), 'a')  # 写入日志
    logfile.write(str(time.asctime()) + ':' + bookid + ':' + bookname + '\n')
    logfile.close()


if __name__ == '__main__':
    getbookid()
    getbookname()
    if cookies:
        print('已经获取cookie')
    else:
        print('正在获取cookie')
        cookies = getcookie()
        print('成功获取cookie')
    run()
