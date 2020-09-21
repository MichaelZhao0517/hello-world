import sys,datetime,os,requests,compressimg
from PyQt5.QtWidgets import QApplication,QMessageBox,QDialog,QFileDialog
from newsadd import Ui_Form
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal
from db import sdb


class cnewsadd(QDialog,Ui_Form):
    mySignal = pyqtSignal(str)
    def __init__(self):
        super(cnewsadd,self).__init__()
        self.setupUi(self)
        self.db = sdb
        self.p0 = ''
        self.p1 = ''
        self.p2 = ''
        self.p3 = ''
        self.pushButton.clicked.connect(lambda:self.upimg(self.pixlabel,'p0'))
        self.cb1.clicked.connect(lambda: self.upimg(self.cl1,'p1'))
        self.cb2.clicked.connect(lambda: self.upimg(self.cl2,'p2'))
        self.cb3.clicked.connect(lambda: self.upimg(self.cl3,'p3'))
        self.dateEdit.setDate(datetime.date.today())
        self.subbt.clicked.connect(self.updatetask)

    def fetchdata(self,sid):
        query=self.db.query("select * from newspaper where Id='%d'"%sid)
        if (query.next()):
            self.title.setText(query.value('title'))
            self.author.setText(query.value('author'))
            self.dateEdit.setDate(query.value('newsdate'))
            self.ct1.setText(query.value('ct1'))
            self.ct2.setText(query.value('ct2'))
            self.ct3.setText(query.value('ct3'))

            url = query.value('pic_url')
            if url!='0':
                res = requests.get(url)
                img = QImage.fromData(res.content).scaled(160, 90)
                self.pixlabel.setPixmap(QPixmap(img))
                self.p0=url

            url = query.value('url1')
            if url != '0':
                res = requests.get(url)
                img = QImage.fromData(res.content).scaled(160, 90)
                self.cl1.setPixmap(QPixmap(img))
                self.p1=url

            url = query.value('url2')
            if url!='0':
                res = requests.get(url)
                img = QImage.fromData(res.content).scaled(160, 90)
                self.cl2.setPixmap(QPixmap(img))
                self.p2=url

            url = query.value('url3')
            if url != '0':
                res = requests.get(url)
                img = QImage.fromData(res.content).scaled(160, 90)
                self.cl3.setPixmap(QPixmap(img))
                self.p3=url

    def upimg(self,pix,p):
        # md = self.db.model.record(i)
        # qid = md.value('Id')
        # url = md.value('beforepic')
        # res = requests.get(url)


        file = QFileDialog.getOpenFileName(self, '请选择需要上传的文件', 'c:\\', '*.jpg *.jpeg *.gif *.png')[0]
        if not file:
            return
        file1=compressimg.resize_image(file)
        a = file[0:file.rfind('/') + 1]
        b = file[file.rfind("."):]
        newfile=a+p+b
        if os.path.isfile(newfile):
            os.remove(newfile)
        os.rename(file1,newfile)
        # os.remove(file)
        pix.setPixmap(QPixmap(newfile).scaled(160,90))
        if p=='p0':
            self.p0=newfile
        elif p=='p1':
            self.p1=newfile
        elif p=='p2':
            self.p2=newfile
        elif p=='p3':
            self.p3=newfile



    def giveimg(self,newfile,sid):

        if newfile[:4]!='http':
            files = {'file': open(newfile, 'rb')}
            data={'sid':sid}
            response = requests.post('https://www.welean.xyz/xcx/upnews.php', files=files,data=data)
            if response.text=="Success":
                QMessageBox.information(self, '通知', newfile+"上传成功")
            else:
                QMessageBox.warning(self, '出错了', newfile + "上传失败，请联系管理员或再试一下")

    def updatetask(self):
        sid=self.sid
        if self.title.text()=='' or self.author.text()=='' or self.ct1.toPlainText()=='' or self.p0=='':
            QMessageBox.warning(self,'不符合规则','红色的格子和标题图片为必填项')
            return


        title=self.title.text()
        author=self.author.text()
        newsdate=self.dateEdit.date().toString("yyyy-MM-dd")
        ct1=self.ct1.toPlainText()
        ct2=self.ct2.toPlainText()
        ct3=self.ct3.toPlainText()
        if self.sid == 0:
            sql = "INSERT INTO `newspaper`(`title`, `author`, `newsdate`, `ct1`, `ct2`,`ct3`) VALUES ('%s','%s','%s','%s','%s','%s')" % \
                  (title,author,newsdate,ct1,ct2,ct3)
            query=self.db.query(sql)
            sid=query.lastInsertId()
            print(sql,sid)

        imgpath = "https://www.welean.xyz/xcx/newspaper/" + str(sid) + "/"
        if self.p0!='':
            if self.p0[:4]=='http':
                pic_url=self.p0
            else:
                file=self.p0
                b = file[file.rfind("."):]
                pic_url=imgpath+"p0"+b
        else:
            pic_url='0'
        if self.p1 != '':
            if self.p1[:4] == 'http':
                url1 = self.p1
            else:
                file = self.p1
                b = file[file.rfind("."):]
                url1 = imgpath + "p1" + b
        else:
            url1 = '0'
        if self.p2 != '':
            if self.p2[:4] == 'http':
                url2 = self.p2
            else:
                file = self.p2
                b = file[file.rfind("."):]
                url2 = imgpath + "p2" + b
        else:
            url2 = '0'
        if self.p3 != '':
            if self.p3[:4] == 'http':
                url3 = self.p3
            else:
                file = self.p3
                b = file[file.rfind("."):]
                url3 = imgpath + "p3" + b
        else:
            url3 = '0'

        sql="update newspaper set title='%s',author='%s',newsdate='%s',ct1='%s',ct2='%s',ct3='%s',pic_url='%s',url1='%s',url2='%s',url3='%s' where Id=%d"\
              % (title,author, newsdate, ct1, ct2, ct3, pic_url, url1, url2,url3,sid)
        self.db.querycheck(sql)
        if self.p0!='' and self.p0[:4]!='http':
            self.giveimg(self.p0,sid)
            os.remove(self.p0)
        if self.p1 != '' and self.p1[:4] != 'http':
            self.giveimg(self.p1, sid)
            os.remove(self.p1)
        if self.p2 != '' and self.p2[:4] != 'http':
            self.giveimg(self.p2, sid)
            os.remove(self.p2)
        if self.p3 != '' and self.p3[:4] != 'http':
            self.giveimg(self.p3, sid)
            os.remove(self.p3)



        self.close()



    def closeEvent(self, QCloseEvent):
        self.mySignal.emit('')  # 发射信号






if __name__=="__main__":
    app=QApplication(sys.argv)
    win=cnewsadd()
    win.show()
    sys.exit(app.exec_())