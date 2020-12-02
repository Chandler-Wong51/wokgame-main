'''
Function:
    定义按钮类
'''
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


'''定义按钮类'''
class PushButton(QLabel):
    click_signal = pyqtSignal()#类属性，所有实例间公用属性
    need_emit = False
    def __init__(self, imagepaths, parent=None, **kwargs):
        super(PushButton, self).__init__(parent)
        self.image_0 = QPixmap(imagepaths[0])
        self.image_1 = QPixmap(imagepaths[1])
        self.image_2 = QPixmap(imagepaths[2])
        self.resize(self.image_0.size())#按钮大小和图片大小相同
        self.setPixmap(self.image_0)#初始按钮画面
        self.setMask(self.image_1.mask())#？？？
    '''鼠标进入按钮范围内'''
    def enterEvent(self, event):
        self.setPixmap(self.image_1)
    '''鼠标离开按钮范围内'''
    def leaveEvent(self, event):
        self.setPixmap(self.image_0)
    '''鼠标左键点击操作'''
    def mousePressEvent(self, event):#？？？
        if event.buttons() == QtCore.Qt.LeftButton:
            self.need_emit = True
            self.setPixmap(self.image_2)
    '''鼠标左键释放操作'''
    def mouseReleaseEvent(self, event):
        if self.need_emit:
            self.need_emit = False
            self.setPixmap(self.image_1)
            self.click_signal.emit()
