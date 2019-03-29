import os
import sys
from bs4 import  BeautifulSoup as BS
import requests
number=10

url1 = 'http://read.ccpph.com.cn/Service/?logic=PDFReaderController&call=getJS&jsurl='+'B_01015673_001'+'(' + str(
    number) + ').js'
html = requests.Session().get(url1)
soup = BS(html.content, 'html.parser')

textjs=""
mainjs = open(os.path.join(sys.path[0],'main.txt'), 'r') #更改了以文件形式读入
textlist=mainjs.readlines()
for i in textlist:
    textjs=textjs+i
jsfile= 'function str(s){' + str(soup) +textjs+ '}'
f = open(os.path.join(sys.path[0],'result.js'), 'w')
f.write(jsfile)
f.close()