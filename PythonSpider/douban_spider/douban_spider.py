'''
Created on 2017年7月16日

@author: aaron
'''
import os
import re
import subprocess
import sys

import requests
from bs4 import BeautifulSoup as BS

from JSspider import json


class douban:
    headers={'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'}
    cookieFile = os.path.join(sys.path[0], "cookie")
    captchaFile=os.path.join(sys.path[0],"captcha")
    def __init__(self):
        self.session=requests.Session()
        self.session.headers = self.headers 
        self._cookie=self._loadcookie()
        if self._cookie:
            self.session.cookies.update(self._cookie)
            soup = BS(self.session.get(r"http://www.douban.com/").content, "html.parser")
            print("已登陆账号：")# %s" % soup.find("span", class_="name").getText())
        else:
            print("没有找到cookie文件，请调用login方法登录一次！")
            a=False
    def Login(self,username,password):
        
        html=self.session.get('https://accounts.douban.com/login')
        soup=BS(html.content,'html.parser')
        img=soup.find('img',attrs={'class':'captcha_image'})
        print(img)
        captchaUrl=img['src']
        id=soup.find('div',attrs={'class':'captcha_block'}).decode()
        print(id)
        idname=re.findall('<input name="captcha-id" type="hidden" value=\"(.*?)\"/>',id)
        print(str(idname))
        if len(captchaUrl)>0:
            formdata={
                   'login':'登录',
                    'ck':'TK9F',
                   'source':'None',
                  'redir':'https://www.douban.com/',
                  'captcha-solution':'',
                  'captcha-id':'',
                 'form_email':username,
                  'form_password':password,
            }
            print('验证码存在！')
            #while True: 
                #try:
            captcha=requests.get(captchaUrl).content#.encode(encoding='utf-8')
            with open(self.captchaFile,'wb') as f:
                f.write(captcha)
            subprocess.call(self.captchaFile, shell=True)
            cachpt=input('请输入验证码:')
            os.remove(self.captchaFile)
            formdata['captcha-solution']=cachpt
            formdata['captcha-id']=idname
               # except:
                    #break
            self.session.post('https://www.douban.com/accounts/login',data=formdata)
            self._savecookie()
        else:
            formdata2={'source':'index_nav',
                  'redir':'https://www.douban.com/',
                 'form_email':username,
                  'form_password':password,
                  'login':'登录'
            }
            self.session.post('https://accounts.douban.com/login',data=formdata2)
            self._savecookie()
    def get_html(self,url):
        html=self.session.get(url)
        print(html.text)
    def _savecookie(self):
        with open(self.cookieFile,'w') as f:
            cookies=self.session.cookies.get_dict()
            json.dump(cookies, f)
            print('='*50)
            print('已在同一目录下保存cookie:',self.cookieFile)
        
    def _loadcookie(self):
        if os.path.exists(self.cookieFile):
            with open(self.cookieFile,'r') as f:
                  cookie= json.load(f)
                  return cookie
        return None
if __name__ == '__main__':
    global a 
    a=True
    dou=douban()
    if a==False:
       dou.Login('1378709248@qq.com','2976351bbbb')
    dou.get_html('https://www.douban.com/people/163859272/')
    
    
    
    
    