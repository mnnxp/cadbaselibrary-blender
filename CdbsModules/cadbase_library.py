# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cadbase_library.ui'
##
## Created by: Qt User Interface Compiler version 5.15.11
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_CADBaseLibrary(object):
    def setupUi(self, CADBaseLibrary):
        if not CADBaseLibrary.objectName():
            CADBaseLibrary.setObjectName(u"CADBaseLibrary")
        CADBaseLibrary.resize(0, 0)
        self.verticalLayout = QVBoxLayout(CADBaseLibrary)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.folder = QTreeView(CADBaseLibrary)
        self.folder.setObjectName(u"folder")
        self.folder.setHeaderHidden(True)

        self.verticalLayout.addWidget(self.folder)

        self.toolBox = QToolBox(CADBaseLibrary)
        self.toolBox.setObjectName(u"toolBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setAcceptDrops(False)
        self.previewframe = QWidget()
        self.previewframe.setObjectName(u"previewframe")
        self.previewframe.setGeometry(QRect(0, 0, 0, 0))
        self.preview = QLabel(self.previewframe)
        self.preview.setObjectName(u"preview")
        self.preview.setGeometry(QRect(10, 0, 350, 128))
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.preview.sizePolicy().hasHeightForWidth())
        self.preview.setSizePolicy(sizePolicy1)
        self.preview.setScaledContents(False)
        self.toolBox.addItem(self.previewframe, u"Preview")
        self.optbuttons = QWidget()
        self.optbuttons.setObjectName(u"optbuttons")
        self.optbuttons.setGeometry(QRect(0, 0, 0, 0))
        self.updatebutton = QToolButton(self.optbuttons)
        self.updatebutton.setObjectName(u"updatebutton")
        self.updatebutton.setGeometry(QRect(0, 10, 230, 32))
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.updatebutton.sizePolicy().hasHeightForWidth())
        self.updatebutton.setSizePolicy(sizePolicy2)
        self.updatebutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.configbutton = QToolButton(self.optbuttons)
        self.configbutton.setObjectName(u"configbutton")
        self.configbutton.setGeometry(QRect(0, 110, 230, 32))
        sizePolicy2.setHeightForWidth(self.configbutton.sizePolicy().hasHeightForWidth())
        self.configbutton.setSizePolicy(sizePolicy2)
        self.configbutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.uploadbutton = QToolButton(self.optbuttons)
        self.uploadbutton.setObjectName(u"uploadbutton")
        self.uploadbutton.setGeometry(QRect(0, 60, 230, 32))
        sizePolicy2.setHeightForWidth(self.uploadbutton.sizePolicy().hasHeightForWidth())
        self.uploadbutton.setSizePolicy(sizePolicy2)
        self.uploadbutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.toolBox.addItem(self.optbuttons, u"Options")

        self.verticalLayout.addWidget(self.toolBox)


        self.retranslateUi(CADBaseLibrary)

        self.toolBox.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(CADBaseLibrary)
    # setupUi

    def retranslateUi(self, CADBaseLibrary):
        CADBaseLibrary.setWindowTitle(QCoreApplication.translate("CADBaseLibrary", u"CADBase Library", None))
        self.preview.setText("")
        self.toolBox.setItemText(self.toolBox.indexOf(self.previewframe), QCoreApplication.translate("CADBaseLibrary", u"Preview", None))
        self.updatebutton.setText(QCoreApplication.translate("CADBaseLibrary", u"Update components", None))
        self.configbutton.setText(QCoreApplication.translate("CADBaseLibrary", u"Settings", None))
        self.uploadbutton.setText(QCoreApplication.translate("CADBaseLibrary", u"Upload files", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.optbuttons), QCoreApplication.translate("CADBaseLibrary", u"Options", None))
    # retranslateUi

