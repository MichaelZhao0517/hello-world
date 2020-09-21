import sys,datetime,pymysql,pandas,os,xlrd,requests,compressimg,globelvar as gl,re
from PyQt5.QtWidgets import QApplication,QMessageBox,QDialog,QFileDialog,QMenu
from questadd import Ui_Form
from PyQt5.QtCore import  Qt
from callQuestionadd import cquestionadd
from PyQt5.QtCore import pyqtSignal
from db import sdb



class cquestadd(QDialog,Ui_Form):
    mySignal = pyqtSignal(str)
    def __init__(self,taskid):
        super(cquestadd,self).__init__()
        self.setupUi(self)
        self.db = sdb
        self.model = self.db.exec("select Id,stem as '问题', answer as '答案',content1 as '选项A',content2 as '选项B',content3 as '选项C',content4 as '选项D',img as '图片地址'from question where taskid="+str(taskid))
        self.tableView.setModel(self.model)
        self.tableView.doubleClicked.connect(self.upd)
        self.tableView.resizeColumnsToContents()
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.genmenu)
        self.pushButton_3.clicked.connect(self.downloadq)
        self.pushButton.clicked.connect(self.updatetask)
        self.pushButton_2.clicked.connect(self.upfile)
        self.pushButton_4.clicked.connect(self.addnew)

    def upimg(self,i):
        md = self.db.model.record(i)
        qid = md.value('Id')


        file = QFileDialog.getOpenFileName(self, '请选择需要上传的文件', 'c:\\', '*.jpg *.jpeg *.gif *.png')[0]
        if not file:
            return
        file1=compressimg.resize_image(file)
        a = file[0:file.rfind('/') + 1]
        b = file[file.rfind("."):]
        newfile=a+str(qid)+b
        if os.path.isfile(newfile):
            os.remove(newfile)
        os.rename(file1, newfile)
        files = {'file': open(newfile, 'rb')}
        response = requests.post('https://www.welean.xyz/xcx/uppyimg.php', files=files,data={'loc':'./questions/'})
        imgpath="https://www.welean.xyz/xcx/questions/"+str(qid)+b
        if response.text=='Successfully':
            sql="update question set img='%s' where Id=%d"%(imgpath,qid)
            c=self.db.querycheck(sql)
        if c:
            QMessageBox.information(self,'通知','文件上传成功')
            self.updatedb( "select Id,stem as '问题', answer as '答案',content1 as '选项A',content2 as '选项B',content3 as '选项C',content4 as '选项D',img as '图片地址'from question where taskid=%d" % (self.taskid))


    def genmenu(self,pos):
        for i in self.tableView.selectionModel().selection().indexes():
            menu=QMenu()
            item1=menu.addAction(u"添加图片")
            menu.addSeparator()
            item2=menu.addAction('删除')
            action=menu.exec_(self.tableView.mapToGlobal(pos))
            if action==item1:

                self.upimg(i.row())
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
        word=re.compile('^[0-9a-zA-Z._]{1,}$')
        if not word.search(tasktitle):
            QMessageBox.warning(self, '错误', '标题不允许有特殊字符')
            return
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
        ae.lineEdit.setText(self.lineEdit.text())
        ae.setWindowModality(Qt.ApplicationModal)
        ae.mySignal.connect(self.getDialogSignal)
        ae.comboBox.addItems(['A', 'B', 'C', 'D'])
        ae.exec_()
    def upd(self):
        id = self.tableView.currentIndex().row()
        md = self.db.model.record(id)
        ae = cquestionadd()
        ae.sid = md.value('Id')
        ae.taskid = self.taskid
        ae.lineEdit.setText(self.lineEdit.text())
        ae.groupBox.setTitle('修改问题')
        ae.pushButton_3.setText('确定修改')
        ae.lineEdit_2.setText(md.value('问题'))
        ae.lineEdit_4.setText(md.value('选项A'))
        ae.lineEdit_5.setText(md.value('选项B'))
        ae.lineEdit_6.setText(md.value('选项C'))
        ae.lineEdit_7.setText(md.value('选项D'))
        ae.comboBox.addItem(md.value('答案'))
        ae.comboBox.addItems(['A', 'B', 'C', 'D'])
        ae.mySignal.connect(self.getDialogSignal)
        ae.setWindowModality(Qt.ApplicationModal)
        ae.exec_()

    def getDialogSignal(self, content):
        self.updatedb("select Id,stem as '问题', answer as '答案',content1 as '选项A',content2 as '选项B',content3 as '选项C',content4 as '选项D',img as '图片地址'from question where taskid="+str(self.taskid))

    def closeEvent(self, QCloseEvent):
        self.mySignal.emit('')  # 发射信号

    def upfile(self):
        file = QFileDialog.getOpenFileName(self, '请选择需要上传的文件', 'c:\\', '*.xls *.xlsx')[0]
        if not file:
            return
        edata = xlrd.open_workbook(file)
        try:
            sheet = edata.sheet_by_name('Sheet1')
        except Exception as ex:
            print(ex)
            return
        rows = sheet.nrows
        if  sheet.row_values(0)[0] != '题目':
            QMessageBox.warning(self, '注意', '文件模板不正确，请使用正确模板')
            return
        taskid=self.taskid
        tasktitle=self.lineEdit.text()
        sql="delete from question where taskid=%d"%(taskid)

        self.db.querycheck(sql)
        for i in range(1, rows):
            try:
                if sheet.row_values(i)[0] != '':
                    stem = sheet.row_values(i)[0]
                    answer = sheet.row_values(i)[1]
                    content1 = sheet.row_values(i)[2]
                    content2 = sheet.row_values(i)[3]
                    content3 = sheet.row_values(i)[4]
                    content4 = sheet.row_values(i)[5]
                    option2=''
                    option3=''
                    option4=''

                    if answer=='' or content1=='':
                        continue
                    else:
                        if content2 != '':
                            option2 ='B'
                        if content3 != '':
                            option3 = 'C'
                        if content4 != '':
                            option4 = 'D'



                        sql = "insert into question (tasktitle,answer,stem,content1,option1,content2,option2,content3,option3,content4,option4,taskid) " \
                              "values('%s','%s','%s','%s','A','%s','%s','%s','%s','%s','%s',%d)" % ( tasktitle, answer,stem,content1,content2,option2,content3,option3,content4,option4,taskid)

                        self.db.query(sql)


            except Exception as ex:
                print(ex)

        self.updatedb("select Id,stem as '问题', answer as '答案',content1 as '选项A',content2 as '选项B',content3 as '选项C',content4 as '选项D',img as '图片地址'from question where taskid=%d"%(taskid))


    def delitem(self,i):
        md = self.db.model.record(i)
        qid = md.value('Id')
        sql="delete from question where Id=%d"%(qid)
        d=self.db.querycheck(sql)
        if d:
            QMessageBox.information(self,'成功','删除成功')
            self.updatedb( "select Id,stem as '问题', answer as '答案',content1 as '选项A',content2 as '选项B',content3 as '选项C',content4 as '选项D',img as '图片地址'from question where taskid=%d" % (self.taskid))




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
    win=cquestadd()
    win.show()
    sys.exit(app.exec_())