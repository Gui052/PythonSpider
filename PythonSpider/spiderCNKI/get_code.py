import requests
from PIL import Image
from PIL import ImageEnhance
from io import BytesIO

'''
获取知网验证码并且进行灰度处理
'''

url="http://kns.cnki.net/kns/checkcode.aspx?t='+Math.random()"

for i in range(100):
    code=requests.get(url)

    img_name = 'code/'+str(i)+'.png'
    image = Image.open(BytesIO(code.content))
    enh_bri = ImageEnhance.Brightness(image)
    brightness = 1.5
    image_brightened = enh_bri.enhance(brightness)
    image_brightened.save(img_name)
    print(i)