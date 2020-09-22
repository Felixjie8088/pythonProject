# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   图形化界面.py
@Desc:
@Create: 2020/09/21 15:25
"""
import tkinter
import tkinter.messagebox as tkmsgbox
import tkinter.filedialog as filedia


class GUI(object):
    def __init__(self, window):
        self.window = window,
        # self.window.title = "去除图片背景（抠图）",
        # self.window.geometry("300x200")
        menubar = tkinter.Menu(self.window)

        # # 创建两个列表
        # li = ['C', 'python', 'php', 'html', 'SQL', 'java']
        # movie = ['CSS', 'jQuery', 'Bootstrap']
        # listb = tkinter.Listbox(root)  # 创建两个列表组件
        # listb2 = tkinter.Listbox(root)
        # for item in li:  # 第一个小部件插入数据
        #     listb.insert(0, item)
        #
        # for item in movie:  # 第二个小部件插入数据
        #     listb2.insert(0, item)
        #
        # listb.pack()  # 将小部件放置到主窗口中
        # listb2.pack()

    def HelloWorld():
        tkmsgbox.showinfo(title="Tips", message="Hello World!")

    def set_button(self, callback):
        button = tkinter.Button(text="Click Me", activebackground="Blue", command=callback)
        button.pack()


if __name__ == '__main__':
    root = tkinter.Tk()  # 创建窗口对象的背景色
    gui = GUI(root)
    gui.set_button(HelloWorld)
    root.mainloop()  # 进入消息循环
