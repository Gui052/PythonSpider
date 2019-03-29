# -*- coding: utf-8 -*-
'''
    >  Filename : 浏览器下载菁优网
    >  dis:手动执行清空操作
    >  Author   : lan
        __
       /\ \
       \ \ \            __       ___
        \ \ \         /'__'\ /\/' _'\
         \ \ \__ __  /\/  \ \\/\ \/\ \
          \ \__  _ _\\ \ __\ \\ \_\ \_\
           \/__ __ _/ \/__ /_'/\/_/\/_/
    >  Date     : 18/07/1 - 01:00
'''
import os
from selenium import webdriver
import tkinter as tk
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pickle
import random

def windows(text):
    window = tk.Tk()
    window.title('INFO!!!')
    window.geometry('300x100')
    l = tk.Label(window,
                 text=text,  # 标签的文字
                 bg='green',# 背景颜色
                 font=('Arial', 12),  # 字体和字体大小
                 width=20, height=2) # 标签长宽
    l.pack(side='top')
    buttons = tk.Button(window, text='关闭', anchor='s', command=window.destroy)
    buttons.pack(side='bottom')
    window.mainloop()

def windows_for_rule():
    global window
    window = tk.Tk()
    window.title('这个是策略选择窗口等待')
    window.geometry('300x150')
    l = tk.Label(window,
                 text='选择完成关闭此窗口或者设置窗口句柄',  # 标签的文字
                 bg='red',# 背景颜色
                 font=('Arial', 12),  # 字体和字体大小
                 width=40, height=2) # 标签长宽
    l.pack(side='top')

    # 登陆界面的信息
    tk.Label(window, text="输入对10取余规则，点'确定'：").place(x=72, y=50)
    # 显示输入框
    originHand = tk.StringVar()
    originHand.set(str(handNum))
    # 显示默认
    global entry_Hand
    entry_Hand = tk.Entry(window, textvariable=originHand)
    entry_Hand.place(x=80, y=80)

    buttons2 = tk.Button(window, text='确定',anchor = 's', command=get_rule)
    buttons2.pack(side='bottom')
    window.mainloop()

def get_rule():
    '''
    获取文本框数据
    :return:
    '''
    global rules
    if entry_Hand.get() != '':
        words = entry_Hand.get()
        temp = words
        rules = temp.split(",")
        # 关闭窗口
        window.destroy()

def start():
    global handNum
    handNum = 1

    option = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'D:\\xiazai\\'} # TODO:下载路径
    option.add_experimental_option('prefs', prefs)
    # option.add_argument(
    #     'User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')
    browser = webdriver.Chrome(chrome_options=option)

    if os.path.exists('cookies.pkl') == 0:

        browser.get('http://www.jyeoo.com/') # login
        windows('登陆完成关闭此窗口即可')
        cookies = browser.get_cookies()
        pickle.dump(cookies, open("cookies.pkl", "wb"))
        print("已在同目录下生成cookies文件：cookies.pkl")

    else:
        browser.get('http://www.jyeoo.com/')
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
        print("载入cookies.pkl")
        browser.refresh()

    # 改变窗口句柄
    windows("请手动点击下载类型（数学等）")
    detail = browser.window_handles[-1]
    browser.switch_to_window(detail)

   
    # 题目计数
    all_subject = 0
    while True:
        windows("请手动点击参数（题型等）")
        windows_for_rule()

        global rules
        page_number = 1
        
        while True:
            browser.implicitly_wait(10)
            WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.ID, 'pageArea')))
            add_to_shitilan = browser.find_elements_by_xpath('//div[@class="fieldtip-right"]/a[last()]')
            # 对10取余
            for index,i in enumerate(add_to_shitilan):
                for k in rules:
                    # 如果列表+1对10取余在规则里面
                    if (index+1)%10==int(k):
                        browser.execute_script("arguments[0].click();",i)
                        all_subject = all_subject+1
                        print("第："+str(page_number)+"页，添加了第："+str(index+1)+"题")

                        # TODO:这里调整间隔
                        time.sleep(random.uniform(2,3))

                        # 如果数量达到,进行下载
                    if all_subject == 50:
                        # 初始化
                        all_subject = 1
                        down = browser.find_element_by_xpath('//*[@id="divRight"]/a')
                        browser.execute_script("arguments[0].click();", down)
                        time.sleep(2)
                        dowmload_hand = browser.window_handles[-1]
                        browser.switch_to_window(dowmload_hand)
                        browser.implicitly_wait(10)

                        browser.find_element_by_xpath('//*[@id="divTree"]/ul[1]/li[1]/label/input').send_keys(Keys.SPACE)
                        browser.find_element_by_xpath('//*[@id="cb-catescore"]').send_keys(Keys.SPACE)
                        browser.find_element_by_xpath('//*[@id="p_flag"]').send_keys(Keys.SPACE)
                        down_button = browser.find_element_by_xpath('//div[@class="paper-cont"]/div[2]/a')
                        browser.execute_script("arguments[0].click();", down_button)
                        browser.implicitly_wait(10)
                        time.sleep(2)

                        WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'box-wrapper')))
                        browser.find_element_by_xpath('//div[@class="btn-block"]/a[1]').click()
                        time.sleep(2)
                        # 执行清空操作
                        browser.execute_script("QuesCart.clear('math',null,function(){location.href='/math/ques/search'})")
                        browser.switch_to.alert.accept()

                        time.sleep(2)
                        browser.close()
                        browser.switch_to_window(detail)

            time.sleep(3)
            next_page = browser.find_elements_by_xpath('//a[@class="next"]')
            if len(next_page)>0:
                browser.execute_script("arguments[0].click();",next_page[0])
                page_number = page_number+1
            else:
                print("结束此参数采集，重新选择参数")
                break


if __name__ == '__main__':
    start()