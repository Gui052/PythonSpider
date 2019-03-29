
import tkinter as tk


def windows_for_rule():
    global window
    window = tk.Tk()
    window.title('策略选择添加题目窗口等待')
    window.geometry('350x250')
    l = tk.Label(window,
                 text='选择完成关闭此窗口或者设置窗口句柄',  # 标签的文字
                 bg='red',  # 背景颜色
                 font=('Arial', 12),  # 字体和字体大小
                 width=40, height=2)  # 标签长宽
    l.pack(side='top')

    # 登陆界面的信息
    tk.Label(window, text="输入对10取余规则").place(x=72, y=50)
    # 显示输入框
    originHand = tk.StringVar()
    originHand.set(str(0))
    # 显示默认
    global entry_Hand
    entry_Hand = tk.Entry(window, textvariable=originHand)
    entry_Hand.place(x=80, y=80)

    tk.Label(window, text="输入手动添加的题目数").place(x=72, y=120)
    addsub = tk.StringVar()
    addsub.set(str(0))
    # 显示默认
    global addNum
    addNum = tk.Entry(window, textvariable=addsub)
    addNum.place(x=80, y=150)

    buttons2 = tk.Button(window, text='确定', anchor='s', command=get_rule)
    buttons2.pack(side='bottom')
    window.mainloop()
def get_rule():
    '''
    获取文本框数据
    :return:
    '''
    global rules,handaddnum
    if entry_Hand.get() != '':
        words = entry_Hand.get()
        temp = words
        rules = temp.split(",")

    if addNum.get() != '':
        handaddnum = addNum.get()
    # 关闭窗口
    window.destroy()


if __name__ == '__main__':
    windows_for_rule()
    global rules, handaddnum
