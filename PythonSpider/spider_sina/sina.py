import base64
import binascii
import http.cookiejar as cookielib
import re
import urllib.parse
import urllib.request as urllib2

import rsa


#import requests
#from bs4 import BeautifulSoup  
  
#新浪微博的模拟登陆  
class weiboLogin:  
    def enableCookies(self):  
            #获取一个保存cookies的对象  
            cj = cookielib.CookieJar()  
            #将一个保存cookies对象和一个HTTP的cookie的处理器绑定  
            cookie_support = urllib2.HTTPCookieProcessor(cj)  
            #创建一个opener,设置一个handler用于处理http的url打开  
            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
            #安装opener，此后调用urlopen()时会使用安装过的opener对象  
            urllib2.install_opener(opener)  
  
    #预登陆获得 servertime, nonce, pubkey, rsakv  
    def getServerData(self):  
            #url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=ZW5nbGFuZHNldSU0MDE2My5jb20%3D&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_=1442991685270'  
            url='https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.19)&_=1500170971406'
            data = urllib2.urlopen(url).read()  
            #print(data)
            #p = re.compile('(.∗)')  
            try:  
                    #json_data = p.search(data).group(1)  
                    #data = json.loads(json_data)  
                    servertime = '1500172429'#str(data['servertime'])  
                    nonce ='4XRTJM' #data['nonce']  
                    pubkey = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC25\
                              3062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC\
                              02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1B\
                              BE495927AC4A799B3181D6442443'                      
                    pubkey=pubkey.replace(' ','')
                    print(pubkey)
                    rsakv ='1330428213' #data['rsakv']      #data['pubkey'] 
                    return servertime, nonce, pubkey, rsakv  
            except:  
                    print ('Get severtime error!')  
                    return None  
                  
  
    #获取加密的密码  
    def getPassword(self, password, servertime, nonce, pubkey):  
            rsaPublickey = int(pubkey, 16)  
            key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥  
            message = str(servertime) + '\t' + str(nonce) + '\n' + str(password) #拼接明文js加密文件中得到  
            passwd = rsa.encrypt(message.encode('utf-8'), key) #加密  
            passwd = binascii.b2a_hex(passwd) #将加密信息转换为16进制。  
            return passwd  
  
    #获取加密的用户名  
    def getUsername(self, username):  
            username_ = urllib.parse.quote(username)  
            username =  base64.b64encode(username_.encode(encoding='utf-8'))[:-1]  
            return username  
  
     #获取需要提交的表单数据     
    def getFormData(self,userName,password,servertime,nonce,pubkey,rsakv):  
        userName = self.getUsername(userName)  
        psw = self.getPassword(password,servertime,nonce,pubkey)  
          
        form_data = { 
            'entry':'weibo',  
            'gateway':'1',  
            'from':'',  
            'savestate':'7',  
            'useticket':'1',  
            'pagerefer':'http://weibo.com/p/1005052679342531/home?from=page_100505&mod=TAB&pids=plc_main',  
            'vsnf':'1',  
            'su':userName,  
            'service':'miniblog',  
            'servertime':servertime,  
            'nonce':nonce,  
            'pwencode':'rsa2',  
            'rsakv':rsakv,  
            'sp':psw,  
            'sr':'1366*768',  
            'encoding':'UTF-8',  
            'prelt':'115',  
            'url':'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',  
            'returntype':'META'  
            }  
        formData = urllib.parse.urlencode(form_data).encode(encoding='UTF8')
        return formData  
  
    #登陆函数  
    def login(self,username,psw):  
            self.enableCookies()  
            url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'  
            servertime,nonce,pubkey,rsakv = self.getServerData()  
            formData = self.getFormData(username,psw,servertime,nonce,pubkey,rsakv)  
            headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Lin… Gecko/20100101 Firefox/54.0'}  
            req  = urllib2.Request(  
                    url = url,  
                    data = formData,  
                    headers = headers  
            )  
            result = urllib2.urlopen(req)  
            text = result.read()  
            print (text)  
            #还没完！！！这边有一个重定位网址，包含在脚本中，获取到之后才能真正地登陆  
            p = re.compile('location\.replace[\"](.∗?)[\"]')  
            try:  
                    #login_url = p.search(text).group(1)  
                    #print (login_url)
                    login_url='http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack&retcode=2092&reason=%B1%A7%C7%B8%A3%A1%B5%C7%C2%BC%CA%A7%B0%DC%A3%AC%C7%EB%C9%D4%BA%F2%D4%D9%CA%D4'  
                    #由于之前的绑定，cookies信息会直接写入  
                    urllib2.urlopen(login_url)  
                    print ("Login success!")  
            except:  
                    print ('Login error!')  
                    return 0  
  
            #访问主页，把主页写入到文件中  
            url = 'http://weibo.com/u/2679342531?refer_flag=1005055014_&is_hot=1'  
            request = urllib2.Request(url)  
            response = urllib2.urlopen(request)  
            text = response.read().decode("gb2312")
            print(text)
            fp_raw = open("/home/aaron/桌面/sina","w")  
            fp_raw.write(text)  
            fp_raw.close()  
            #print text  
              
wblogin = weiboLogin()  
print ('新浪微博模拟登陆:')
username ='18831299625'
password = '29763251bbbb'
wblogin.login(username,password)
  