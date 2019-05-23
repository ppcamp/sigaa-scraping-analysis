# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'grade.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_gradeWindow(object):
    def setupUi(self, gradeWindow):
        gradeWindow.setObjectName("gradeWindow")
        gradeWindow.resize(320, 200)
        gradeWindow.setMinimumSize(QtCore.QSize(320, 187))
        self.centralwidget = QtWidgets.QWidget(gradeWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 311, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 0, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label1 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label1.setObjectName("label1")
        self.horizontalLayout.addWidget(self.label1, 0, QtCore.Qt.AlignTop)
        self.inputNumeroGrade = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.inputNumeroGrade.setObjectName("inputNumeroGrade")
        self.horizontalLayout.addWidget(self.inputNumeroGrade, 0, QtCore.Qt.AlignTop)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.btnGerarGrade = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnGerarGrade.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnGerarGrade.setObjectName("btnGerarGrade")
        self.verticalLayout.addWidget(self.btnGerarGrade)
        self.btnSalvarGrade = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnSalvarGrade.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnSalvarGrade.setObjectName("btnSalvarGrade")
        self.verticalLayout.addWidget(self.btnSalvarGrade)
        self.btnGerarDiagrama = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnGerarDiagrama.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnGerarDiagrama.setObjectName("btnGerarDiagrama")
        self.verticalLayout.addWidget(self.btnGerarDiagrama)
        gradeWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(gradeWindow)
        self.btnGerarGrade.clicked.connect(gradeWindow.close)
        self.btnSalvarGrade.clicked.connect(gradeWindow.close)
        self.btnGerarDiagrama.clicked.connect(gradeWindow.close)
        QtCore.QMetaObject.connectSlotsByName(gradeWindow)

    def retranslateUi(self, gradeWindow):
        _translate = QtCore.QCoreApplication.translate
        gradeWindow.setWindowTitle(_translate("gradeWindow", "Scraping da Grade"))
        self.label1.setText(_translate("gradeWindow", "Número da Grade"))
        self.btnGerarGrade.setText(_translate("gradeWindow", "Gerar Grade"))
        self.btnSalvarGrade.setText(_translate("gradeWindow", "Salvar Grade"))
        self.btnGerarDiagrama.setText(_translate("gradeWindow", "Gerar Diagrama"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    gradeWindow = QtWidgets.QMainWindow()
    ui = Ui_gradeWindow()
    ui.setupUi(gradeWindow)
    gradeWindow.show()
    sys.exit(app.exec_())
