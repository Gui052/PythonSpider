from selenium import webdriver
from lxml import etree

bro=webdriver.PhantomJS()
bro.get('http://zhannei.baidu.com/cse/search?q=%E6%80%9D%E6%94%BF+%E6%80%9D%E6%83%B3%E6%94%BF%E6%B2%BB&s=6995449224882484381&srt=lds&nsid=0')
bro.implicitly_wait(10)
while 1:
    urls=bro.find_elements_by_class_name('c-title')
    for i in urls:
        h3=i.get_attribute('innerHTML') #获取源代码
        a=etree.HTML(h3).xpath('//@href')
    nextpage=bro.find_element_by_xpath('//*[@id="pageFooter"]/a[10]')
    if nextpage.text!='':
        nextpage.click()
    else:
        break
bro.quit()