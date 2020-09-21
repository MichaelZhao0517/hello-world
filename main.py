# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(980, 700)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("华文仿宋")
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QWidget#centralwidget{border-image: url(:/pic/src/img/back.jpg);}\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.subLayout = QtWidgets.QGridLayout()
        self.subLayout.setObjectName("subLayout")
        self.verticalLayout.addLayout(self.subLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 980, 19))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.menubar.setFont(font)
        self.menubar.setStyleSheet("background-image: url(:/pic/src/img/back.jpg);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setStyleSheet("color: rgb(255, 255, 255);")
        self.menu.setTitle("菜单")
        self.menu.setSeparatorsCollapsible(False)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.toolBar.setFont(font)
        self.toolBar.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self.toolBar.setAutoFillBackground(False)
        self.toolBar.setStyleSheet("font: 10pt \"Agency FB\";\n"
"background-color: rgb(40, 50, 62);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.toolBar.setIconSize(QtCore.QSize(64, 64))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.frameclose = QtWidgets.QAction(MainWindow)
        self.frameclose.setObjectName("frameclose")
        self.appvSuggest = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pic/src/img/assign.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.appvSuggest.setIcon(icon)
        self.appvSuggest.setObjectName("appvSuggest")
        self.downloadSuggestion = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/pic/src/img/down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downloadSuggestion.setIcon(icon1)
        self.downloadSuggestion.setObjectName("downloadSuggestion")
        self.uploadTask = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/pic/src/img/tasks.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.uploadTask.setIcon(icon2)
        self.uploadTask.setObjectName("uploadTask")
        self.uploadQuestion = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/pic/src/img/question.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.uploadQuestion.setIcon(icon3)
        self.uploadQuestion.setObjectName("uploadQuestion")
        self.actionNewspaper = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/pic/src/img/complete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewspaper.setIcon(icon4)
        self.actionNewspaper.setObjectName("actionNewspaper")
        self.menu.addAction(self.frameclose)
        self.menubar.addAction(self.menu.menuAction())
        self.toolBar.addAction(self.appvSuggest)
        self.toolBar.addAction(self.downloadSuggestion)
        self.toolBar.addAction(self.uploadTask)
        self.toolBar.addAction(self.uploadQuestion)
        self.toolBar.addAction(self.actionNewspaper)

        self.retranslateUi(MainWindow)
        self.frameclose.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pentair Suggestion Management System(PSMS)"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.frameclose.setText(_translate("MainWindow", "退出"))
        self.frameclose.setToolTip(_translate("MainWindow", "退出"))
        self.frameclose.setShortcut(_translate("MainWindow", "Alt+X"))
        self.appvSuggest.setText(_translate("MainWindow", "批准提案"))
        self.appvSuggest.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#000000;\">批准提案</span></p></body></html>"))
        self.downloadSuggestion.setText(_translate("MainWindow", "下载提案"))
        self.downloadSuggestion.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#555500;\">下载提案</span></p></body></html>"))
        self.uploadTask.setText(_translate("MainWindow", "稽核任务"))
        self.uploadTask.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#555500;\">稽核任务</span></p></body></html>"))
        self.uploadQuestion.setText(_translate("MainWindow", "限时问答"))
        self.uploadQuestion.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#555500;\">限时问答</span></p></body></html>"))
        self.actionNewspaper.setText(_translate("MainWindow", "Newspaper"))


import suggestion_rc
