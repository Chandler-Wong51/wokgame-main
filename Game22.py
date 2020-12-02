'''
Function:
	游戏开始窗口和主函数
'''
import sys
import cfg
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from modules.misc.Buttons import *
from modules.ai.playWithAI import *
from modules.online.playOnline import *
from modules.others.playWithOthers import *
#成旭测试No.1


'''游戏开始界面'''
class gameStartUI(QWidget):#继承最简单窗体
	def __init__(self, parent=None, **kwargs):
		super(gameStartUI, self).__init__(parent)#多继承防止重复定义，调用父类构造方法
		self.setFixedSize(760, 650)#由于图片大小不可拉伸窗口
		self.setWindowTitle('可圈可点组五子棋游戏')#左上角窗口文字
		self.setWindowIcon(QIcon(cfg.ICON_FILEPATH))#左上角标志图片
		# 背景图片
		palette = QPalette()#创建调色板实例
		palette.setBrush(self.backgroundRole(), QBrush(QPixmap(cfg.BACKGROUND_IMAGEPATHS.get('bg_start'))))
		self.setPalette(palette)
		# 按钮
		# --人机对战
		self.ai_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('ai'), self)
		self.ai_button.move(250, 50)#按钮位置
		self.ai_button.show()#Qlabel需要让我们看到
		self.ai_button.click_signal.connect(self.playWithAI)
		# --联机对战
		self.online_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('online'), self)
		self.online_button.move(250, 200)
		self.online_button.show()
		self.online_button.click_signal.connect(self.playOnline)
		#--人人对战
		self.others_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('others'),self)
		self.others_button.move(250, 350)
		self.others_button.show()
		self.others_button.click_signal.connect(self.playWithOthers)
		#--退出
		self.exit_button=PushButton(cfg.BUTTON_IMAGEPATHS.get('exit'),self)
		self.exit_button.move(250,500)
		self.exit_button.show()
		self.exit_button.click_signal.connect(self.exit_exit)
	'''人机对战'''
	def playWithAI(self):
		self.close()
		self.gaming_ui = playWithAIUI(cfg)
		self.gaming_ui.exit_signal.connect(lambda: sys.exit())
		self.gaming_ui.back_signal.connect(self.show)
		self.gaming_ui.show()
	'''联机对战'''
	def playOnline(self):
		self.close()
		self.gaming_ui = playOnlineUI(cfg, self)
		self.gaming_ui.show()
	'''人人对战'''
	def playWithOthers(self):
		self.close()
		self.gaming_ui = playWithOthersUI(cfg)
		self.gaming_ui.exit_signal.connect(lambda: sys.exit())
		self.gaming_ui.back_signal.connect(self.show)
		self.gaming_ui.show()
	'''退出'''
	def exit_exit(self):
		sys.exit()

'''run'''
if __name__ == '__main__':
	app = QApplication(sys.argv)
	handle = gameStartUI()
	font = QFont()
	font.setPointSize(12)
	handle.setFont(font)
	handle.show()
	sys.exit(app.exec_())
