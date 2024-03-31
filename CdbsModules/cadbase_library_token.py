# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cadbase_library_token.ui'
##
## Created by: Qt User Interface Compiler version 5.15.11
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_Token(object):
    def setupUi(self, Token):
        if not Token.objectName():
            Token.setObjectName(u"Token")
        Token.resize(1050, 900)
        self.verticalLayout = QVBoxLayout(Token)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_2 = QGroupBox(Token)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_5.addWidget(self.label_2)

        self.lineEdit_2 = QLineEdit(self.groupBox_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.verticalLayout_5.addWidget(self.lineEdit_2)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_5.addWidget(self.label_3)

        self.lineEdit_4 = QLineEdit(self.groupBox_2)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setEchoMode(QLineEdit.Password)

        self.verticalLayout_5.addWidget(self.lineEdit_4)


        self.verticalLayout_2.addLayout(self.verticalLayout_5)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.buttonBox = QDialogButtonBox(Token)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setCursor(QCursor(Qt.PointingHandCursor))
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Token)

        QMetaObject.connectSlotsByName(Token)
    # setupUi

    def retranslateUi(self, Token):
        Token.setWindowTitle(QCoreApplication.translate("Token", u"CADBase Library Authorization", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Token", u"Authorization", None))
        self.label.setText(QCoreApplication.translate("Token", u"CADBase platform access token will be saved locally, after successful authorization.\n"
"When the authorization token expires, you will need to request a new authorization token by re-entering your username and password.", None))
        self.label_2.setText(QCoreApplication.translate("Token", u"Username", None))
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("Token", u"Enter your username from CADBase", None))
        self.label_3.setText(QCoreApplication.translate("Token", u"Password", None))
        self.lineEdit_4.setPlaceholderText(QCoreApplication.translate("Token", u"Enter your password from CADBase", None))
    # retranslateUi

