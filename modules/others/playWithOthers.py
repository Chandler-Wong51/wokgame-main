# -!- coding: gbk-!-
'''
Function:
    ���˶�ս����ʵ��
'''
import pygame
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from itertools import product
from modules.misc.utils import *
from modules.misc.Buttons import *
from modules.misc.Chessman import *
from modules.ai.aiGobang import aiGobang


'''���˶�ս'''
class playWithOthersUI(QWidget):
    back_signal = pyqtSignal()
    exit_signal = pyqtSignal()
    send_back_signal = False
    def __init__(self, cfg, parent=None, **kwargs):
        super(playWithOthersUI, self).__init__(parent)
        self.time_label = QLabel(self)
        self.fonth = QFont('Microsoft YaHei', 13, 75)
        self.time_label = QLabel(self)
        self.time_label.setFont(self.fonth)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.move(650, 100)
        self.time_label.resize(70, 30)
        self.player_time = {'black': 300, 'white': 300}
        self.timer = QTimer(self)  # ��ʼ����ʱ��
        self.time_label.setText('05:00')
        self.timer.timeout.connect(self.operate)
        self.timer.setInterval(1000)  # ���ü�ʱ�������������λ����
        #time_model
        self.cfg = cfg
        self.setFixedSize(760, 650)
        self.setWindowTitle('���˶�ս������Ȧ�ɵ�������')
        self.setWindowIcon(QIcon(cfg.ICON_FILEPATH))
        # ����ͼƬ
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(cfg.BACKGROUND_IMAGEPATHS.get('bg_game'))))
        self.setPalette(palette)
        # ��ť
        self.home_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('home'), self)
        self.home_button.click_signal.connect(self.goHome)
        self.home_button.move(680, 10)
        self.startgame_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('startgame'), self)
        self.startgame_button.click_signal.connect(self.startgame)
        self.startgame_button.move(640, 240)
        self.regret_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('regret'), self)
        self.regret_button.click_signal.connect(self.regret)
        self.regret_button.move(640, 310)
        self.givein_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('givein'), self)
        self.givein_button.click_signal.connect(self.givein)
        self.givein_button.move(640, 380)
        # ���ӱ�־
        self.chessman_sign = QLabel(self)
        sign = QPixmap(cfg.CHESSMAN_IMAGEPATHS.get('sign'))
        self.chessman_sign.setPixmap(sign)
        self.chessman_sign.setFixedSize(sign.size())
        self.chessman_sign.show()
        self.chessman_sign.hide()
        # ����(19*19����)
        self.chessboard = [[None for i in range(19)] for _ in range(19)]
        # ��ʷ��¼(������)
        self.history_record = []
        # �Ƿ�����Ϸ��
        self.is_gaming = True
        # ʤ����
        self.winner = None
        self.winner_info_label = None
        # ��ɫ����andĿǰ�ֵ�˭����
        self.player1_color = 'white'
        self.player2_color = 'black'
        self.whoseround = self.player1_color
        # ʵ����ai
        #self.ai_player = aiGobang(self.ai_color, self.player_color)
        # ������������
        pygame.mixer.init()
        self.drop_sound = pygame.mixer.Sound(cfg.SOUNDS_PATHS.get('drop'))
    def setup_ui(self):
        self.timer.start()

    def operate(self):
        self.player_time[self.whoseround] = self.player_time[self.whoseround] - 1
        self.time_label.setText(self.change_second_to_time(self.player_time[self.whoseround]))
    def change_second_to_time(self, a):
        stra = '0' + str(a // 60) + ':' + str(a % 60).rjust(2, '0')
        return stra
    '''����������¼�-��һغ�'''
    def mousePressEvent(self, event):
        if (event.buttons() != QtCore.Qt.LeftButton) or (self.winner is not None) or(not self.is_gaming):
            return
        # ��ֻ֤�����̷�Χ����Ӧ
        if event.x() >= 50 and event.x() <= 50 + 30 * 18 + 14 and event.y() >= 50 and event.y() <= 50 + 30 * 18 + 14:
            pos = Pixel2Chesspos(event)
            # ��֤���ӵĵط�����û��������
            if self.chessboard[pos[0]][pos[1]]:
                return
            # ʵ����һ�����Ӳ���ʾ

            if self.whoseround ==self.player1_color:
                d = PushButton(self.cfg.BUTTON_IMAGEPATHS.get('turn2'), self)
                d.move(660, 170)
                d.show()
            else:
                d = PushButton(self.cfg.BUTTON_IMAGEPATHS.get('turn1'), self)
                d.move(660, 170)
                d.show()
            self.setup_ui()
            #�غϷ���ʾ
            c = Chessman(self.cfg.CHESSMAN_IMAGEPATHS.get(self.whoseround), self)
            c.move(event.pos())
            c.show()
            self.chessboard[pos[0]][pos[1]] = c
            # ������������
            self.drop_sound.play()
            # �������λ�ñ�־������λ�ý��и���
            self.chessman_sign.show()
            self.chessman_sign.move(c.pos())
            self.chessman_sign.raise_()
            # ��¼�������
            self.history_record.append([*pos, self.whoseround])
            # �Ƿ�ʤ����
            self.winner = checkWin(self.chessboard)
            if self.winner:
                self.showGameEndInfo()
                return
            # �л��غϷ�(��ʵ���Ǹ���ɫ)
            self.nextRound()
    # '''�������ͷŲ���-���õ��Իغ�'''
    # def mouseReleaseEvent(self, event):
        # if (self.winner is not None) or (self.whoseround != self.ai_color) or (not self.is_gaming):
            # return
        # self.aiAct()
    # '''�����Զ���-AI�غ�'''
    # def aiAct(self):
        # if (self.winner is not None) or (self.whoseround == self.player_color) or (not self.is_gaming):
            # return
        # next_pos = self.ai_player.act(self.history_record)
        # # ʵ����һ�����Ӳ���ʾ
        # c = Chessman(self.cfg.CHESSMAN_IMAGEPATHS.get(self.whoseround), self)
        # c.move(QPoint(*Chesspos2Pixel(next_pos)))
        # c.show()
        # self.chessboard[next_pos[0]][next_pos[1]] = c
        # # ������������
        # self.drop_sound.play()
        # # �������λ�ñ�־������λ�ý��и���
        # self.chessman_sign.show()
        # self.chessman_sign.move(c.pos())
        # self.chessman_sign.raise_()
        # # ��¼�������
        # self.history_record.append([*next_pos, self.whoseround])
        # # �Ƿ�ʤ����
        # self.winner = checkWin(self.chessboard)
        # if self.winner:
            # self.showGameEndInfo()
            # return
        # # �л��غϷ�(��ʵ���Ǹ���ɫ)
        # self.nextRound()
    # '''�ı����ӷ�'''
    def nextRound(self):
        self.whoseround = self.player1_color if self.whoseround == self.player2_color else self.player2_color
    '''��ʾ��Ϸ�������'''
    def showGameEndInfo(self):
        self.is_gaming = False
        info_img = QPixmap(self.cfg.WIN_IMAGEPATHS.get(self.winner))
        self.winner_info_label = QLabel(self)
        self.winner_info_label.setPixmap(info_img)
        self.winner_info_label.resize(info_img.size())
        self.winner_info_label.move(50, 50)
        self.winner_info_label.show()
    '''����'''
    def givein(self):
        if self.is_gaming and (self.winner is None) and (self.whoseround == self.player1_color):
            self.winner = self.player2_color
            self.showGameEndInfo()
        if self.is_gaming and (self.winner is None) and (self.whoseround == self.player2_color):
            self.winner = self.palyer1_color
            self.showGameEndInfo()
    '''����-ֻ���ҷ��غϵ�ʱ����Ի���'''
    def regret(self):
        if (self.winner is not None) or (len(self.history_record) == 0) or (not self.is_gaming) :
            return
        pre_round = self.history_record.pop(-1)
        self.chessboard[pre_round[0]][pre_round[1]].close()
        self.chessboard[pre_round[0]][pre_round[1]] = None
        c = Chessman(self.cfg.CHESSMAN_IMAGEPATHS.get(self.whoseround), self)
        c.move(QPoint(*Chesspos2Pixel(pre_round)))
        self.chessman_sign.move(c.pos())
        self.chessman_sign.show()
        self.nextRound()
        if self.whoseround == self.player1_color:
            d = PushButton(self.cfg.BUTTON_IMAGEPATHS.get('turn1'), self)
            d.move(660, 170)
            d.show()
        else:
            d = PushButton(self.cfg.BUTTON_IMAGEPATHS.get('turn2'), self)
            d.move(660, 170)
            d.show()
    '''��ʼ��Ϸ-֮ǰ�Ķ��ı����Ѿ���������'''
    def startgame(self):
        if self.is_gaming:
            return
        self.is_gaming = True
        self.whoseround = self.player_color
        for i, j in product(range(19), range(19)):
            if self.chessboard[i][j]:
                self.chessboard[i][j].close()
                self.chessboard[i][j] = None
        self.winner = None
        self.winner_info_label.close()
        self.winner_info_label = None
        self.history_record.clear()
        self.chessman_sign.hide()
    '''�رմ����¼�'''
    def closeEvent(self, event):
        if not self.send_back_signal:
            self.exit_signal.emit()
    '''������Ϸ��ҳ��'''
    def goHome(self):
        self.send_back_signal = True
        self.close()
        self.back_signal.emit()

