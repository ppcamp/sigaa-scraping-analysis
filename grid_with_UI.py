# -*- coding: utf-8 -*-
# ===========================================================
# Grade main
# ===========================================================
from PyQt5 import QtCore, QtGui, QtWidgets

from packages.gui.gridUi import Ui_gradeWindow
from packages.sigaa.grid import GridScraping

class Ui_Main(object):

    def openGridWindow(self):
        Main.hide()
        self.paa = GridScraping()
        self.paa.login(user=self.txtfieldUser.text(),
                       password=self.textfieldPsswd.text())

        self.Main = QtWidgets.QMainWindow()
        self.ui = Ui_gradeWindow()
        self.ui.setupUi(self.Main, self.paa)
        self.Main.show()

    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.setWindowModality(QtCore.Qt.NonModal)
        Main.resize(386, 137)
        Main.setMinimumSize(QtCore.QSize(386, 137))
        Main.setMaximumSize(QtCore.QSize(386, 137))
        Main.setFocusPolicy(QtCore.Qt.TabFocus)
        Main.setWindowTitle("Login")
        Main.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        Main.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(Main)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 0, 361, 67))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 10, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.txtfieldUser = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.txtfieldUser.setObjectName("txtfieldUser")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.txtfieldUser)
        self.labelUser = QtWidgets.QLabel(self.formLayoutWidget)
        self.labelUser.setObjectName("labelUser")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.labelUser)
        self.labelPsswd = QtWidgets.QLabel(self.formLayoutWidget)
        self.labelPsswd.setObjectName("labelPsswd")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.labelPsswd)
        self.textfieldPsswd = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.textfieldPsswd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.textfieldPsswd.setObjectName("textfieldPsswd")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.textfieldPsswd)
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
        Main.setCentralWidget(self.centralwidget)
        self.retranslateUi(Main)

        self.btnLogin.clicked.connect(self.openGridWindow)

        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWhatsThis(_translate(
            "Main", "<html><head/><body><p>Login prompt, before to go for the start page</p></body></html>"))
        self.labelUser.setText(_translate("Main", "Usuário"))
        self.labelPsswd.setText(_translate("Main", "Senha"))
        self.btnLogin.setText(_translate("Main", "Entrar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Main = QtWidgets.QMainWindow()

    ui = Ui_Main()
    ui.setupUi(Main)

    Main.show()
    sys.exit(app.exec_())
