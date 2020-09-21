from PyQt5.QtWidgets import QApplication,QMessageBox,QDialog,QMenu
from PyQt5.QtCore import  Qt
import re,sys,globelvar as gl
from news import Ui_Form
from callNewsadd import cnewsadd
from PyQt5.QtSql import QSqlDatabase  , QSqlQueryModel
class cNews(QDialog,Ui_Form):

	def __init__(self):
		super(cNews, self).__init__()
		self.setupUi(self)


		# 信号槽连接
		self.prevButton.clicked.connect(self.onPrevButtonClick)
		self.nextButton.clicked.connect(self.onNextButtonClick)
		self.addnew.clicked.connect(lambda:self.callnewsadd(0))
		self.switchPageButton.clicked.connect(self.onSwitchPageButtonClick)
	# 查询模型

		self.currentPage = 0
		# 总页数
		self.totalPage = 0		
		# 总记录数
		self.totalRecrodCount = 0
		# 每页显示记录数
		self.PageRecordCount  = 10



		self.setTableView()

		# self.tableView.resizeColumnsToContents()
		self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tableView.doubleClicked.connect(self.dbclick)
		self.tableView.customContextMenuRequested.connect(self.genmenu)

	def callnewsadd(self,sid):

		ae = cnewsadd()
		ae.sid = sid
		if sid==0:
			ae.groupBox.setTitle('添加新闻')
		else:
			ae.groupBox.setTitle('修改新闻')
			ae.fetchdata(sid)
		ae.mySignal.connect(self.getDialogSignal)
		ae.setWindowModality(Qt.ApplicationModal)
		ae.show()
	def dbclick(self):
		id = self.tableView.currentIndex().row()
		md = self.queryModel.record(id).value('Id')
		self.callnewsadd(md)


	def getDialogSignal(self, content):
		pass

	def delitem(self, i):
		md = self.queryModel.record(i)
		qid = md.value('Id')
		sql = "update newspaper set nav_url=1 where Id=%d" % (qid)
		d = self.db.exec(sql)
		if d:
			QMessageBox.information(self, '成功', '删除成功')
			self.queryModel.setQuery("select Id,newsdate,title,author,pic_url '封面图片' from newspaper where nav_url='' order by newsdate desc")

	def genmenu(self, pos):
		for i in self.tableView.selectionModel().selection().indexes():
			menu = QMenu()
			item1 = menu.addAction(u"删除")
			action = menu.exec_(self.tableView.mapToGlobal(pos))
			if action == item1:

				self.delitem(i.row())
				return
			else:
				return
	# 设置表格	
	def setTableView(self):	
		gl._init()
		self.db = QSqlDatabase.addDatabase('QMYSQL')


		self.db.setHostName(gl.get_value('HOSTNAME'))
		self.db.setPort(gl.get_value('PORT'))
		self.db.setDatabaseName(gl.get_value('DBNAME'))
		self.db.setUserName(gl.get_value('USRNAME'))
		self.db.setPassword(gl.get_value('PWD'))
		# 设置数据库名称
		# self.db.setDatabaseName('./database.db')
		# 打开数据库
		self.db.open()

		# 声明查询模型
		self.queryModel = QSqlQueryModel(self)
		# 设置当前页
		self.currentPage = 1;
		# 得到总记录数
		self.totalRecrodCount = self.getTotalRecordCount()
		# 得到总页数
		self.totalPage = self.getPageCount()
		# 刷新状态
		self.updateStatus()
		# 设置总页数文本
		self.setTotalPageLabel()
		# 设置总记录数
		self.setTotalRecordLabel()
		
		# 记录查询
		self.recordQuery(0)
		# 设置模型
		self.tableView.setModel(self.queryModel)
		self.updateStatus()
		print('totalRecrodCount=' + str(self.totalRecrodCount) )		
		print('totalPage=' + str(self.totalPage) )


	# 得到记录数	
	def getTotalRecordCount(self):			
		self.queryModel.setQuery("select Id,newsdate,title,author,pic_url '封面图片' from newspaper where nav_url='' order by newsdate desc")
		rowCount = self.queryModel.rowCount()
		print('rowCount=' + str(rowCount) )
		return rowCount
			
	# 得到页数		
	def getPageCount(self):

		if  self.totalRecrodCount % self.PageRecordCount == 0  :
			return (self.totalRecrodCount / self.PageRecordCount )
		else :
			return int((self.totalRecrodCount / self.PageRecordCount + 1))

	# 记录查询		
	def recordQuery(self, limitIndex ):	
		szQuery = ("select Id,newsdate,title,author,pic_url '封面图片' from newspaper where nav_url='' order by newsdate desc limit %d,%d" % (  limitIndex , self.PageRecordCount )  )
		print('query sql=' + szQuery )
		self.queryModel.setQuery(szQuery)
		
	# 刷新状态		
	def updateStatus(self):				
		szCurrentText = ("当前第%d页" % self.currentPage )
		print(szCurrentText)
		print(self.currentPageLabel)
		self.currentPageLabel.setText( szCurrentText )


		print('current=' + str(self.currentPage)+'tt='+str(self.totalPage))
		#设置按钮是否可用
		if self.currentPage == 1 :
			if self.totalPage==1:
				self.prevButton.setEnabled(False)
				self.nextButton.setEnabled(False)
			else:
				self.prevButton.setEnabled( False )
				self.nextButton.setEnabled( True )
		elif  self.currentPage >= self.totalPage :
			self.prevButton.setEnabled( True )
			self.nextButton.setEnabled( False )
		else :
			self.prevButton.setEnabled( True )
			self.nextButton.setEnabled( True )

	# 设置总数页文本		
	def setTotalPageLabel(self):	
		szPageCountText  = ("总共%d页" % self.totalPage )
		self.totalPageLabel.setText(szPageCountText)

	# 设置总记录数		
	def setTotalRecordLabel(self):	
		szTotalRecordText  = ("共%d条" % self.totalRecrodCount )
		print('*** setTotalRecordLabel szTotalRecordText=' + szTotalRecordText )
		self.totalRecordLabel.setText(szTotalRecordText)
		
	# 前一页按钮按下		
	def onPrevButtonClick(self):	
		print('*** onPrevButtonClick ');
		limitIndex = (self.currentPage - 2) * self.PageRecordCount
		self.recordQuery( limitIndex) 
		self.currentPage -= 1 
		self.updateStatus() 

	# 后一页按钮按下	
	def onNextButtonClick(self):
		print('*** onNextButtonClick ');
		limitIndex =  self.currentPage * self.PageRecordCount
		self.recordQuery( limitIndex) 
		self.currentPage += 1
		self.updateStatus() 
		
	# 转到页按钮按下
	def onSwitchPageButtonClick(self):			
		# 得到输入字符串
		szText = self.switchPageLineEdit.text()
		#数字正则表达式		
		pattern = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
		match = 1
		
		# 判断是否为数字
		if not match :
			QMessageBox.information(self, "提示", "请输入数字" )
			return
			
		# 是否为空
		if szText == '' :
			QMessageBox.information(self, "提示" , "请输入跳转页面" )
			return

		#得到页数
		pageIndex = int(szText)
		#判断是否有指定页
		if pageIndex > self.totalPage or pageIndex < 1 :
			QMessageBox.information(self, "提示", "没有指定的页面，请重新输入" )
			return
			
		#得到查询起始行号
		limitIndex = (pageIndex-1) * self.PageRecordCount			
			
		#记录查询
		self.recordQuery(limitIndex);
		#设置当前页
		self.currentPage = pageIndex
		#刷新状态
		self.updateStatus();
			
if __name__ == '__main__':
	app = QApplication(sys.argv)
	

	example = cNews()
	# 显示窗口
	example.show()
	
	sys.exit(app.exec_())
