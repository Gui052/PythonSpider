#将doc转为docx，统计每张试卷的标签情况，将统计结果输出到excel中
import os
from win32com import client as wc

path = "C:\\Users\\lsgo24\\Desktop\\2013-2017年全国各地中考数学试卷\\整理完毕的试卷\\{0}中考数学试卷"
savepath = "E:\\words\\{0}"

year = ['2013','2014','2015','2016','2017']

word = wc.Dispatch('Word.Application')
for i in year:
    temppath = path.format(i)

    files=os.listdir(temppath)
    for file in files:
        try:
            os.mkdir(savepath.format(i) +"\\"+ file.split('.')[0])
        except:
            print("文件夹存在")

        try:
            doc = word.Documents.Open(temppath + "\\" + file)
            doc.SaveAs(savepath.format(i) + "\\" + file.split('.')[0] + "\\index.html" , 10)
            doc.Close()
        except:
            print("错误文档：" + file)

word.Quit()