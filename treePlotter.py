# -*- coding: utf-8 -*-
"""
Created on Sat May 26 15:31:04 2018

@author: Simon
"""

import matplotlib.pyplot as plt

#定义绘图格式
decisionNode = dict(boxstyle="square", fc="0.7")
leafNode = dict(boxstyle="round",fc="0.7")
arrow_args = dict(arrowstyle="<|-")

#获取叶子总数
def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if ( type(secondDict[key]).__name__=='dict' ):
            #如果还是字典，进入下一层遍历叶子
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs

#获取最大层数
def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if ( type(secondDict[key]).__name__=='dict' ):
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if ( thisDepth>maxDepth ):
            maxDepth = thisDepth
    return maxDepth

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',\
                            xytext=centerPt, textcoords='axes fraction',\
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)

#箭头上的文字
def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)

#递归画树函数
def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)
    #depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]   #取出头节点的标签
    #根据本节点下叶子个数计算起始位置
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]   #头结点的数据
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict': 
            plotTree(secondDict[key],cntrPt,str(key))
        else:   #只有一个节点
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    #本层叶子画完，回到上层，继续作图
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD

def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')    #创建新图形
    fig.clf()    #清空绘图区
    axprops = dict(xticks=[], yticks=[])    #去掉坐标轴
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    #已经绘制的节点位置
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0;
    plotTree(inTree, (0.5,1.0), '')    #从画布的上方往下画图
    plt.savefig("./decisionTree.png")
    #plt.show()
    plt.close()

def retrieveTree():
    listOfTrees =[{'play or nor': {'rain': {'windy': {0: 'yes', 1: 'no'}},\
                                   'sunny': {'temperature': {0: 'yes', 1: 'no'}}, 'overcast': 'yes'}}]
    return listOfTrees[0]
    
#print(retrieveTree())
