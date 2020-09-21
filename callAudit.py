import sys,xlrd,datetime
from PyQt5.QtWidgets import QApplication,QWidget,QFileDialog,QMessageBox
from audit import Ui_Form
from db import sdb


class cAudit(QWidget,Ui_Form):
    def __init__(self):
        super(cAudit,self).__init__()
        self.setupUi(self)
        self.db=sdb
        self.model=self.db.exec("select `type`,`month`,status,(select cname from userinfo where eid=owner1) as owner1, (select cname from userinfo where eid=owner2) as owner2,ehsarea from tasks order by `month` desc ")
        # print(self.model)
        self.pushButton.clicked.connect(self.upfile)
        self.tableView.setModel(self.model)
        self.setcombolist()
        self.setcombolist2()

    def upfile(self):
        file=QFileDialog.getOpenFileName(self,'请选择需要上传的文件','c:\\','*.xls *.xlsx')[0]
        if not file:
            return
        edata=xlrd.open_workbook(file)
        try:
         sheet=edata.sheet_by_name('Sheet1')
        except Exception as ex:
            print(ex)
            return
        rows = sheet.nrows
        rowlsts = [i for i in sheet.row_values(0) if i != '']
        if len(rowlsts)<=7 or sheet.row_values(0)[7]!='mehs' :
            QMessageBox.warning(self, '注意', '文件模板不正确，请使用正确模板')
            return

        for i in range(1, rows):
            try:
                if sheet.row_values(i)[0]!='':
                    type=sheet.row_values(i)[0]
                    month1=int(sheet.row_values(i)[1])

                    month= xlrd.xldate.xldate_as_datetime(month1,0)
                    ehsarea = sheet.row_values(i)[2]
                    owner1 = int(sheet.row_values(i)[3])
                    owner2 = int(sheet.row_values(i)[4])

                    sql = "insert into tasks (type,month,ehsarea,owner1,owner2,status) values('%s','%s','%s','%s','%s',0)"%(type,month,ehsarea,owner1,owner2)
                    print(sql)
                    self.db.query(sql)


            except Exception as ex:
                print(ex)


        self.updatedb("select `type`,`month`,status,(select cname from userinfo where eid=owner1) as owner1, (select cname from userinfo where eid=owner2) as owner2,ehsarea from tasks order by `month` desc ")


    def updatedb(self,sql):
        self.db.exec(sql)
        self.tableView.setModel(self.model)

    def search(self):
        cb1 = self.comboBox.currentText();
        cb2 = self.comboBox_2.currentText();


        sql = "select type,month,status,(select cname from userinfo where eid=owner1) as owner1, (select cname from userinfo where eid=owner2) as owner2,ehsarea from tasks where month='%s' and type='%s' order by month desc "%(cb2,cb1)
        print(sql)
        self.updatedb(sql)

    def setcombolist2(self):
        query=self.db.query("select type from tasks where type is not null group by type desc")

        while(query.next()):
            self.comboBox.addItem(query.value(0))
        self.comboBox.currentIndexChanged.connect(self.search)

    def setcombolist(self):
        query = self.db.query("select month from tasks where month is not null group by month desc")

        while (query.next()):
            self.comboBox_2.addItem(query.value(0).toString("yyyy-MM-dd"))
        self.comboBox_2.currentIndexChanged.connect(self.search)









if __name__=="__main__":
    app=QApplication(sys.argv)
    win=cAudit()
    win.show()
    sys.exit(app.exec_())