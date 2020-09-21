import sys
from PyQt5.QtWidgets import QApplication,QMessageBox,QDialog,QFileDialog
from idiomaddadd import Ui_Form
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
        if self.textBrowser.toPlainText()=='' or self.answer.text()=='' or self.options.text()=='':
            QMessageBox.warning(self,'不符合规则','请填满问题，答案和选项')
            return
        if not self.answer.text() in self.options.text():
            QMessageBox.warning(self,'没有发现答案','选项中必须包含答案且答案需要在选项中连续显示')
            return
        taskid=self.taskid
        Id=self.sid
        question = self.textBrowser.toPlainText()
        answer = self.answer.text()
        options = self.options.text()

        if Id:
            sql = "update exam set answer='%s',question='%s',candidates='%s' where Id=%d"\
                  % ( answer, question,options,Id)
        else:
            sql = "insert into exam (answer,question,candidates,taskid) " \
                  "values('%s','%s','%s',%d)" % ( answer, question,options, taskid)
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