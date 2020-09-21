import sys,requests
from PyQt5.QtWidgets import QApplication,QWidget,QMessageBox
from appv import Ui_Form
from PyQt5.QtGui import *
from PyQt5.QtCore import  Qt
from callAppvedit import cappvedit
from db import sdb


class cAppv(QWidget,Ui_Form):
    def __init__(self):
        super(cAppv,self).__init__()
        self.setupUi(self)
        self.db=sdb
        self.model=self.db.exec("select suggest.id as id,idate,dept1,dept3,cname,beforepic,suggest.eid as eid,content from suggest left join userinfo on suggest.eid=userinfo.eid where status='open'")
        self.tableView.setModel(self.model)
        self.tableView.setColumnHidden(0,1)
        self.tableView.setColumnHidden(5, 1)
        self.tableView.doubleClicked.connect(self.getappvedit)
        self.setcombolist()


    def updatedb(self,sql):
        self.db.exec(sql)
        self.tableView.setModel(self.model)

    def search(self):
        tmp = self.comboBox.currentText();
        print(tmp)
        if(tmp!='ALL'):
            sql="select suggest.id as id,idate,dept1,dept3,cname,beforepic,suggest.eid as eid,content from suggest left join userinfo on suggest.eid=userinfo.eid where status='open' and dept1='"+tmp+"'"
        else:
            sql="select suggest.id as id,idate,dept1,dept3,cname,beforepic,suggest.eid as eid,content from suggest left join userinfo on suggest.eid=userinfo.eid where status='open'"
        self.updatedb(sql)

    def setcombolist(self):
        query=self.db.query("select dept1 from userinfo where dept1 is not null group by dept1 desc")
        self.comboBox.addItem('ALL')
        while(query.next()):
            self.comboBox.addItem(query.value(0))
        self.comboBox.currentIndexChanged.connect(self.search)



    def getappvedit(self):
        id=self.tableView.currentIndex().row()
        md=self.db.model.record(id)
        ae=cappvedit()
        ae.sid=md.value('id')
        ae.eid = md.value('eid')
        ae.idate = md.value('idate')
        ae.lineEdit.setText( md.value('dept1'))
        ae.lineEdit_2.setText(md.value('cname'))
        ae.textEdit.setText(md.value('content'))
        url = md.value('beforepic')
        res = requests.get(url)
        img = QImage.fromData(res.content).scaled(500,300)
        ae.pixlabel.setPixmap(QPixmap(img))
        ae.mySignal.connect(self.getDialogSignal)
        ae.setWindowModality(Qt.ApplicationModal)
        ae.exec_()

    def getDialogSignal(self,content):
        self.updatedb("select suggest.id as id,idate,dept1,dept3,cname,beforepic,suggest.eid as eid,content from suggest left join userinfo on suggest.eid=userinfo.eid where status='open'")




if __name__=="__main__":
    app=QApplication(sys.argv)
    win=cAppv()
    win.show()
    sys.exit(app.exec_())