'''
Created on 2017年7月15日

@author: aaron
'''
from bs4 import  BeautifulSoup as BS
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
class all_answer(object):
    '''
    爬取知乎上一个问题的所有回答
    '''
    

    def __init__(self,url,headers):
        self._url=url
        self._headers=headers
        
    def scroll(self,driver):
        driver.execute_script("""
            (function () {
                var y = document.body.scrollTop;
                var step = 100;
                window.scroll(0, y);


                function f() {
                    if (y < document.body.scrollHeight) {
                        y += step;
                        window.scroll(0, y);
                        setTimeout(f, 50);
                    }
                    else {
                        window.scroll(0, y);
                        document.title += "scroll-done";
                    }
                }
                setTimeout(f, 1000);
            })();
            """)
    def get_html(self):
        driver=webdriver.Firefox()
        driver.get(self._url)
        a=0
            # 首先加载出全部的内容，判断是否页面中存在“更多”这一个按钮
        while a<30:
            # 这里需要注意的是：selenium2 是不支持 类名之中 有空格的
            #try:
            #self.scroll(driver)
            #time.sleep(20)
            more = driver.find_element_by_css_selector("button.Button.QuestionMainAction")
            actions=ActionChains(driver)
            actions.move_to_element(more)
            actions.click(more)
            a=a+1
            #except NoSuchElementException as e:
                #break
        # 加载了全部的内容后，获取到所有内容，存为items
        soup=BS(driver.page_source,'html5lib')
        driver.quit()
        #soup=soup.prettify()
        #print(soup)
        return soup
    def get_html2(self,session):
        html=session.get(self._url,headers=self._headers)
        soup=BS(html.content,'html5lib')
        return soup
    def get_question(self,soup):
        str=''
        span1=soup.find_all('span',attrs={'class':'RichText CopyrightRichText-richText'})
        print(span1)
        for span in span1:
            str+=span.text+'\n\n\n'
        with open('/home/aaron/桌面/知乎问答','w') as f:
            f.write(str)
        print('导入成功')
        
        
    