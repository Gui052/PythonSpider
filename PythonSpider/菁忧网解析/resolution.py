import urllib.request
import urllib.parse
from lxml import etree
from lxml.html import tostring
import requests
import re
import os
import datetime
import json
import sys
import traceback


def get_cookies():

    if os.path.exists('cookie'):
        with open('cookie', "r") as f:
            cookie = json.load(f)
            print("载入cookie")
    return cookie


def url_request(url,cookie):
    '''
    网页请求函数
    :param url:
    :return:
    '''
    cookies = {}
    id=url.split('/')[-1]
    for i in cookie:
        name = i['name']
        value = i['value']
        cookies[name] = value
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'}
    session = requests.Session()
    session.headers = headers
    session.cookies.update(cookies)
    html = session.get(url)
    htmldetial =  bytes.decode(html.content)
    return htmldetial,id



def get_img_url(html):
    img_string = etree.HTML(html)
    img_urls = img_string.xpath('//img/@src')
    img_urls2 =re.findall('(http://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|].png)',html)
    img_urls.extend(img_urls2)
    img_urls=list(set(img_urls))
    if not img_urls:
        return html,[]
    ss = requests.Session()
    img_name=[]
    for i,img_url in enumerate(img_urls):
        html=html.replace(img_url,'{'+str(i)+'}')
        img_content = ss.get(img_url)
        current_time=datetime.datetime.now().microsecond
        img_name.append(current_time)
        path=os.path.join('pictures',str(current_time)+'.png')
        with open(path, 'wb') as f:
            f.write(img_content.content)
    return  html,img_name




def process_stem(stem,Is_option=False):
    stem=stem.replace('</td></tr><tr><td>','/')#替换为除号
    stem=stem.replace('<sup>','**')  #
    stem = stem.replace('&nbsp;', '')
    #stem = stem.replace('&nbsp;', '')
    stem=stem.replace('\r\n','**')
    fill_blank=re.findall('(<div class="sanwser">.*?</div>)',stem)
    for blank in fill_blank:
        stem=stem.replace(blank,'')
    stem=re.findall('>(.*?)<',stem)
    question_item=''
    if Is_option==False:
        for i in range(len(stem)):
            question_item+=stem[i]
    else:
        for i in range(len(stem)):
            question_item+=stem[i]+" "

    return question_item


def get_html_and_text(html,str_xpath):
    selector = etree.HTML(html)
    comment1 = selector.xpath(str_xpath)
    if comment1:
        comment1 = tostring(comment1[0], encoding='unicode')
        comment = process_stem(comment1)
    else:
        comment = ''
    return comment1,comment


def get_question_content(html,id):

    selector = etree.HTML(html)  # 将源码转化为能被XPath匹配的格式
    stem1 = tostring(selector.xpath('//*[@id="{0}"]/div[@class="pt1"]'.format(id))[0],encoding='unicode')
    stem=process_stem(stem1)
    match_item=re.findall('[\(（][^\)）]+[\)）]',stem)
    if match_item[0]:
        stem=stem.replace(match_item[0],'')

    try:
        option1= tostring(selector.xpath('//*[@id="{0}"]/div[@class="pt2"]'.format(id))[0],encoding='unicode')
        option = process_stem(option1,Is_option=True)
    except:
        option=''

    key_point=selector.xpath('//*[@id="{0}"]/div[@class="pt3"]/a/text()'.format(id))

    # 得到考点的源码和匹配项
    if key_point:
        key_point1 =tostring(selector.xpath('//*[@id="{0}"]/div[@class="pt3"]'.format(id))[0],encoding='unicode')
        key_point=key_point[0]
    else:
        key_point=''
        key_point1 = ''
    special_question=selector.xpath('//*[@id="{0}"]/div[@class="pt4"]/text()'.format(id))
    if special_question:
       special_question=special_question[0]
       special_question1= tostring(selector.xpath('//*[@id="{0}"]/div[@class="pt4"]'.format(id))[0],encoding='unicode')
    else:
       special_question=''
       special_question1=''

    #得到分析,解答，评论的源码和匹配内容
    analysis1,analysis=get_html_and_text(html,'//*[@id="{0}"]/div[@class="pt5"]'.format(id))
    solve1,solve=get_html_and_text(html,'//*[@id="{0}"]/div[@class="pt6"]'.format(id))
    comment1,comment=get_html_and_text(html,'//*[@id="{0}"]/div[@class="pt7"]'.format(id))

    #得到组卷次数，真题和难度值的内容
    zu_juan=selector.xpath('//*[@id="cont"]/div[2]/div[4]/div[2]/div[1]/span/label[3]/em/text()')
    zhen_ti=selector.xpath('//*[@id="cont"]/div[2]/div[4]/div[2]/div[1]/span/label[2]/em/text()')
    difficult=selector.xpath('//*[@id="cont"]/div[2]/div[4]/div[2]/div[1]/span/label[1]/em/text()')

    #得到题目源码以及题目中包含的图片路径
    question_html=stem1 + option1
    question_html,question_img_path=get_img_url(question_html)

    #得到解析源码以及解析中包含的图片路径
    analyse_html=key_point1+special_question1+analysis1+solve1+comment1
    analyse_html,analyse_img_path=get_img_url(analyse_html)



    return  stem,option,key_point,special_question,analysis,solve,comment,zu_juan,zhen_ti,difficult,question_html \
            ,analyse_html,question_img_path,analyse_img_path



def run(url):
    cookie=get_cookies()
    html,id=url_request(url,cookie)
    stem,option,key_point,special_question, analysis, solve, comment,zu_juan,zhen_ti,difficult,question_html,analyse_html,question_img_path,analyse_img_path=get_question_content(html,id)
    return stem,option,key_point,special_question,analysis,solve\
        ,comment,zu_juan[0],zhen_ti[0],difficult[0],question_html,analyse_html\
        ,question_img_path,analyse_img_path
print(run('http://www.jyeoo.com/math/ques/detail/0a48770a-d5aa-48f8-8786-4c41a60c452e'))