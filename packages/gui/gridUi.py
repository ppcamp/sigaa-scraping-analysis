# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_gradeWindow(object):
    def updateLabel(self, l):
        self.label.setText(l)

    def updateProgress(self, v):
        """
        Update progress bar with percent value in search pre and co

        Parameters
        ----------
        v: integer
            Percentual value for search

        Example
        -------
        >> self.updateProgress(95)
        """
        self.progressBar.setProperty("value", v)

    def gerarGrade(self):
        """
        Btn gerar Grade. Trigger to call getGrid

        Example
        -------
        >> self.gerarGrade()
        """
        # self.updateLabel("teste")
        self.paa.set_codCurso(self.inputNumeroGrade.text())
        self.paa.get_Grid(self)
        self.btnSalvarGrade.setEnabled(True)

    def salvarGrade(self):
        """
        Save grid in xml file

        Example
        -------
        >> self.salvarGrade()
        """
        self.paa.xml_Grid()

    def gerarDiagrama(self):
        """
        Not implemented
        """
        self.paa.quit_webdriver()
        Main.close()

    def setupUi(self, Main, paa):
        self.paa = paa
        Main = Main

        Main.setObjectName("Main")
        Main.resize(320, 261)
        Main.setMinimumSize(QtCore.QSize(320, 200))
        self.centralwidget = QtWidgets.QWidget(Main)
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
        self.horizontalLayout.addWidget(
            self.inputNumeroGrade, 0, QtCore.Qt.AlignTop)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.btnGerarGrade = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnGerarGrade.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnGerarGrade.setObjectName("btnGerarGrade")
        self.verticalLayout.addWidget(self.btnGerarGrade)
        self.btnSalvarGrade = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnSalvarGrade.setEnabled(False)
        self.btnSalvarGrade.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnSalvarGrade.setObjectName("btnSalvarGrade")
        self.verticalLayout.addWidget(self.btnSalvarGrade)
        self.btnGerarDiagrama = QtWidgets.QPushButton(
            self.verticalLayoutWidget)
        self.btnGerarDiagrama.setEnabled(False)
        self.btnGerarDiagrama.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnGerarDiagrama.setObjectName("btnGerarDiagrama")
        self.verticalLayout.addWidget(self.btnGerarDiagrama)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 190, 311, 68))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(
            self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.progressBar = QtWidgets.QProgressBar(self.verticalLayoutWidget_2)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        Main.setCentralWidget(self.centralwidget)

        self.retranslateUi(Main)

        self.btnGerarGrade.clicked.connect(self.gerarGrade)
        self.btnSalvarGrade.clicked.connect(self.salvarGrade)
        self.btnGerarDiagrama.clicked.connect(self.gerarDiagrama)

        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWindowTitle(_translate("Main", "Scraping da Grade"))
        self.label1.setText(_translate("Main", "Número da Grade"))
        self.btnGerarGrade.setText(_translate("Main", "Gerar Grade"))
        self.btnSalvarGrade.setText(_translate("Main", "Salvar Grade"))
        self.btnGerarDiagrama.setText(_translate("Main", "Gerar Diagrama"))

        self.progressBar.setFormat(_translate("Main", "%p%"))
