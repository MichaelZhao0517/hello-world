import sys,datetime
import templatemessage
from PyQt5.QtWidgets import QApplication,QWidget,QMessageBox,QDialog
from appvedit import Ui_appvEdit
from PyQt5.QtCore import pyqtSignal
from db import sdb


class cappvedit(QDialog,Ui_appvEdit):
    mySignal = pyqtSignal(str)
    def __init__(self,parent = None):
        super(cappvedit,self).__init__(parent)
        self.setupUi(self)
        self.db = sdb
        self.pushButton.clicked.connect(self.appv)
        self.pushButton_2.clicked.connect(self.neg)
        self.comboBox.addItems(['安全','5S','质量','交货','成本','效率','事务'])
        self.comboBox_2.addItems(['内务环境','环境','工具','劳动防护','机器','设备','程序','标准','人机工程','身体位置','意识','培训'])
        self.comboBox.currentIndexChanged.connect(self.cb1change)
        self.setcombolist()
        self.dateEdit.setMinimumDate(datetime.date.today())



    def neg(self):
        neginfo=self.textEdit_2.toPlainText()
        sid=self.sid
        print(neginfo)
        if(neginfo==''):
            QMessageBox.about(self, '注意', '请填写否决原因后再否决')


        else:
            sql = "UPDATE `suggest` SET `status`='cancel',`cancel`='%s' WHERE `ID` =%d"%(neginfo,sid)
            self.db.querycheck(sql)
            self.close()

    def appv(self):
        exeid=self.lineEdit_3.text()
        sql = "SELECT eid FROM userInfo WHERE  cname = '%s'"%(exeid)
        query=self.db.query(sql)

        if(query.next()):
            self.lineEdit_3.setText(query.value('eid'))

            self.updatesuggest()
            self.close()
        else:
            QMessageBox.about(self, '注意', '没有找到该员工，请确认')
            return

    def closeEvent(self, QCloseEvent):

        self.mySignal.emit('')  # 发射信号
    def updatesuggest(self):
        typea=self.comboBox.currentText()
        exeid=self.lineEdit_3.text()
        linename = self.comboBox_5.currentText()
        duedate=self.dateEdit.date().toString("yyyy-MM-dd")
        td=datetime.date.today()
        sid=self.sid
        eid = self.eid

        if(self.radioButton.isChecked()):
            fifi='是'
        else:
            fifi='否'
        if(typea=='安全'):
            c=self.comboBox_2.currentText()
            sql="UPDATE `suggest` SET `exeid`='%s',`linename`='%s',`fifi`='%s',`status`='ongoing',`type`='安全',`type2`='%s',`duedate`='%s',`depend`=2 WHERE `ID` =%d"%(exeid,linename,fifi,c,duedate,sid)

        else:
            c=typea
            sql = "UPDATE `suggest` SET `exeid`='%s',`linename`='%s',`fifi`='%s',`status`='ongoing',`type`='%s',`duedate`='%s',`depend`=2 WHERE `ID` =%d" % (exeid, linename, fifi, c, duedate, sid)

        print(c,exeid,linename,duedate,fifi,sid,eid)
        self.db.querycheck(sql)
        # 加分
        sql = "INSERT INTO `getscore`(`eid`, `getdate`, `getid`, `gettype`, `getscore`) VALUES ('%s','%s',%d,'批准',10)"%(eid,td,sid)

        self.db.querycheck(sql)

        sql ="UPDATE `score` SET `suggestscore`=`suggestscore`+10,`score`=`score`+10 where `eid`='%s'"%(eid)
        print(sql)
        tt=self.db.querycheck(sql)
        if(not tt):

            sql = "INSERT INTO `score`(`eid`, `suggestscore`, `score`) VALUES ('$s',10,10)"%(eid)
            self.db.querycheck(sql)
        # 发送模板消息
        sql = "SELECT `wxid`,`cname` FROM `acinfo` left join `userinfo` on acinfo.eid=userinfo.eid WHERE  acinfo.EID ='%s'"%(exeid)
        query=self.db.query(sql)
        if(query.next()):

            openid=query.value('wxid')
            cname=query.value('cname')
            ad=[self.textEdit.toPlainText()[0:20],cname,self.idate.toString("yyyy-MM-dd"),duedate,'待处理']
            templatemessage.aform3(ad,openid)

        sql = "SELECT `wxid` FROM `acinfo` WHERE  acinfo.EID ='%s'"%(eid)
        query=self.db.query(sql)
        if(query.next()):
            openid=query.value('wxid')
            ad=['已批准',self.textEdit.toPlainText()[0:20],td.strftime('%Y-%m-%d'),self.idate.toString("yyyy-MM-dd"),'无']
            templatemessage.aform2(ad,openid)







    def cb1change(self):
        t=self.comboBox.currentText()
        if(t!='安全'):
            self.comboBox_2.setHidden(1)
        else:
            self.comboBox_2.setHidden(0)

    def setcombolist(self):
            query=self.db.query("select vsm from line  group by vsm order by Id desc")
            while(query.next()):
                self.comboBox_3.addItem(query.value(0))
            self.searchcb3()
            self.comboBox_3.currentIndexChanged.connect(self.searchcb3)
            self.comboBox_4.currentIndexChanged.connect(self.searchcb4)

    def searchcb3(self):
        cb3 = self.comboBox_3.currentText();
        self.comboBox_4.clear()
        query = self.db.query("select area from line  where vsm='" + cb3 + "'  group by area")
        while (query.next()):
            self.comboBox_4.addItem(query.value(0))
        self.searchcb4()
    def searchcb4(self):
        cb4 = self.comboBox_4.currentText()
        self.comboBox_5.clear()
        query = self.db.query("select linename from line  where area='" + cb4 + "'  group by linename")
        while (query.next()):
            self.comboBox_5.addItem(query.value(0))




if __name__=="__main__":
    app=QApplication(sys.argv)
    win=cappvedit()
    win.show()
    sys.exit(app.exec_())