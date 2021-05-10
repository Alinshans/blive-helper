import sys

from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QMessageBox
from PyQt5.QtGui import QRegExpValidator
from main_ui import Ui_MainWindow
from blive.blivethread import BLiveThread


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
        self.blivethread.start()

    def connect_room(self):
        if self.pushButton.text() == '连接':
            if self.lineEdit.text():
                room_id = int(self.lineEdit.text())
                if self.blivethread.connect_room(room_id):
                    self.pushButton.setText('断开')
                else:
                    QMessageBox.warning(self, '警告', '该房间ID不存在！')

        else:
            self.blivethread.disconnect_room()
            self.pushButton.setText('连接')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
