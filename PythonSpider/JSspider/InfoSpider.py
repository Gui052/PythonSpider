from selenium import webdriver
import time
import re
import os
import sys

browser = webdriver.Chrome()
browser.get("http://read.ccpph.com.cn/")

browser.implicitly_wait(10)

ids = [
    "313",
    "314",
    "315",
    "327",
    "415",
    "416",
    "419",
    "422",
    "423",
    "424",
    "425",
    "426",
    "427"]
pages = [209, 81, 103, 48, 60, 308, 43, 114, 43, 211, 71, 344, 615]
length = 0

while length < len(ids):
    # 手动输入id
    browser.find_element_by_xpath("//*[@id=" + ids[length] + "]").click()
    # 手动输入页数
    num = pages[length]
    name = browser.find_element_by_xpath("//*[@id=" + ids[length] + "]").text
    str = ""
    while num:
        browser.implicitly_wait(10)
        # 获取出版时间
        bookinfo = browser.find_elements_by_xpath(
            '//div[@class="infoPanel"]/div[4]')
        # 获取书名
        bookname = browser.find_elements_by_xpath('//div[@class="infoTitle"]')

        i = 0
        while len(bookinfo) > i:
            str = str + bookname[i].text + ":" + bookinfo[i].text + "\n"
            i = i + 1

        # 点击下一页
        browser.find_element_by_xpath('//*[@onclick="next()"]').click()
        num = num - 1

    f = open(os.path.join(sys.path[0], name + '.txt'), 'a')
    f.write(str)
    f.close()
    length = length + 1


try:
    browser.implicitly_wait(10)
    browser.find_element_by_xpath('//*[@id="logoutbtn"]').click()
except BaseException:
    browser.quit()
browser.implicitly_wait(10)
browser.quit()
