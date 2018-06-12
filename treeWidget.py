# -*- coding: utf-8 -*-
"""
Created on Sat May 26 17:04:27 2018

@author: Simon
"""
import trees
import tkinter
from tkinter import messagebox
import treePlotter

top = tkinter.Tk()  # 顶层窗口对象，容纳整个GUI应用
top.title("决策树")
top.geometry("690x550")
top.resizable(width=0, height=0)

helloLabel = tkinter.Label(top, text="决策树")
helloLabel.pack()

myDat = trees.loadDataSet()
labels = ['age', 'prescript', 'astigmatic', 'tearRate']
myTree = trees.createTree(myDat, labels)
treePlotter.createPlot(myTree)
# 创建画布，加载图像
canvas = tkinter.Canvas(top,height=480,width=680)
imageFile = tkinter.PhotoImage(file="decisionTree.png")
image = canvas.create_image(5,5,anchor='nw',image=imageFile)
canvas.pack(side='top')

# 定义变量
varTestOne = tkinter.StringVar()
varTestOne.set('young,myope,no,normal')
testLabel = tkinter.Label(top, text="请输入测试数据")
testLabel.pack(side='left')
entry_TestOne = tkinter.Entry(top,textvariable=varTestOne)  # 显示变量
entry_TestOne.pack(side='left')

def ack():
    # 处理函数
    usrOne = varTestOne.get()   # 用户输入
    varTestOne.set(usrOne)
    print(usrOne.strip(',').split(','))
    
    labels = ['age', 'prescript', 'astigmatic', 'tearRate']
    result = trees.classify(myTree,labels,usrOne.strip(',').split(','))
    tkinter.messagebox.showinfo(title="判断结果",message="您的输入是："+usrOne+"\n结果是："+result)

ackButton = tkinter.Button(top, text="确定", command=ack)
#ackButton.place(x=483,y=505)
ackButton.pack(side='left')

quitButton = tkinter.Button(top, text="退出", command=top.quit)
quitButton.pack(side='right')

#进入主事件循环
top.mainloop()

