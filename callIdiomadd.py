import sys,datetime,pymysql,pandas,os,xlrd,requests,compressimg,globelvar as gl
from PyQt5.QtWidgets import QApplication,QMessageBox,QDialog,QFileDialog,QMenu
from idiomadd import Ui_Form
from PyQt5.QtCore import  Qt
from callIdiomaddadd import cquestionadd
from PyQt5.QtCore import pyqtSignal
from db import sdb



class cidiomadd(QDialog,Ui_Form):
    mySignal = pyqtSignal(str)
    def __init__(self,taskid):
        super(cidiomadd,self).__init__()
        self.setupUi(self)
        self.db = sdb
        self.taskid=taskid
        self.model = self.db.exec("select id,question as '问题', answer as '答案',candidates as '选项',pictureUrl as '图片地址'from exam where taskid="+str(taskid))
        self.tableView.setModel(self.model)
        self.tableView.doubleClicked.connect(self.upd)
        self.tableView.resizeColumnsToContents()
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.genmenu)
        self.pushButton_3.clicked.connect(self.downloadq)
        self.pushButton.clicked.connect(self.updatetask)
        self.pushButton_4.clicked.connect(self.addnew)

    def upimg(self,i):
        md = self.db.model.record(i)
        qid = md.value('id')


        file = QFileDialog.getOpenFileName(self, '请选择需要上传的文件', 'c:\\', '*.jpg *.jpeg *.gif *.png')[0]
        if not file:
            return
        file1=compressimg.resize_image(file)
        a = file[0:file.rfind('/') + 1]
        b = file[file.rfind("."):]
        newfile=a+str(qid)+b
        self.nf=newfile
        if os.path.isfile(newfile):
            os.remove(newfile)
        os.rename(file1, newfile)
        files = {'file': open(newfile, 'rb')}
        response = requests.post('https://www.welean.xyz/xcx/uppyimg.php', files=files,data={'loc':'./idioms/'})
        imgpath="https://www.welean.xyz/xcx/idioms/"+str(qid)+b
        if response.text=='Successfully':
            sql="update exam set pictureUrl='%s' where id=%d"%(imgpath,qid)
            c=self.db.querycheck(sql)
        if c:
            QMessageBox.information(self,'通知','文件上传成功')
            self.updatedb(
                "select id,question as '问题', answer as '答案',candidates as '选项',pictureUrl as '图片地址'from exam where taskid=" + str(
                    self.taskid))



    def genmenu(self,pos):
        for i in self.tableView.selectionModel().selection().indexes():
            menu=QMenu()
            item1=menu.addAction(u"添加图片")
            menu.addSeparator()
            item2=menu.addAction('删除')
            action=menu.exec_(self.tableView.mapToGlobal(pos))
            if action==item1:

                self.upimg(i.row())
                os.remove(self.nf)
                return
            elif action==item2:

                self.delitem(i.row())
                return
            else:
                return


    def updatedb(self, sql):
        self.db.exec(sql)
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()
    def updatetask(self):
        tasktitle = self.lineEdit.text()
        type = self.comboBox.currentText()
        passscore = self.lineEdit_3.text()
        startdate = self.dateEdit.date().toString("yyyy-MM-dd")
        duedate = self.dateEdit_2.date().toString("yyyy-MM-dd")
        if tasktitle == '' or type == '' or passscore == '' or startdate == '' or duedate == '':
            QMessageBox.warning(self, '错误', '请保证每个字段都有内容后再提交')
            return
        if not passscore.isdigit() or int(passscore) < 0 or int(passscore) > 100:
            QMessageBox.warning(self, '错误', '及格分数请输入0~100之间的数字')
            return
        sql = "update questiontask set tasktitle='%s',type='%s',pass='%s',startdate='%s',duedate='%s' where Id=%d" % (tasktitle, type, passscore, startdate, duedate,self.taskid)
        print(sql)
        c=self.db.querycheck(sql)
        if c:
            QMessageBox.information(self,'提示','数据更新成功')
    def addnew(self):
        ae = cquestionadd()
        ae.taskid= self.taskid
        ae.sid=0
        ae.setWindowModality(Qt.ApplicationModal)
        ae.mySignal.connect(self.getDialogSignal)
        ae.exec_()
    def upd(self):
        id = self.tableView.currentIndex().row()
        md = self.db.model.record(id)
        ae = cquestionadd()
        ae.sid = md.value('Id')
        ae.taskid = self.taskid
        ae.groupBox.setTitle('修改问题（填空题）')
        ae.pushButton_3.setText('确定修改')
        ae.textBrowser.setText(md.value('问题'))
        ae.answer.setText(md.value('答案'))
        ae.options.setText(md.value('选项'))

        ae.mySignal.connect(self.getDialogSignal)
        ae.setWindowModality(Qt.ApplicationModal)
        ae.exec_()

    def getDialogSignal(self, content):
        self.updatedb("select id,question as '问题', answer as '答案',candidates as '选项',pictureUrl as '图片地址'from exam where taskid="+str(self.taskid))

    def closeEvent(self, QCloseEvent):
        self.mySignal.emit('')  # 发射信号


    def delitem(self,i):
        md = self.db.model.record(i)
        qid = md.value('id')
        sql="delete from exam where id=%d"%(qid)
        d=self.db.querycheck(sql)
        if d:
            QMessageBox.information(self,'成功','删除成功')
            self.updatedb(
                "select id,question as '问题', answer as '答案',candidates as '选项',pictureUrl as '图片地址'from exam where taskid=" + str(
                    self.taskid))

    def downloadq(self):
        q=QMessageBox.information(self,'即将开始下载','开始下载后，下载过程可能会等待2秒，不要拼命点击',QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if q==QMessageBox.Yes:

            self.connect = pymysql.connect(host=gl.get_value('HOSTNAME'), port=gl.get_value('PORT'),
                                           user=gl.get_value('USRNAME'),
                                           password=gl.get_value('PWD'), database=gl.get_value('DBNAME'),
                                           charset=gl.get_value('CHAR'))
            # 返回一个cursor对象,也就是游标对象
            self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)
            sql="select questionresult.Id as id,dept1,dept2,dept3,cname,testdate,score,testtimes from questionresult left join userinfo on questionresult.eid=userinfo.eid where taskid=%d"%(self.taskid)
            self.cursor.execute(sql)

            field= self.cursor.fetchall()
            if not field:
                QMessageBox.warning(self,'警告','目前并无测试记录，请稍后再试')
                return
            data = pandas.DataFrame(field)
            pandas.DataFrame.to_csv(data.set_index("id",drop=True), os.getcwd() + "/"+self.lineEdit.text()+"测试结果.csv", encoding="utf_8_sig")
            QMessageBox.about(self, '注意', '文件已经下载到程序的同一目录，请注意查看')



if __name__=="__main__":
    app=QApplication(sys.argv)
    # import qdarkstyle
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win=cidiomadd(18)
    # win.setWindowFlags(Qt.WindowStaysOnTopHint)
    win.show()
    sys.exit(app.exec_())