# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cadbase_library_config.ui'
##
## Created by: Qt User Interface Compiler version 5.15.11
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_Config(object):
    def setupUi(self, Config):
        if not Config.objectName():
            Config.setObjectName(u"Config")
        Config.resize(445, 545)
        self.verticalLayout = QVBoxLayout(Config)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_3 = QGroupBox(Config)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setLineWidth(1)
        self.label.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_3 = QLineEdit(self.groupBox_3)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.horizontalLayout_2.addWidget(self.lineEdit_3)

        self.pushButton_3 = QPushButton(self.groupBox_3)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy1)
        self.pushButton_3.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.pushButton_3)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox = QGroupBox(Config)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_4.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_4.addWidget(self.pushButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)


        self.horizontalLayout.addLayout(self.verticalLayout_4)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(Config)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
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

        self.buttonBox = QDialogButtonBox(Config)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setCursor(QCursor(Qt.PointingHandCursor))
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Config)

        QMetaObject.connectSlotsByName(Config)
    # setupUi

    def retranslateUi(self, Config):
        Config.setWindowTitle(QCoreApplication.translate("Config", u"CADBase Library Configuration", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Config", u"Library path", None))
        self.label.setText(QCoreApplication.translate("Config", u"The macro will use this directory to save downloaded files. Be careful, data in this directory may be overwritten.\n"
"Changing the library path will require restarting FreeCAD.", None))
        self.lineEdit_3.setPlaceholderText(QCoreApplication.translate("Config", u"Enter the path to the local CADBase library.", None))
#if QT_CONFIG(accessibility)
        self.pushButton_3.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.pushButton_3.setText(QCoreApplication.translate("Config", u"...", None))
        self.groupBox.setTitle(QCoreApplication.translate("Config", u"Server URL", None))
        self.label_4.setText(QCoreApplication.translate("Config", u"Here you can specify the server on which the CADBase platform. Specify the server (URL or IP) if you need to connect to the unofficial CADBase platform server", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Config", u"Enter data server URL here", None))
        self.pushButton.setText(QCoreApplication.translate("Config", u"Set official", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Config", u"Authorization", None))
        self.label_2.setText(QCoreApplication.translate("Config", u"Username", None))
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("Config", u"Enter your username from the CADBase", None))
        self.label_3.setText(QCoreApplication.translate("Config", u"Password", None))
        self.lineEdit_4.setPlaceholderText(QCoreApplication.translate("Config", u"Enter your password from the CADBase", None))
    # retranslateUi

