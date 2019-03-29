from selenium import webdriver
import os
import sys

browser=webdriver.PhantomJS()

def write_file(urls):
    str=""
    file=open(os.path.join(sys.path[0],'RenMinWang.txt'),'a')
    for i in urls:
        str = str + i.get_attribute('href') + '\n'
    file.write(str)
    file.close()

def get_urls():
    browser.get('http://www.people.com.cn/')
    browser.implicitly_wait(10)
    browser.execute_script('searchForm.submit();')
    browser.implicitly_wait(10)
    #转换窗口句斌
    browser.switch_to_window(browser.window_handles[1])
    browser.find_element_by_xpath('//*[@id="keyword"]').send_keys('思政 思想政治')
    browser.execute_script("createParameter('/cnpeople/search.do','news')")
    browser.implicitly_wait(10)
    while 1:
        urls=browser.find_elements_by_xpath('//ul/li[3]/a')
        write_file(urls)
        nextpage=browser.find_elements_by_link_text('下一页')
        if len(nextpage)!=0:
            nextpage[0].click()
        else:
            break


if __name__ == '__main__':
    get_urls()
    browser.quit()