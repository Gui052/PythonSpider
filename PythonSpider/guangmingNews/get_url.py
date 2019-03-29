from selenium import webdriver
import os
import sys

def get_urls():

    bro=webdriver.PhantomJS()
    i = 0
    while 1:
        url = 'http://zhannei.baidu.com/cse/search?q=%E6%80%9D%E6%94%BF%20%E6%80%9D%E6%83%B3%E6%94%BF%E6%B2%BB&p=' +str(i) +'&s=6995449224882484381&nsid=1'
        bro.get(url)
        i = i + 1
        bro.implicitly_wait(10)
        urls=bro.find_elements_by_xpath('//h3[@class="c-title"]/a')
        write_file(urls)
        if i==48:
            break
        print(i)

def write_file(urls):
    str=""
    file=open(os.path.join(sys.path[0],'guangming.txt'),'a')
    for i in urls:
        str = str + i.get_attribute('href') + '\n'
    file.write(str)
    file.close()

if __name__ == '__main__':
    get_urls()