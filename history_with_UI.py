# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from packages.sigaa.history import HistoryScraping


class Ui_Grade(object):
    def callBtnLogin(self):
        self.paa = HistoryScraping()
        self.paa.login(user=self.inputUser.text(),
                       password=self.inputPsswd.text())

        self.btnGetHistory.setEnabled(True)

    def callBtnHistory(self):
        self.paa.get_History()
        self.btnGenerateXml.setEnabled(True)
        self.btnGenerateDiagram.setEnabled(True)

    def callBtnXml(self):
        self.paa.xml_History()

    def callBtnDiagram(self):
        pass

    def setupUi(self, Grade):
        Grade.setObjectName("Grade")
        Grade.resize(335, 290)
        Grade.setMinimumSize(QtCore.QSize(335, 290))
        Grade.setMaximumSize(QtCore.QSize(335, 290))
        self.centralwidget = QtWidgets.QWidget(Grade)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 0, 331, 81))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(10, 10, 10, 10)
        self.formLayout.setHorizontalSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.labelUser = QtWidgets.QLabel(self.formLayoutWidget)
        self.labelUser.setObjectName("labelUser")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.labelUser)
        self.inputUser = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.inputUser.setObjectName("inputUser")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.inputUser)
        self.labelPsswd = QtWidgets.QLabel(self.formLayoutWidget)
        self.labelPsswd.setObjectName("labelPsswd")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.labelPsswd)
        self.inputPsswd = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.inputPsswd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.inputPsswd.setObjectName("inputPsswd")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.inputPsswd)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 80, 331, 201))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnLogin = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnLogin.setObjectName("btnLogin")
        self.verticalLayout.addWidget(self.btnLogin)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.btnGetHistory = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnGetHistory.setEnabled(False)
        self.btnGetHistory.setObjectName("btnGetHistory")
        self.verticalLayout.addWidget(self.btnGetHistory)
        self.btnGenerateXml = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnGenerateXml.setEnabled(False)
        self.btnGenerateXml.setObjectName("btnGenerateXml")
        self.verticalLayout.addWidget(self.btnGenerateXml)
        self.btnGenerateDiagram = QtWidgets.QPushButton(
            self.verticalLayoutWidget)
        self.btnGenerateDiagram.setEnabled(False)
        self.btnGenerateDiagram.setObjectName("btnGenerateDiagram")
        self.verticalLayout.addWidget(self.btnGenerateDiagram)
        Grade.setCentralWidget(self.centralwidget)

        self.btnLogin.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnGetHistory.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnGenerateXml.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnGenerateDiagram.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


        self.retranslateUi(Grade)

        self.btnLogin.clicked.connect(self.callBtnLogin)
        self.inputPsswd.returnPressed.connect(self.callBtnLogin)

        self.btnGetHistory.clicked.connect(self.callBtnHistory)
        self.btnGenerateXml.clicked.connect(self.callBtnXml)
        self.btnGenerateDiagram.clicked.connect(self.callBtnDiagram)



        QtCore.QMetaObject.connectSlotsByName(Grade)

    def retranslateUi(self, Grade):
        _translate = QtCore.QCoreApplication.translate
        Grade.setWindowTitle(_translate("Grade", "Grade"))
        self.labelUser.setText(_translate("Grade", "Usuário"))
        self.labelPsswd.setText(_translate("Grade", "Senha"))
        self.btnLogin.setText(_translate("Grade", "Entrar"))
        self.btnGetHistory.setText(_translate("Grade", "Obter Histórico"))
        self.btnGenerateXml.setText(_translate("Grade", "Gerar XML"))
        self.btnGenerateDiagram.setText(_translate("Grade", "Gerar Diagrama"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Grade = QtWidgets.QMainWindow()
    ui = Ui_Grade()
    ui.setupUi(Grade)
    Grade.show()
    sys.exit(app.exec_())
