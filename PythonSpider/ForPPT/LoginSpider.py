# -*- coding: utf-8 -*-
'''
    >  Filename : py
    >  Author   :
        __
       /\ \
       \ \ \            __       ___
        \ \ \         /'__'\ /\/' _'\
         \ \ \__ __  /\/  \ \\/\ \/\ \
          \ \__  _ _\\ \ __\ \\ \_\ \_\
           \/__ __ _/ \/__ /_'/\/_/\/_/
    >  Date     : 17/11/13 - 15:46
'''
from selenium import webdriver
import time
import os
import json
import requests

if os.path.exists('cookie')==0:
    browser=webdriver.Chrome()
    browser.get('https://www.zhihu.com/#signin')#调用浏览器打开登录界面
    browser.implicitly_wait(10)
    time.sleep(20)
    cookie=browser.get_cookies()

    with open('cookie', "w") as output:
        json.dump(cookie, output)
        print("=" * 50)
        print("已在同目录下生成cookie文件：")
    browser.quit()

if os.path.exists('cookie'):
    with open('cookie', "r") as f:
        cookie = json.load(f)

    browser=webdriver.Chrome()
    browser.get('https://www.zhihu.com/')
    for i in cookie:
        browser.add_cookie(i)
    browser.refresh()
    time.sleep(10)
    browser.quit()

    cookies={}
    for i in cookie:
        name=i['name']
        value=i['value']
        cookies[name]=value
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'}
    session = requests.Session()
    session.headers = headers
    session.cookies.update(cookies)
    html = session.get('https://www.zhihu.com/#signin')
    htmldetial = html.content.decode()
    print(htmldetial)



