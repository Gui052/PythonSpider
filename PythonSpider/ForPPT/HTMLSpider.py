from urllib import request
from lxml import etree
# ----------------------------------------------------------------------
def GetHtml(url):
    text = request.urlopen(url)
    html = text.read()
    return html
# ----------------------------------------------------------------------
def NextPage(Html):
    nextpage = etree.HTML(Html)
    urlNext = nextpage.xpath('//a[@class="next"]/@href')
    return urlNext[0]
# ----------------------------------------------------------------------
def GetInfo(html):
    select = etree.HTML(html)
    money = select.xpath('//div[@class="money"]/b/text()')
    title = select.xpath('//div[@class="des"]/h2/a[1]/text()')
    param = []
    for i in range(len(money)):
        print([title[i], money[i]])
# ----------------------------------------------------------------------
if __name__ == "__main__":
    Html = GetHtml('http://bd.58.com/chuzu/?PGTID=0d100000-001a-85ce-4e76-5e66d0195bb9&ClickID=1')
    urls = NextPage(Html)
    GetInfo(Html)
