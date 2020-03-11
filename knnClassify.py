# coding=utf-8
"""
knn分类算法模块
"""
from numpy import *

def knnClassify(testFeature, trainingSet, labels, k):
    """
    KNN算法实现，采用欧氏距离

    参数：
        testFeature：测试数据集，ndarray类型，一维数组
        trainingSet：训练数据集，ndarray类型，二维数组
        labels：训练集对应标签，ndarray类型, 一维数组
        k：k值，数值型（int）

    返回值：
        预测结果，类型与标签中的元素一致
    """
    dataSetSize = trainingSet.shape[0]
    '''
    构建一个由dataSet[i]-testFeature的新的数据集diffMat
    diffMat中每个元素都是dataSet中每个特征与testFeature的差值（欧氏距离中的差）
    '''
    testFeatureArray = tile(testFeature, (dataSetSize, 1))
    diffMat = testFeatureArray - trainingSet
    # 对每个差值求平方
    sqDiffMat = diffMat ** 2
    # 计算dataSet中每个属性与testFeature的差的平方的和
    sqDistances = sqDiffMat.sum(axis=1)
    # 计算每个feature与testFeature之间的欧氏距离
    distances = sqDistances ** 0.5

    '''
    排序,按照从小到大的顺序记录distances中各个数据的位置
    如：distance = [5, 9, 0, 2]
    则：sortedDistance = [2, 3, 0, 1]
    '''
    sortedDistances = distances.argsort()

    # 选择距离最小的k个点
    classCount = {}
    for i in range(k):
        voteiLabel = labels[sortedDistances[i]]
        classCount[voteiLabel] = classCount.get(voteiLabel, 0) + 1
    # print('classCount: ', classCount)
    # 对k个结果进行统计、排序，选出最终结果，将字典按照value值从大到小排序

    sortedClassCount = sorted(classCount.items(), key=lambda x: x[1], reverse=True)
    # print("sortedClassCount", sortedClassCount)

    return sortedClassCount[0][0]
