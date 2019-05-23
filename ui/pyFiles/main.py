# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from grade import Ui_gradeWindow as grade


class Ui_Login(object):
    def __init__(self, Janela):
        self.setupUi(Janela)

    def openWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = grade()
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, Janela):
        Janela.setObjectName("Janela")
        Janela.setWindowModality(QtCore.Qt.NonModal)
        Janela.resize(386, 137)
        Janela.setMinimumSize(QtCore.QSize(386, 137))
        Janela.setMaximumSize(QtCore.QSize(386, 137))
        Janela.setFocusPolicy(QtCore.Qt.TabFocus)
        Janela.setWindowTitle("Janela")
        Janela.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        Janela.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(Janela)
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
        Janela.setCentralWidget(self.centralwidget)

        self.retranslateUi(Janela)
        self.btnLogin.released.connect(Janela.hide)
        self.btnLogin.clicked.connect(self.openWindow)
        QtCore.QMetaObject.connectSlotsByName(Janela)

    def retranslateUi(self, Janela):
        _translate = QtCore.QCoreApplication.translate
        Janela.setWhatsThis(_translate("Janela", "<html><head/><body><p>Janela prompt, before to go for the start page</p></body></html>"))
        self.labelUser.setText(_translate("Janela", "Usuário"))
        self.labelPsswd.setText(_translate("Janela", "Senha"))
        self.btnLogin.setText(_translate("Janela", "Entrar"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Janela = QtWidgets.QMainWindow()

    ui = Ui_Login(Janela)
    # ui.setupUi(Janela)

    Janela.show()
    sys.exit(app.exec_())
