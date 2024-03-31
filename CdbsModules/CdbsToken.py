from pathlib import Path
from PySide2 import QtWidgets
from CdbsModules.cadbase_library_token import Ui_Token
import CdbsModules.CdbsEvn as CdbsEvn
import CdbsModules.PartsList as PartsList
from CdbsModules.CdbsAuth import CdbsAuth
from CdbsModules.Translate import translate
from CdbsModules.Logger import logger

class CdbsToken(Ui_Token, QtWidgets.QDialog):

    def __init__(self):
        super(CdbsToken, self).__init__()
        self.setupUi(self)
        self.setObjectName('CADBaseLibraryToken')
        self._connect_widgets()

    def _connect_widgets(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def reject(self, *args, **kwargs):
        logger('info', translate('CadbaseMacro', 'Changes not accepted'))
        self.close()

    def accept(self, *args, **kwargs):
        if self.lineEdit_2.text() and self.lineEdit_4.text():
            username = self.lineEdit_2.text()
            password = self.lineEdit_4.text()
            CdbsAuth(username, password)
        logger('info', translate('CadbaseMacro', 'Configuration updated'))
        self.close()

    def closeEvent(self, *args, **kwargs):
        self.deleteLater()