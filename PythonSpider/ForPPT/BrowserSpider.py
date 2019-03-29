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

browser=webdriver.Chrome()
browser.get('http://www.baidu.com')
browser.implicitly_wait(10)
browser.find_element_by_id('kw').send_keys('Python')
browser.find_element_by_id('su').click()

text=''
for i in range(1,10):
    div=browser.find_element_by_id(str(i)).get_attribute('srcid')
    text=text+div+'\n'
title=browser.find_elements_by_xpath('//h3[@class="t"]')
for i in title:
    print(i.text)

browser.quit()
print(text)

