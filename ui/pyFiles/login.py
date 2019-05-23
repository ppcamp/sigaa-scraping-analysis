# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.setWindowModality(QtCore.Qt.NonModal)
        Login.resize(386, 137)
        Login.setMinimumSize(QtCore.QSize(386, 137))
        Login.setMaximumSize(QtCore.QSize(386, 137))
        Login.setFocusPolicy(QtCore.Qt.TabFocus)
        Login.setWindowTitle("Login")
        Login.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        Login.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(Login)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 0, 361, 67))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 10, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.txtfieldUser = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.txtfieldUser.setObjectName("txtfieldUser")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtfieldUser)
        self.labelUser = QtWidgets.QLabel(self.formLayoutWidget)
        self.labelUser.setObjectName("labelUser")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelUser)
        self.labelPsswd = QtWidgets.QLabel(self.formLayoutWidget)
        self.labelPsswd.setObjectName("labelPsswd")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelPsswd)
        self.textfieldPsswd = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.textfieldPsswd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.textfieldPsswd.setObjectName("textfieldPsswd")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.textfieldPsswd)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(110, 70, 161, 61))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnLogin = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnLogin.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnLogin.setObjectName("btnLogin")
        self.verticalLayout.addWidget(self.btnLogin)
        Login.setCentralWidget(self.centralwidget)

        self.retranslateUi(Login)
        self.btnLogin.released.connect(Login.close)
        self.btnLogin.clicked.connect(Login.setFocus)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWhatsThis(_translate("Login", "<html><head/><body><p>Login prompt, before to go for the start page</p></body></html>"))
        self.labelUser.setText(_translate("Login", "Usuário"))
        self.labelPsswd.setText(_translate("Login", "Senha"))
        self.btnLogin.setText(_translate("Login", "Entrar"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Login = QtWidgets.QMainWindow()
    ui = Ui_Login()
    ui.setupUi(Login)
    Login.show()
    sys.exit(app.exec_())
