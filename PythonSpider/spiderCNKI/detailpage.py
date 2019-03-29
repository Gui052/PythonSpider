# -*- coding: utf-8 -*-
'''
    >  Filename : py
    >  Author   :
        __
       /\ \
       \ \ \             __       ___
        \ \ \         /' __'\ /\/' _'\
         \ \ \__ _  /\ `/  \ \\ \ \/\ \
          \ \_  _ _\\ \_\___\ \\ \_\ \_\
           \/_ __ _/ \/____/_/'/\/_/\/_/
    >  Date     : 17/11/13 - 15:46
'''
from PIL import Image
import pytesseract
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.alert import Alert

browser=webdriver.Chrome()
browser.get('http://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB')
browser.implicitly_wait(10)

time.sleep(3)

browser.find_element_by_xpath(
    '//*[@id="XuekeNavi_Div"]/div[1]/input[1]').click()  # 取消全选
browser.implicitly_wait(10)

time.sleep(3)
# 展开大标题
value='A'  #A--H迭代
type=browser.find_elements_by_xpath('//*[@id="'+value+'first"]')
type[0].click()
browser.implicitly_wait(10)

time.sleep(3)
# 小标题单击
select=browser.find_elements_by_xpath('//*[@id="'+value+'child"]//a')
select[0].click()
browser.implicitly_wait(10)

time.sleep(3)
#点击作者
browser.find_element_by_xpath('//a[@id="alink2"]').click()
browser.implicitly_wait(10)

time.sleep(3)

alert = browser.switch_to().alert()
alert.accept()

name=browser.find_elements_by_xpath('//span[@id="GroupItemALink"]')
name[0].click()
browser.implicitly_wait(10)

time.sleep(3)

#这一块是获取frame链接，即获取到详细页网址
url=browser.find_element_by_id('iframeResult').get_attribute('src')

js="window.open('"+url+"');"
browser.execute_script(js)

browser.implicitly_wait(10)
browser.switch_to_window(browser.window_handles[1])
browser.implicitly_wait(10)
browser.find_element_by_xpath('//*[@id="selectCheckbox"]').click()
browser.implicitly_wait(10)
time.sleep(3)

while 1:
    nextpage=browser.find_elements_by_xpath('//*[@id="Page_next"]')
    if len(nextpage)!=0:
        nextpage[0].click()
        browser.implicitly_wait(10)

        time.sleep(3)

        browser.find_element_by_xpath('//*[@id="selectCheckbox"]').click()
        browser.implicitly_wait(10)

        time.sleep(3)

    else:
        browser.find_element_by_xpath('//a[@title="生成、导出所选文献不同的引文格式"]').click()
        browser.switch_to_window(browser.window_handles[2])
        browser.implicitly_wait(10)
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="exportExcel"]').click()
        browser.implicitly_wait(10)

        time.sleep(5)

        browser.close()
        browser.switch_to_window(browser.window_handles[1])
        time.sleep(2)
        browser.close()
        browser.switch_to_window(browser.window_handles[0])
        break

time.sleep(3)
browser.close()

browser.quit()