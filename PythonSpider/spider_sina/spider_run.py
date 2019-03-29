'''
Created on 2017年7月15日

@author: aaron
'''
import base64
import hashlib
import os
import re
import sys
import urllib

import requests
from bs4 import BeautifulSoup as BS

from JSspider import json


class SinaClient:
    headers={ 'use_agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/59.0.3071.109 Chrome/59.0.3071.109 Safari/537.36',
                 'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                 'accept-encoding':'gzip, deflate, br',
            }
    homeURL = r"http://www.weibo.com/"
    cookieFile = os.path.join(sys.path[0], "cookie")
    def __init__(self):
        global a
        os.chdir(sys.path[0])  # 设置脚本所在目录为当前工作目录
        self.__session = requests.Session()
        self.__session.headers = self.headers  # 用self调用类变量是防止将来类改名
        # 若已经有 cookie 则直接登录
        self.__cookie = self._loadCookie()
        if self.__cookie:
            print("检测到cookie文件，直接使用cookie登录")
            self.__session.cookies.update(self.__cookie)
            soup = BS(self.open(r"http://www.weibo.com/").text, "html.parser")
            print("已登陆账号： %s" % soup.find("span", class_="name").getText())
            a=True
        else:
            print("没有找到cookie文件，请调用login方法登录一次！")

    def _loadCookie(self):
        if(os.path.exists(self.cookieFile)):
            with open(self.cookieFile,'r') as f:
                cookie= json.load(f)
            return cookie
        else:
            return None
    def get_prelogin_status(self):
        prelogin_url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=NTQyMjU%3D&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_=1500105808193' 
        data = urllib.request.urlopen(prelogin_url).read()
        str_data = data.decode()
        pattern = re.compile('\((.*)\)')
        try:
            json_data = re.search(pattern, str_data).group(1)
            data = json.loads(json_data)
            servertime = str(data['servertime'])       
            nonce = data['nonce']
            rsakv = data['rsakv']
            print(servertime,nonce,rsakv)
            return servertime, nonce, rsakv
        except Exception as e:
            print('Getting prelogin status met error!: ' + str(e))
            return None
    def login(self,usename,password):
        self.usename=usename
        self.password=password
        postdata={
        'entry':'weibo',
        'gateway':'1',
        'from':'',    
        'savestate':'7',
        'userticket':'1',
        'pagerefer':'',
        'vsnf': '1',
        'su': '',
        'service': 'account',
        'servertime': '',       
        'nonce': '',
        'pwencode': 'rsa2',
        'rsakv':'',
        'sp': '',
        'sr':'1920*1080',
        'encoding': 'UTF-8',
        'cdult':'3',
        #'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'domain':'sina.com.cn',
        'prelt':'64',
        'returntype': 'TEXT' 
        }
        servertime,nonce,rsakv=self.get_prelogin_status()
        postdata['servertime']=servertime
        postdata['nonce']=servertime
        postdata['rsakv']=servertime
        postdata['su']=self.getsu()
        postdata['sp']=-self.getsp(servertime,nonce)
        res = self.__session.post(self.homeURL, data=postdata)
        print("=" * 50)
        if res.text is not None:
            print('登录成功') # 输出脚本信息，调试用
        self.__saveCookie()
    def __saveCookie(self):
        """cookies 序列化到文件
        即把dict对象转化成字符串保存
        """
        with open(self.cookieFile, "w") as output:
            cookies = self.__session.cookies.get_dict()
            json.dump(cookies, output)
            print("=" * 50)
            print("已在同目录下生成cookie文件：", self.cookieFile)
            
    def getsu(self):
        username_ = urllib.parse.quote(self.usename)
        username = base64.encodestring(username_)[:-1]
        return username
    def getsp(self,servertime,nonce):
        pwd1 = hashlib.sha1(self.password.encode(encoding="utf-8")).hexdigest()
        pwd2 = hashlib.sha1(pwd1.encode(encoding="utf-8")).hexdigest()
        pwd3_ = pwd2 + servertime + nonce
        pwd3 = hashlib.sha1(pwd3_.encode(encoding="utf-8")).hexdigest()
        return pwd3
        
if __name__ == '__main__':
    global a
    a=False
    sina=SinaClient()
    if a==False:
        sina.login('18831299625','2976351bbbb')