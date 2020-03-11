import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from numpy import *

class PaintPad(QWidget):
    def __init__(self):
        super(PaintPad, self).__init__()
        # setMouseTracking设置为False，否则不按下鼠标时也会跟踪鼠标事件
        self.setMouseTracking(False)
        '''
         要想将按住鼠标后移动的轨迹保留在窗体上
         需要一个列表来保存所有移动过的点
        '''
        self.pos_xy = []

        pal = QPalette()
        pal.setColor(QPalette.Window, Qt.white)
        self.setAutoFillBackground(True)
        self.setPalette(pal)


    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        pen = QPen(Qt.black, 50, Qt.SolidLine)
        painter.setPen(pen)

        '''
         首先判断pos_xy列表中是不是至少有两个点了
         然后将pos_xy中第一个点赋值给point_start
         利用中间变量pos_tmp遍历整个pos_xy列表
          point_end = pos_tmp
      
          判断point_end是否是断点，如果是
           point_start赋值为断点
           continue
          判断point_start是否是断点，如果是
           point_start赋值为point_end
           continue
      
          画point_start到point_end之间的线
          point_start = point_end
         这样，不断地将相邻两个点之间画线，就能留下鼠标移动轨迹了
        '''
        if len(self.pos_xy) > 1:
            point_start = self.pos_xy[0]
            for pos_tmp in self.pos_xy:
                point_end = pos_tmp

                if point_end == (-1, -1):
                    point_start = (-1, -1)
                    continue
                if point_start == (-1, -1):
                    point_start = point_end
                    continue

                painter.drawLine(point_start[0], point_start[1], point_end[0], point_end[1])
                point_start = point_end
        painter.end()

    def mouseMoveEvent(self, event):
        '''
         按住鼠标移动事件：将当前点添加到pos_xy列表中
         调用update()函数在这里相当于调用paintEvent()函数
         每次update()时，之前调用的paintEvent()留下的痕迹都会清空
        '''
        # 中间变量pos_tmp提取当前点
        pos_tmp = (event.pos().x(), event.pos().y())
        # pos_tmp添加到self.pos_xy中
        self.pos_xy.append(pos_tmp)
        self.update()

    def mouseReleaseEvent(self, event):
        '''
         重写鼠标按住后松开的事件
         在每次松开后向pos_xy列表中添加一个断点(-1, -1)
         然后在绘画时判断一下是不是断点就行了
         是断点的话就跳过去，不与之前的连续
        '''
        pos_test = (-1, -1)
        self.pos_xy.append(pos_test)
        self.update()

    def clear(self):
        self.pos_xy = []
        self.update()

    def getPaintData(self):
        '''
        将控件渲染成图片，转换成数组格式
        :return:
        '''
        imgMat = []
        fileName = "./test.png"
        fileName1 = "./test1.png"
        fileName2 = "./test2.png"
        fileName3 = "./test3.png"

        pixmap = QPixmap(self.size())
        self.render(pixmap)
        imgn = pixmap.toImage()
        imgn.save(fileName2)
        imgn_height = imgn.size().height()
        imgn_width  = imgn.size().width()
        # 有效图像的大小
        # 有效图像左上角坐标
        xPoint_left = 517
        yPoint_left = 569
        #有效图像右下角坐标
        xPoint_right = 0
        yPoint_right = 0
        height = 0
        width  = 0
        for i in range(imgn_width):
            for j in range(imgn_height):
                if(qGray(imgn.pixel(i, j)) == 0):
                    # 计算有效图像的左上角坐标点
                    if(i<xPoint_left):
                        xPoint_left = i
                    if(j<yPoint_left):
                        yPoint_left = j
                    if(i>xPoint_right):
                        xPoint_right = i
                    if(j>yPoint_right):
                        yPoint_right = j
        height = yPoint_right - yPoint_left
        width = xPoint_right - xPoint_left
        # 打印有效图像的坐标，宽度，高度
        # print(xPoint_left, yPoint_left, width, height)
        # 裁剪图片
        img_cut = imgn.copy(xPoint_left, yPoint_left, width, height)
        img_cut.save(fileName1)
        #创建一个空白的正方形图片，边长取截取图片最长的
        len = max(width, height)
        img_white = QPixmap(len, len)
        img_white.fill(Qt.white)
        img_white_p = img_white.toImage()
        #将裁剪图片融合进去

        if height >= width:
            point = (height - width)/2
            for i in range(width):
                for j in range(height):
                    img_white_p.setPixelColor(point+i, j, img_cut.pixelColor(i, j))
        else:
            point = (width - height)/2
            for i in range(width):
                for j in range(height):
                    img_white_p.setPixelColor(i, point+j, img_cut.pixelColor(i, j))
        img_white_p.save(fileName3)
        img_20_20_p = img_white_p.scaled(20, 20, Qt.IgnoreAspectRatio)
        #创建一个28*28的空图片
        img_28_28 = QPixmap(28,28)
        img_28_28.fill(Qt.white)
        img_28_28_p = img_28_28.toImage()
        #图片融合
        for i in range(20):
            for j in range(20):
                img_28_28_p.setPixelColor(4+i, 4+j, img_20_20_p.pixelColor(i,j))
        # 保存图片
        img_28_28_p.save(fileName)
        for i in range(28):
            imgRow = []
            for j in range(28):
                gary = qGray(img_28_28_p.pixel(i, j))
                if 0 == gary:
                    imgRow.append(1)
                else:
                    imgRow.append(0)
            imgMat.append(imgRow)
        imgMat = array(imgMat)
        return imgMat.T



if __name__ == "__main__":
    app = QApplication(sys.argv)
    pad = PaintPad()
    pad.show()
    app.exec_()
