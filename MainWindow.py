import sys
from PaintPad import PaintPad
from HWDataSet import HWDataSet
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from numpy import *
from knnClassify import *
from sklearn import neighbors



class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.dataset = HWDataSet("./dataset")
        self.dataset.sendMsg.connect(self.showMsg)

        self.knn = neighbors.KNeighborsClassifier()

        #手写板
        self.paintBox = QGroupBox("Hand Write Area")
        self.paintPad = PaintPad()
        #二进制
        # self.binViewBox = QGroupBox("Binary Image")
        # self.binViewLabel = QLabel()
        # self.binViewLabel.setAlignment(Qt.AlignCenter)
        #结果展示
        self.resBox = QGroupBox("Result Display")
        self.resDisplay = QLabel("[HELLO]")
        font = QFont()
        font.setBold(True)
        font.setPointSize(100)
        self.resDisplay.setFont(font)
        self.resDisplay.setAlignment(Qt.AlignCenter)

        self.msgPad = QLabel()

        self.recoBtn = QPushButton("Recognition")
        self.recoBtn.clicked.connect(self.recognition)

        self.clearBtn = QPushButton("Clear")
        self.clearBtn.clicked.connect(self.paintPad.clear)

        self.loadBtn = QPushButton("LoadData")
        self.loadBtn.clicked.connect(self.loadData)

        paintLayout = QHBoxLayout()
        paintLayout.addWidget(self.paintPad)
        self.paintBox.setLayout(paintLayout)

        # binViewLayout = QHBoxLayout()
        # binViewLayout.addWidget(self.binViewLabel)
        # self.binViewBox.setLayout(binViewLayout)

        disLayout = QHBoxLayout()
        disLayout.addWidget(self.resDisplay)
        self.resBox.setLayout(disLayout)

        self.upLayout = QHBoxLayout()
        self.upLayout.addWidget(self.paintBox)
        # self.upLayout.addWidget(self.binViewBox)
        self.upLayout.addWidget(self.resBox)

        self.downLayout = QHBoxLayout()
        self.downLayout.addWidget(self.msgPad)
        self.downLayout.addWidget(self.clearBtn)
        self.downLayout.addWidget(self.recoBtn)
        self.downLayout.addWidget(self.loadBtn)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.upLayout)
        self.mainLayout.addLayout(self.downLayout)

        self.setLayout(self.mainLayout)
        self.resize(1800, 600)
        self.setWindowTitle("Hand Write Recognition By Python.")

    def loadData(self):
        self.msgPad.setText("Loading Data...")
        #Load Data
        self.dataset.loadNumData()
        self.msgPad.setText("Load Data ok.")
        #将二值化数据降维至向量
        trainingData = self.dataset.dimReduction(self.dataset.numTrainSetBin())
        trainingLabels = self.dataset.numTrainLabel().reshape((1, -1))[0]
        self.msgPad.setText("Training algorithm...")
        self.knn.fit(trainingData, trainingLabels)
        self.msgPad.setText("Training algorithm ok.")

    def showMsg(self, msg):
        self.msgPad.setText(msg)

    def recognition(self):
        testData = self.paintPad.getPaintData()
        # self.binViewLabel.clear()
        strData = str(testData)
        strData = strData.replace('0', ' ')

        # self.binViewLabel.setText(strData)
        testData = testData.reshape(1, -1)
        n = self.knn.predict(testData)
        '''
        n = knnClassify(testData[0], self.trainSetDim, trainingLabels, 3)
        '''
        self.resDisplay.clear()
        self.resDisplay.setText(str(n))

class Main(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.dataset = HWDataSet("./dataset")
        self.dataset.sendMsg.connect(self.showMsg)

        self.knn = neighbors.KNeighborsClassifier()

        #手写板
        self.paintBox = QGroupBox("Hand Write Area")
        self.paintPad = PaintPad()
        #二进制
        # self.binViewBox = QGroupBox("Binary Image")
        # self.binViewLabel = QLabel()
        # self.binViewLabel.setAlignment(Qt.AlignCenter)
        #结果展示
        self.resBox = QGroupBox("Result Display")
        self.resDisplay = QLabel("[HELLO]")
        font = QFont()
        font.setBold(True)
        font.setPointSize(100)
        self.resDisplay.setFont(font)
        self.resDisplay.setAlignment(Qt.AlignCenter)

        self.msgPad = QLabel()

        self.recoBtn = QPushButton("Recognition")
        self.recoBtn.clicked.connect(self.recognition)

        self.clearBtn = QPushButton("Clear")
        self.clearBtn.clicked.connect(self.paintPad.clear)

        self.loadBtn = QPushButton("LoadData")
        self.loadBtn.clicked.connect(self.loadData)

        paintLayout = QHBoxLayout()
        paintLayout.addWidget(self.paintPad)
        self.paintBox.setLayout(paintLayout)

        # binViewLayout = QHBoxLayout()
        # binViewLayout.addWidget(self.binViewLabel)
        # self.binViewBox.setLayout(binViewLayout)

        disLayout = QHBoxLayout()
        disLayout.addWidget(self.resDisplay)
        self.resBox.setLayout(disLayout)

        self.upLayout = QHBoxLayout()
        self.upLayout.addWidget(self.paintBox)
        # self.upLayout.addWidget(self.binViewBox)
        self.upLayout.addWidget(self.resBox)

        self.downLayout = QHBoxLayout()
        self.downLayout.addWidget(self.msgPad)
        self.downLayout.addWidget(self.clearBtn)
        self.downLayout.addWidget(self.recoBtn)
        self.downLayout.addWidget(self.loadBtn)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.upLayout)
        self.mainLayout.addLayout(self.downLayout)

        self.setLayout(self.mainLayout)
        self.resize(1800, 600)
        self.setWindowTitle("Hand Write Recognition By Python.")

    def loadData(self):
        self.msgPad.setText("Loading Data...")
        #Load Data
        self.dataset.loadNumData()
        self.msgPad.setText("Load Data ok.")
        #将二值化数据降维至向量
        trainingData = self.dataset.dimReduction(self.dataset.numTrainSetBin())
        trainingLabels = self.dataset.numTrainLabel().reshape((1, -1))[0]
        self.msgPad.setText("Training algorithm...")
        self.knn.fit(trainingData, trainingLabels)
        self.msgPad.setText("Training algorithm ok.")

    def showMsg(self, msg):
        self.msgPad.setText(msg)

    def recognition(self):
        testData = self.paintPad.getPaintData()
        # self.binViewLabel.clear()
        strData = str(testData)
        strData = strData.replace('0', ' ')

        # self.binViewLabel.setText(strData)
        testData = testData.reshape(1, -1)
        n = self.knn.predict(testData)
        '''
        n = knnClassify(testData[0], self.trainSetDim, trainingLabels, 3)
        '''
        self.resDisplay.clear()
        self.resDisplay.setText(str(n))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    handWrite = MainWindow()
    # handWrite= Main()
    handWrite.show()
    app.exec_()