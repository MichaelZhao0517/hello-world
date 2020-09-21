import sys,pymysql,os,pandas,globelvar as gl
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox
from main import Ui_MainWindow
from callAppv import cAppv
from callAudit import cAudit
from callQuest import cQuest
from callnews import cNews

class MainForm(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainForm,self).__init__()
        self.setupUi(self)
        self.appv=cAppv()
        self.auditform=cAudit()
        self.questform=cQuest()
        self.newspaper = cNews()
        self.appvSuggest.triggered.connect(self.appvShow)
        self.uploadTask.triggered.connect(self.auditShow)
        self.downloadSuggestion.triggered.connect(self.downloadsug)
        self.uploadQuestion.triggered.connect(self.quest)
        self.actionNewspaper.triggered.connect(self.news)

    def news(self):
        self.auditform.hide()
        self.questform.hide()
        self.appv.hide()
        self.subLayout.addWidget(self.newspaper)
        self.newspaper.queryModel.setQuery("select Id,newsdate,title,author,pic_url '封面图片' from newspaper where nav_url='' order by newsdate desc")
        self.newspaper.show()
    def appvShow(self):
        self.auditform.hide()
        self.questform.hide()
        self.newspaper.hide()
        self.subLayout.addWidget(self.appv)
        self.appv.updatedb("select suggest.id as id,idate,dept1,dept3,cname,beforepic,suggest.eid as eid,content from suggest left join userinfo on suggest.eid=userinfo.eid where status='open'")
        self.appv.show()

    def quest(self):
        self.auditform.hide()
        self.appv.hide()
        self.newspaper.hide()
        self.subLayout.addWidget(self.questform)
        self.questform.updatedb("select * from questiontask order by startdate desc")
        self.questform.show()

    def auditShow(self):
        self.appv.hide()
        self.questform.hide()
        self.newspaper.hide()
        self.subLayout.addWidget(self.auditform)
        self.auditform.updatedb("select `type`,`month`,ehsarea,(select cname from userinfo where eid=owner1) as owner1, (select cname from userinfo where eid=owner2) as owner2,status from tasks order by `month` desc ")
        self.auditform.show()

    def downloadsug(self):
        q=QMessageBox.information(self,'即将开始下载','开始下载提案后，下载过程可能会等待2秒，不要拼命点击',QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if q==QMessageBox.Yes:
            gl._init()
            self.connect = pymysql.connect(host=gl.get_value('HOSTNAME'), port=gl.get_value('PORT'), user=gl.get_value('USRNAME'),
                                           password=gl.get_value('PWD'), database=gl.get_value('DBNAME'),
                                           charset=gl.get_value('CHAR'))
            # 返回一个cursor对象,也就是游标对象
            self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)
            self.cursor.execute("SELECT id as '提案ID',A.cname as '提案人',A.dept1 as '提案部门',idate as '提案日期',B.cname as '执行人',B.dept1 as '执行部门',content as '内容',status as '状态',acdate as '确认日期',duedate,cfdate as '完成日期',type as '类别',type2 as '类别2',fifi,cancel as 备注 FROM `suggest` left join `userinfo` as A on suggest.eid=A.eid left join `userinfo` as B on suggest.exeid=B.eid")
            field= self.cursor.fetchall()
            data = pandas.DataFrame(field)
            pandas.DataFrame.to_csv(data, os.getcwd() + "/suggest.csv", encoding="utf_8_sig",index=None)
            QMessageBox.about(self, '注意', '文件已经下载到程序的同一目录，请注意查看')


if __name__=="__main__":
    app=QApplication(sys.argv)
    win=MainForm()
    # styleFile = "./src/qss/QDarkStyleSheet.qss"
    # qssStyle = gl.readQss(styleFile)
    # win.setStyleSheet(qssStyle)

    win.show()

    sys.exit(app.exec_())