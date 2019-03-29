from urllib import request
import json
# 利用urllib2获取网络数据
def registerUrl():
    try:
        url = "http://www.weather.com.cn/data/sk/101090201.html"
        repose=request.urlopen(url)
        data = repose.read()
        return data
    except:
        print()

# 解析从网络上获取的JSON数据
def praserJsonFile(jsonData):
    str2 = jsonData.decode('utf-8') #解决编码问题
    value = json.loads(str2)
    rootlist = value.keys()
    print(rootlist)
    print("--------------------------")
    for rootkey in rootlist:
        print(rootkey)
    print("--------------------------")
    subvalue = value[rootkey]
    print(subvalue)
    print("--------------------------")
    for subkey in subvalue:
        print(subkey, subvalue[subkey])

if __name__ == "__main__":
    data = registerUrl()
    praserJsonFile(data)

