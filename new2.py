from PySide2 import QtWidgets
from CdbsModules.cadbase_library_config import Ui_Config
import CdbsModules.CdbsEvn as CdbsEvn
import CdbsModules.DataHandler as DataHandler
from CdbsModules.CdbsAuth import CdbsAuth
from CdbsModules.Translate import translate
# from CdbsModules.ChooseFolder import ChooseFolder

class CADBaseSetting(Ui_Config, QtWidgets.QDialog):

    def __init__(self):
        super(CADBaseSetting, self).__init__()
        self.setupUi(self)
        self.setObjectName('CADBaseLibraryConfig')
        self._connect_widgets()
        self.lineEdit_3.setText(CdbsEvn.g_library_path)
        self.lineEdit.setText(CdbsEvn.g_base_api)

    def _connect_widgets(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.pushButton.clicked.connect(self.setdefaulturl)
        self.pushButton_3.clicked.connect(self.changepath)

    def setdefaulturl(self, *args, **kwargs):
        self.lineEdit.setText(CdbsEvn.g_cadbase_api)

    def changepath(self, *args, **kwargs):
        np = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            translate(
                'CadbaseMacro',
                'Local location of your existing CADBase library',
            ),
            CdbsEvn.g_library_path,
        )
        if np:
            self.lineEdit_3.setText(np)

    def reject(self, *args, **kwargs):
        DataHandler.logger('info', translate('CadbaseMacro', 'Changes not accepted'))
        # self.closeEvent()
        self.close()

    def accept(self, *args, **kwargs):
        update_settings = False
        if self.lineEdit.text():
            CdbsEvn.g_base_api = self.lineEdit.text()
            update_settings = True
        if self.lineEdit_3.text() != CdbsEvn.g_library_path:
            CdbsEvn.g_library_path = self.lineEdit_3.text()
            update_settings = True
        if update_settings:
            DataHandler.logger('error', f'update_settings')
            CdbsEvn.save()
            DataHandler.logger('error', f'BEFORE g_api_login: {CdbsEvn.g_api_login}')
            CdbsEvn.update_settings()
            DataHandler.logger('error', f'AFTER g_api_login: {CdbsEvn.g_api_login}')
        if self.lineEdit_2.text() and self.lineEdit_4.text():
            username = self.lineEdit_2.text()
            password = self.lineEdit_4.text()
            CdbsAuth(username, password)
        DataHandler.logger('info', translate('CadbaseMacro', 'Configuration updated'))
        # self.closeEvent()
        self.close()

    def closeEvent(self, *args, **kwargs):
        self.deleteLater()