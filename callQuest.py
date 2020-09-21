import sys,datetime,re
from PyQt5.QtWidgets import QApplication,QWidget,QMessageBox,QFileDialog
from quest import Ui_Form
from callQuestadd import cquestadd
from callIdiomadd import cidiomadd
from PyQt5.QtCore import  Qt
from db import sdb


class cQuest(QWidget,Ui_Form):
    def __init__(self):
        super(cQuest,self).__init__()
        self.setupUi(self)
        self.db=sdb
        self.model=self.db.exec("select * from questiontask order by startdate desc")
        self.tableView.setModel(self.model)
        self.tableView.doubleClicked.connect(self.getappvedit)
        self.setcombolist()
        self.pushButton.clicked.connect(self.addtask)
        self.dateEdit.setMinimumDate(datetime.date.today())
        self.dateEdit_2.setMinimumDate(datetime.date.today())


    def updatedb(self,sql):
        self.db.exec(sql)
        self.tableView.setModel(self.model)


    def setcombolist(self):
        self.comboBox.addItems(['EHS', 'LEAN', 'OTHERS'])
    def addtask(self):
        tasktitle=self.lineEdit.text()
        word=re.compile('^[0-9a-zA-Z._]{1,}$')
        if not word.search(tasktitle):
            QMessageBox.warning(self, '错误', '标题不允许有特殊字符')
            return
        type=self.comboBox.currentText()
        passscore=self.lineEdit_3.text()
        startdate=self.dateEdit.date().toString("yyyy-MM-dd")
        duedate=self.dateEdit_2.date().toString("yyyy-MM-dd")
        qtype=self.comboBox_2.currentText()
        if tasktitle=='' or type=='' or passscore=='' or startdate=='' or duedate=='':
            QMessageBox.warning(self,'错误','请保证每个字段都有内容后再提交')
            return
        if not passscore.isdigit() or int(passscore)<0 or int(passscore)>100:
            QMessageBox.warning(self, '错误', '及格分数请输入0~100之间的数字')
            return
        sql="insert into questiontask(tasktitle,type,pass,startdate,duedate,qtype) values('%s','%s','%s','%s','%s','%s') "%(tasktitle,type,passscore,startdate,duedate,qtype)
        print(sql)
        self.db.query(sql)
        self.lineEdit.setText('')
        self.updatedb("select * from questiontask order by startdate desc")



    def getappvedit(self):
        id=self.tableView.currentIndex().row()
        md=self.db.model.record(id)
        qtype=md.value('qtype')
        if qtype=='填空题':
            ae=cidiomadd(md.value('Id'))
        else:
            ae = cquestadd(md.value('Id'))
        ae.taskid=md.value('Id')
        ae.lineEdit.setText( md.value('tasktitle'))
        ae.lineEdit_3.setText(str(md.value('pass')))
        ae.comboBox.addItem(md.value('type'))
        ae.comboBox.addItems(['EHS', 'LEAN', 'OTHERS'])
        ae.dateEdit.setDate(md.value('startdate'))
        ae.dateEdit_2.setDate(md.value('duedate'))
        ae.mySignal.connect(self.getDialogSignal)
        ae.setWindowModality(Qt.ApplicationModal)
        ae.exec_()

    def getDialogSignal(self,content):
        self.updatedb("select * from questiontask order by startdate desc")




if __name__=="__main__":
    app=QApplication(sys.argv)
    win=cQuest()
    win.show()
    sys.exit(app.exec_())