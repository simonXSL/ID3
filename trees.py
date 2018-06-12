# -*- coding: utf-8 -*-
"""
Created on Sat May 26 11:17:46 2018
Decision Tree : ID3
@author: Simon
结束标准：划分出来的类属于同一个类,没有属性可供再分了
"""

from math import log
import operator
import treePlotter

# 计算给定数据集的香农熵
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)   #条目数量
    labelCounts = {}    #每个标签出现的次数，用来计算概率
    for featVec in dataSet:
        currentLabel = featVec[-1]    #取标签，在最后一个
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannoEnt = 0.0    #初始化
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries    #计算概率
        shannoEnt -= prob*log(prob, 2)
    return shannoEnt

# 方式一、创建数据集
def createDataSet():
    dataSet = [['hot', 1, 0, 'sunny', 'no'],
               ['hot', 1, 1, 'sunny', 'no'],
               ['hot', 0, 0, 'overcast', 'yes'],
               ['cool', 0, 1, 'rain', 'no'],
               ['cool', 0, 0, 'rain', 'yes'],
               ['cool', 0, 0, 'sunny', 'yes'],
               ['cool', 0, 0, 'rain', 'yes'],
               ['cool', 1, 1, 'overcast', 'yes']]
    # 气温，湿度，有风，天气，是否出去玩耍
    labels = ['temperature', 'humidity', 'windy', 'play or nor']
    return dataSet, labels

# 方式二、读入数据集
def loadDataSet():
    import re
    retDataSet = []
    fr = open("dataSet.txt")
    for inst in fr.readlines():
        retDataSet.append(re.split('\t', inst))
    return retDataSet
    

# 划分数据集 第axis个属性=value就划分为相应新数据集
def splitDataSet(dataSet, axis, value):
    retDataSet = []    # 不修改原始数据集
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

# 遍历整个数据集，选择信息增益最大的特征-划分数据集
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0])-1    # 最后一个已经人为分好类
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1    # 初始化
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)    # 第i个分类标签 值的集合
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob*calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if ( infoGain > bestInfoGain ):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote]=0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

# 创建字典形式的树
def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    if ( classList.count(classList[0])==len(classList) ):   # 类别完全相同
        return classList[0]
    if ( len(dataSet[0]) == 1 ):    # 递归遍历之后，返回出现次数最多的
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])   # 在这里已经删除了
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value), subLabels)
    return myTree

# 使用决策树执行分类
def classify(inputTree,featLabels,testVec):
    firstStr = list(inputTree.keys())[0]
    print(firstStr)
    secondDict = inputTree[firstStr]
    print(featLabels)
    featIndex = featLabels.index(firstStr) # 将标签转化成索引
    for key in secondDict.keys():
        if testVec[featIndex] == key:  
            if type(secondDict[key]).__name__=='dict':
                classLabel = classify(secondDict[key],featLabels,testVec)
            else : classLabel = secondDict[key]# 到达叶子节点，返回标签
    return classLabel

def storeTree(inputTree,filename):
    import pickle
    fw = open(filename,'wb+')
    pickle.dump(str(inputTree),fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename,'rb')
    return pickle.load(fr)

if __name__ == '__main__':
    """
    # 利用生成的数据集
    myDat,labels = createDataSet()
    shannoEnt = calcShannonEnt(myDat)
    chooseBestFeatureToSplit(myDat)
    myTree = createTree(myDat, labels)
    print(myTree)
    #绘制图形树
    treePlotter.createPlot(myTree)
    #该决策树的存取
    storeTree(myTree,"myClassifier.txt")
    print('决策树:',grabTree("myClassifier.txt"))
    """
    # 读入的数据集
    DataSet = loadDataSet()
    readLabels = ['age','prescript','astigmatic','tearRate']
    myTree = createTree(DataSet, readLabels)
    readLabels = ['age','prescript','astigmatic','tearRate']
    classify(myTree, readLabels, ['pre','myope','no','normal'])
    print(myTree)
    # 绘制图形树
    treePlotter.createPlot(myTree)
    # 生成图形界面,输入数据，执行决策树 treeWidget.py
