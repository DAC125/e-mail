import sys
import smtpclient
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.sendButton.clicked.connect(self.clickme)
        '''self.to.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.fromlabel.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.subject.setEchoMode(QtWidgets.QLineEdit.Normal)'''
        #self.message.setEchoMode(QtWidgets.QLineEdit.Normal)

    def clickme(self):
        if self.to.text() != '' or self.fromlabel != '' or self.subject != '' or self.message != '':
            smtpclient.sendermail(self.fromlabel.text(), self.to.text().split(','), self.subject.text(), self.message.text(),"127.0.0.1",1234)
        else:
            print('datos incompletos')



    def gotocreate(self):
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)



app=QApplication(sys.argv)
mainwindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec_()