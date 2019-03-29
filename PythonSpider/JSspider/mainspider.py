from selenium import webdriver
import time
import re
import os
import sys

browser = webdriver.Chrome()
browser.get("http://read.ccpph.com.cn/")

browser.implicitly_wait(10)

#手动输入id
browser.find_element_by_xpath('//*[@id="427"]').click()
#手动输入页数
num = 165

while num:
    browser.implicitly_wait(10)
    # 获取ID
    butt = browser.find_elements_by_xpath('//div[@class="list_botom"]/div')
    bookid = ""
    for i in butt:
        stro = i.get_attribute('onclick')
        temp = re.findall(r'B\w*\d', stro)
        bookid = bookid + temp[0] + '\n'
    f = open(os.path.join(sys.path[0], 'bookid.txt'), 'a')
    f.write(bookid)
    f.close()
    # 获取书名
    bookname = browser.find_elements_by_xpath('//div[@class="infoTitle"]')
    namestr = ""
    for i in bookname:
        namestr = namestr + i.text + '\n'
    f = open(os.path.join(sys.path[0], 'bookname.txt'), 'a')
    f.write(namestr)
    f.close()

    # 点击下一页
    browser.find_element_by_xpath('//*[@onclick="next()"]').click()
    num = num - 1
    print("获取第" + str(num) + "页")

try:
    browser.implicitly_wait(10)
    browser.find_element_by_xpath('//*[@id="logoutbtn"]').click()
except BaseException:
    browser.quit()
browser.implicitly_wait(10)
browser.quit()
