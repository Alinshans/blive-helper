import sys
from multipledispatch import dispatch
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QMessageBox
from PyQt5.QtGui import QRegExpValidator
from main_ui import Ui_MainWindow
from blive.blivethread import BLiveThread, RoomInfo


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        # 连接按钮
        self.pushButton.clicked.connect(self.connect_room)
        reg = QRegExp('[0-9]+$')
        validator = QRegExpValidator(self)
        validator.setRegExp(reg)
        self.lineEdit.setValidator(validator)
        # 状态栏
        self.statusbar.showMessage('未连接直播间')
        # ws线程
        self.blivethread = BLiveThread()
        self.blivethread.on_message.connect(self.on_message)
        self.blivethread.start()
        self.room_info = RoomInfo()

    @dispatch(object)
    def on_message(self, message):
        print(type(message))
        print(message)

    @dispatch(int)
    def on_message(self, message: int):
        print('handle_int_message')
        self.room_info.popularity = message
        self.update_room_info()

    @dispatch(str)
    def on_message(self, message: str):
        print('handle_str_message')
        print(message)
        if message == 'preparing':
            self.room_info.status = self.blivethread.live_status[0]
        elif message == 'live':
            self.room_info.status = self.blivethread.live_status[1]
        elif message == 'round':
            self.room_info.status = self.blivethread.live_status[2]
        self.update_room_info()

    def connect_room(self):
        if self.pushButton.text() == '连接':
            if self.lineEdit.text():
                room_id = int(self.lineEdit.text())
                self.room_info = self.blivethread.connect_room(room_id)
                if self.room_info:
                    self.pushButton.setText('断开')
                    self.update_room_info()
                else:
                    QMessageBox.warning(self, '警告', '该房间ID不存在！')
        else:
            self.blivethread.disconnect_room()
            self.pushButton.setText('连接')

    def update_room_info(self):
        if self.room_info.up_name:
            self.statusbar.showMessage(f'已连接：{self.room_info.up_name} - {self.room_info.title} | 状态：{self.room_info.status} | 人气值：{self.room_info.popularity}')
            self.setWindowTitle(f'{self.room_info.up_name} - {self.room_info.title}')
        else:
            self.statusbar.showMessage(f'已连接：{self.room_info.title} | 状态：{self.room_info.status} | 人气值：{self.room_info.popularity}')
            self.setWindowTitle(f'{self.room_info.title}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
