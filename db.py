from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel,QSqlQuery
import globelvar as gl

class sdb:
    def __init__(self):
        self.db = QSqlDatabase.addDatabase('QMYSQL')
        self.model = QSqlQueryModel()  # 1
        self.connect()



    def connect(self):
        # print(QSqlDatabase.drivers())
        gl._init()
        self.db.setHostName(gl.get_value('HOSTNAME'))
        self.db.setPort(gl.get_value('PORT'))
        self.db.setDatabaseName(gl.get_value('DBNAME'))
        self.db.setUserName(gl.get_value('USRNAME'))
        self.db.setPassword(gl.get_value('PWD'))

        # self.db.setHostName('111.231.82.68')
        # self.db.setPort(8000)
        # self.db.setDatabaseName('suggestion')
        # self.db.setUserName('pentairSuggest')
        # self.db.setPassword('Zhao.jiayun_0217')

        if not self.db.open():
           print(self.db.lastError().text())

    def close(self):
        self.db.close()
        print("db closed")


    def exec(self,sql):

        self.model.setQuery(sql)
        return self.model

    def query(self,sql):
        query = QSqlQuery(self.db)
        query.exec(sql)
        return query
    def querycheck(self,sql):
        query = QSqlQuery(self.db)
        return query.exec(sql)


sdb=sdb()
if __name__=="__main__":
    db=sdb()

