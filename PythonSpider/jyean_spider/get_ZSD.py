from urllib import request
from lxml import etree
import os
import sys


def get_node():
    '''获取知识点节点标号'''
    url='http://www.jyeoo.com/tech2/ques/partialcategory?a=undefined&q=&f=1&r=0.16314471814861653'
    html = request.urlopen(url).read().decode('utf8')
    text = etree.HTML(html)
    node = text.xpath('//a[@onclick="nodeClick(this,2)"]/..')
    nodes = ""
    for i in node:
        # temp1 = i.xpath('a/@pk')[0]
        temp2=i.xpath('a/text()')[0]
        nodes += temp2 + '\n'
    with open(os.path.join(sys.path[0], '高中通用.txt'), 'w', encoding='utf8') as f:
        f.write(nodes)

if __name__ == '__main__':
    get_node()