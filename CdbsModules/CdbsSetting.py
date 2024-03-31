from pathlib import Path
from PySide2 import QtWidgets
from CdbsModules.cadbase_library_config import Ui_Config
import CdbsModules.CdbsEvn as CdbsEvn
import CdbsModules.PartsList as PartsList
from CdbsModules.CdbsAuth import CdbsAuth
from CdbsModules.Translate import translate
from CdbsModules.Logger import logger

class CdbsSetting(Ui_Config, QtWidgets.QDialog):

    def __init__(self):
        super(CdbsSetting, self).__init__()
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
        logger('info', translate('CadbaseMacro', 'Changes not accepted'))
        self.close()

    def accept(self, *args, **kwargs):
        update_settings = False
        if self.lineEdit.text():
            CdbsEvn.g_base_api = self.lineEdit.text()
            update_settings = True
        if self.lineEdit_3.text() != CdbsEvn.g_library_path:
            CdbsEvn.g_library_path = self.lineEdit_3.text()
            PartsList.g_last_clicked_object = Path(CdbsEvn.g_library_path)
            update_settings = True
        if update_settings:
            logger('info', translate('CadbaseMacro', 'Updating settings'))
            CdbsEvn.save()
            CdbsEvn.update_settings()
            logger('info', translate('CadbaseMacro', 'Configuration updated'))
        else:
            logger('info', translate('CadbaseMacro', 'No changes found'))
        self.close()

    def closeEvent(self, *args, **kwargs):
        self.deleteLater()