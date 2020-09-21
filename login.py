from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import Qt
import sys,time
from wechatplat import MainForm

class LoginDlg(QDialog):
    def __init__(self, parent=None):
        super(LoginDlg, self).__init__(parent)
        usr = QLabel("用户：")
        pwd = QLabel("密码：")
        self.usrLineEdit = QLineEdit()
        self.pwdLineEdit = QLineEdit()
        self.pwdLineEdit.setEchoMode(QLineEdit.Password)

        gridLayout = QGridLayout()
        gridLayout.addWidget(usr, 0, 0, 1, 1)
        gridLayout.addWidget(pwd, 1, 0, 1, 1)
        gridLayout.addWidget(self.usrLineEdit, 0, 1, 1, 3);
        gridLayout.addWidget(self.pwdLineEdit, 1, 1, 1, 3);

        okBtn = QPushButton("确定")
        cancelBtn = QPushButton("取消")
        btnLayout = QHBoxLayout()

        btnLayout.setSpacing(60)
        btnLayout.addWidget(okBtn)
        btnLayout.addWidget(cancelBtn)

        dlgLayout = QVBoxLayout()
        dlgLayout.setContentsMargins(40, 40, 40, 40)
        dlgLayout.addLayout(gridLayout)
        dlgLayout.addStretch(40)
        dlgLayout.addLayout(btnLayout)

        self.setLayout(dlgLayout)
        okBtn.clicked.connect(self.accept)
        cancelBtn.clicked.connect(self.reject)
        self.setWindowTitle("微信提案建议后台管理")
        self.resize(300, 200)

    def accept(self):
        if self.usrLineEdit.text().strip() == "lean" and self.pwdLineEdit.text() == "pims":
            super(LoginDlg, self).accept()
            print("dd")
            main.show()
        else:
            QMessageBox.warning(self,
                    "警告",
                    "用户名或密码错误！",
                    QMessageBox.Yes)
            self.usrLineEdit.setFocus()

    def reject(self):
        QMessageBox.warning(self,
                            "警告",
                            "确定退出？",
                            QMessageBox.Yes)
        sys.exit()
if __name__=="__main__":
    app=QApplication(sys.argv)
    splash = QSplashScreen(QPixmap(":/pic/src/img/1.jpg"))

    splash.show()
    font = QFont()
    font.setPointSize(16)
    font.setBold(True)
    font.setWeight(75)
    splash.setFont(font)
    splash.showMessage("正在加载。。。",Qt.AlignHCenter,Qt.red )
    time.sleep(1)
    splash.showMessage("请耐心等待，不要反复点击。。。",Qt.AlignHCenter,Qt.red )
    time.sleep(1)
    # 设置进程，启动加载页面时可以进行其他操作而不会卡死
    app.processEvents()

    win=LoginDlg()
    main=MainForm()
    win.show()
    splash.finish(win)
    sys.exit(app.exec_())