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

url = 'http://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB'
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(10)
driver.find_element_by_xpath(
    '//*[@id="XuekeNavi_Div"]/div[1]/input[1]').click()  # 取消全选
driver.implicitly_wait(10)
time.sleep(5)
driver.find_elements_by_xpath('//*[@id="Afirst"]')[0].click()  # 展开大标题
driver.implicitly_wait(10)
time.sleep(5)
# driver.find_elements_by_xpath('//*[@id="selectbox"]')[0].click()  #大标题选择框
driver.find_elements_by_xpath('//*[@id="Achild"]//a')[0].click()
driver.implicitly_wait(10)
time.sleep(5)
driver.find_element_by_xpath('//*[@id="alink2"]').click()  # 点击作者
driver.implicitly_wait(10)
time.sleep(5)
driver.find_elements_by_xpath('//*[@id="groupPagerundefined"]')[1].click()
driver.implicitly_wait(10)
time.sleep(5)
name = driver.find_elements_by_xpath('//*[@id="Show2"]//li')
name[0].click()
driver.implicitly_wait(10)

time.sleep(5)
table=driver.switch_to().frame(1)
print()

# driver.execute_script("javascript:expertCoreSearch('&ua=1.21')")#执行js函数,搜索按钮点击

# if driver.find_element_by_xpath('//*[@id="CheckCodeImg"]') == 1:  # 找到网页有验证码的情况
#     driver.save_screenshot('f://aa.png')  # 截取当前网页，该网页有我们需要的验证码
#     imgelement = driver.find_element_by_xpath(
#         '//*[@id="CheckCodeImg"]')  # 定位验证码
#     location = imgelement.location  # 获取验证码x,y轴坐标
#     size = imgelement.size  # 获取验证码的长宽
#     rangle = (int(location['x']),
#               int(location['y']),
#               int(location['x'] + size['width']),
#               int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
#     i = Image.open("f://aa.png")  # 打开截图
#     frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
#     frame4.save('f://frame4.jpg')
#     qq = Image.open('f://frame4.jpg')
#     text = pytesseract.image_to_string(qq).strip()  # 使用image_to_string识别验证码
#     driver.find_element_by_id('CheckCode').send_keys(text) # 填入验证码
# driver.find_element_by_xpath('//input[@onclick="javascript:CheckCodeSubmit()"]').click()
# #点击提交
