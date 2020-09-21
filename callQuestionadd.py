import sys
from PyQt5.QtWidgets import QApplication,QMessageBox,QDialog,QFileDialog
from questionadd import Ui_Form
from PyQt5.QtCore import pyqtSignal
from db import sdb


class cquestionadd(QDialog,Ui_Form):
    mySignal = pyqtSignal(str)
    def __init__(self):
        super(cquestionadd,self).__init__()
        self.setupUi(self)
        self.db = sdb
        self.pushButton_3.clicked.connect(self.updatetask)



    def updatetask(self):
        if self.comboBox.currentText()=='' or self.lineEdit_2.text()=='' or self.lineEdit_4.text()=='':
            QMessageBox.warning(self,'不符合规则','请至少有问题和答案和一个选项')
            return
        tasktitle=self.lineEdit.text()
        taskid=self.taskid
        Id=self.sid
        stem = self.lineEdit_2.text()
        answer = self.comboBox.currentText()
        content1 = self.lineEdit_4.text()
        content2 = self.lineEdit_5.text()
        content3 = self.lineEdit_6.text()
        content4 = self.lineEdit_7.text()
        option2 = ''
        option3 = ''
        option4 = ''

        if content2 != '':
            option2 = 'B'
        if content3 != '':
            option3 = 'C'
        if content4 != '':
            option4 = 'D'
        if Id:
            sql = "update question set answer='%s',stem='%s',content1='%s',option1='A',content2='%s',option2='%s',content3='%s',option3='%s',content4='%s',option4='%s' where Id=%d"\
                  % ( answer, stem, content1, content2, option2, content3, option3, content4, option4,Id)
        else:
            sql = "insert into question (tasktitle,answer,stem,content1,option1,content2,option2,content3,option3,content4,option4,taskid) " \
                  "values('%s','%s','%s','%s','A','%s','%s','%s','%s','%s','%s',%d)" % (tasktitle, answer, stem, content1, content2, option2, content3, option3, content4, option4, taskid)
        print(sql)

        self.db.query(sql)
        QMessageBox.information(self,'成功','成功')
        self.close()



    def closeEvent(self, QCloseEvent):
        self.mySignal.emit('')  # 发射信号






if __name__=="__main__":
    app=QApplication(sys.argv)
    win=cquestionadd()
    win.show()
    sys.exit(app.exec_())