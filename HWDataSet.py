from PyQt5.QtCore import *
from numpy import *
import struct
import numpy as np

class HWDataSet(QObject):
    """
    手写识别数据集定义
    self.__numTrainSet = array([])      #: 手写数字训练集
    self.__numTrainSetBin = array([])   #: 手写数字训练街（二值化）
    self.__numTrainSetResize = array([])#: 手写数字训练集（去冗余）
    self.__numTrainLabel = array([])    #: 手写数字训练集标签
    self.__numTestSet = array([])       #: 手写数字测试集
    self.__numTestSetBin = array([])   #: 手写数字测试集（二值化）
    self.__numTestSetResize = array([])#: 手写数字测试集（去冗余）
    self.__numTestLabel = array([])     #: 手写数字测试集标签
    """
    def __init__(self, dataPath='./'):
        super(HWDataSet, self).__init__()
        self.__numTrainSet = array([])      #: 手写数字训练集
        self.__numTrainSetBin = array([])   #: 手写数字训练街（二值化）
        self.__numTrainSetResize = array([])#: 手写数字训练集（去冗余）
        self.__numTrainLabel = array([])    #: 手写数字训练集标签
        self.__numTestSet = array([])       #: 手写数字测试集
        self.__numTestSetBin = array([])   #: 手写数字测试集（二值化）
        self.__numTestSetResize = array([])#: 手写数字测试集（去冗余）
        self.__numTestLabel = array([])     #: 手写数字测试集标签
        self.__dataPath = dataPath


    sendMsg = pyqtSignal(object)

    def loadNumData(self):
        # 加载手写数字数据集
        self.loadHWNumDataSet(0)
        # 数据二值化
        self.__numTrainSetBin = self.binaryConversion(self.__numTrainSet)
        w, h, self.__numTrainSetResize = self.resizeImages(self.__numTrainSetBin)
        self.loadHWNumLabelSet(0)

        self.loadHWNumDataSet(1)
        self.__numTestSetBin = self.binaryConversion(self.__numTestSet)
        w, h, self.__numTestSetResize = self.resizeImages(self.__numTestSetBin)
        self.loadHWNumLabelSet(1)

    def numTrainSet(self):
        """
        获取训练数据集
        :return: 训练集原始数据
        """
        return self.__numTrainSet

    def numTrainSetBin(self):
        return self.__numTrainSetBin

    def numTrainSetResize(self):
        return self.__numTrainSetResize

    def numTrainLabel(self):
        """
        获取训练集标签
        :return:
        """
        return self.__numTrainLabel

    def numTestSet(self):
        """
        获取测试集
        :return:  测试集原始数据
        """
        return self.__numTestSet

    def numTestSetBin(self):
        return self.__numTestSetBin

    def numTestSetResize(self):
        return self.__numTestSetResize

    def numTestLabel(self):
        """
        获取测试集标签
        :return:
        """
        return self.__numTestLabel

    def loadHWNumDataSet(self, which=0):
        '''
        手写数字识别数据集加载
        TRAINING SET IMAGE FILE (train-images-idx3-ubyte):
        [offset] [type]          [value]          [description]
        0000     32 bit integer  0x00000803(2051) magic number
        0004     32 bit integer  60000            number of images
        0008     32 bit integer  28               number of rows
        0012     32 bit integer  28               number of columns
        0016     unsigned byte   ??               pixel
        0017     unsigned byte   ??               pixel
        ........
        xxxx     unsigned byte   ??               pixel
        '''
        self.sendMsg.emit("loading image dataset...")
        print("loading image dataset...")
        binfile = None
        if which == 0:
            try:
                binfile = open(self.__dataPath+ r"/train-images.idx3-ubyte", 'rb')
            except IOError:
                self.sendMsg.emit("in class HWDataSet->loadNumData: open train-images.id3-ubyte error")
                print("in class HWDataSet->loadNumData: open train-images.id3-ubyte error")
        else:
            try:
              binfile = open(self.__dataPath+r"/t10k-images.idx3-ubyte", 'rb')
            except IOError:
                self.sendMsg.emit("in class HWDataSet->loadNumData: open t10k-images.id3-ubyte error")
                print("in class HWDataSet->loadNumData: open t10k-images.id3-ubyte error")
        buffers = binfile.read()
        head = struct.unpack_from('>IIII', buffers, 0)
        self.sendMsg.emit("head"+str(head))
        print("head,", head)
        offset = struct.calcsize('>IIII')
        imgNum = head[1]
        width = head[2]
        height = head[3]
        # [60000]*28*28
        bits = imgNum * width * height
        bitsString = '>' + str(bits) + 'B'  # like '>47040000B'
        imgs = struct.unpack_from(bitsString, buffers, offset)
        binfile.close()
        img = np.reshape(imgs, [imgNum, width, height])
        if 0 == which:
            self.__numTrainSet = img
        elif 1 == which:
            self.__numTestSet = img
        self.sendMsg.emit("load images "+str(which)+" finished.")
        print("load images %d finished." %which)
        return img

    # 加载标签集
    def loadHWNumLabelSet(self, which=0):
        print("loading HW number labels...")
        binfile = None
        if which == 0:
            try:
                binfile = open(self.__dataPath+r"/train-labels.idx1-ubyte", 'rb')
            except IOError:
                print("in class HWDataSet->loadHWNumLabelSet: open train-labels.idx1-ubyte error")
        else:
            try:
                binfile = open(self.__dataPath+r"/t10k-labels.idx1-ubyte", 'rb')
            except IOError:
                print("in class HWDataSet->loadHWNumLabelSet: open t10k-labels.idx1-ubyte error")
        buffers = binfile.read()

        head = struct.unpack_from('>II', buffers, 0)
        print("head,", head)
        imgNum = head[1]

        offset = struct.calcsize('>II')
        numString = '>' + str(imgNum) + "B"
        labels = struct.unpack_from(numString, buffers, offset)
        binfile.close()
        labels = np.reshape(labels, [imgNum, 1])
        if 0 == which:
            self.__numTrainLabel = labels
        elif 1 == which:
            self.__numTestLabel = labels
        # print labels
        print('load labels %d finished' %which)
        return labels

    # 二值化
    def binaryConversion(self, imgs):
        binaryImages = []
        if 0 == len(imgs):
            print('Warning: No Data to binary conversion!')
            return None
        for i in imgs:
            img = []
            x_point_l = 28
            y_point_l = 28
            x_point_r = 0
            y_point_r = 0
            for row in range(0, 28):
                img.append([])
                for col in range(0, 28):
                    if i[row][col] > 50:
                        img[row].append(1)
                        if (col < x_point_l):
                            x_point_l = col
                        if (row < y_point_l):
                            y_point_l = row
                        if (col > x_point_r):
                            x_point_r = col
                        if (row > y_point_r):
                            y_point_r = row
                    else:
                        img[row].append(0)
            # print(x_point_l, y_point_l, x_point_r, y_point_r)
            # print(np.array(img))
            # 计算有效数据的坐标点以及长宽
            width = x_point_r - x_point_l+1
            height = y_point_r - y_point_l+1
            Data_Mat = np.zeros((28,28),dtype=np.uint8)
            # 将有效数据移动至图像中心
            point_x = (28 - width) // 2
            point_y = (28 - height) // 2
            # print(point_x,point_y)
            for i in range(0, height):
                for j in range(0, width):
                    Data_Mat[point_y+i][point_x+j] = img[y_point_l+i][x_point_l+j]
            # print(Data_Mat.tolist())

            binaryImages.append(Data_Mat.tolist())
        print('Binary Conversion completed.')
        return np.array(binaryImages)

    def dimReduction(self, imagesDataSet):
        """
        原始数据降维，将原来的矩阵形式转换为一维数组

        参数：
            imagesDataSet：手写图像数据集，三维数组

        返回值：
            newImages：转换后的数据集二维数组
        """
        newImages = []
        for image in imagesDataSet:
            # 矩阵变换
            newImage = image.reshape(1, -1)
            newImages.append(newImage[0])
        return newImages

    def resizeImages(self, images):
        '''
        去掉原始图像中的冗余像素数据
        :param images: 原始图像数据，三维数组
        :returns
            newWidth: resize之后图像的宽度
            newHeight: resize之后图像的高度
            newImages: 去冗余之后的数据集，三维数组
        '''
        newWidth = 0
        newHeight = 0

        '''
        计算新的图像尺寸
        遍历所有图片，找到像素面积最大的图片img
        以img的尺寸作为resize之后的图像尺寸
        '''
        for image in images:
            colSum = image.sum(0)
            rowSum = image.sum(1)
            c = 0
            r = 0
            for i in colSum:
                if i != 0:
                    c += 1
            for i in rowSum:
                if i != 0:
                    r += 1
            if c > newWidth:
                newWidth = c
            if r > newHeight:
                newHeight = r

        '''
        resize
        '''
        newImages = []
        for image in images:
            x0 = 0
            y0 = 0
            xSum = image.sum(1)
            ySum = image.sum(0)
            for i in range(len(xSum)):
                if xSum[i] != 0:
                    x0 = i
                    break
            for i in range(len(ySum)):
                if ySum[i] != 0:
                    y0 = i
                    break
            tempImage = zeros((newWidth, newHeight), int)
            for x in range(x0, 28):
                if x - x0 >= 20: break
                for y in range(y0, 28):
                    if y - y0 >= 20: break
                    tempImage[x - x0][y - y0] = image[x][y]

            newImages.append(tempImage)

        return newWidth, newHeight, array(newImages)
if __name__ == "__main__":
    numDataSets = HWDataSet("./dataset")

    print(numDataSets.numTrainSet()[0])
