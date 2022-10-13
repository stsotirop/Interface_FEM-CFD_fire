from PyQt5.QtWidgets import QFileDialog, QMessageBox, QLineEdit, QDialogButtonBox, QDialog
from PyQt5.QtCore import QDir, QFileInfo
from PyQt5 import uic
from utils import resolve_path
from computation_core.cross_sections import create_2upn


form, base = uic.loadUiType(resolve_path("section_properties_ui/DoubleChannel.ui"))


class AddDoubleChannelUi(base, form):

    def __init__(self):
        super(base, self).__init__()
        self.pathFolder = None

    def clicker_browse(self):
        dialog = QFileDialog(self)
        if self.label_CreateFolder.text():
            dialog.setDirectory(self.label_CreateFolder.text())
        dialog.setFileMode(dialog.Directory)

        # we cannot use the native dialog, because we need control over the UI
        options = dialog.Options(dialog.DontUseNativeDialog | dialog.ShowDirsOnly)
        dialog.setOptions(options)

        def check_line_edit(_path):
            if not _path:
                return
            if _path.endswith(QDir.separator()):
                return check_line_edit(_path.rstrip(QDir.separator()))
            _path = QFileInfo(_path)
            if _path.exists() or QFileInfo(_path.absolutePath()).exists():
                button.setEnabled(True)
                return True

        # get the "Open" button in the dialog
        button = dialog.findChild(QDialogButtonBox).button(QDialogButtonBox.Open)

        # get the line edit used for the path
        line_edit = dialog.findChild(QLineEdit)
        line_edit.textChanged.connect(check_line_edit)

        # override the existing accept() method, otherwise selectedFiles() will
        # complain about selecting a non-existing path
        def accept():
            if check_line_edit(line_edit.text()):
                # if the path is acceptable, call the base accept() implementation
                QDialog.accept(dialog)

        dialog.accept = accept
        path = None
        if dialog.exec_() and dialog.selectedFiles():
            path = QFileInfo(dialog.selectedFiles()[0]).absoluteFilePath()
            self.label_CreateFolder.setText(path)
        if path:
            self.pathFolder = path

    def clicker_create_profile(self):
        h = round(float(self.lineEdit_h.text()), 3)
        b = round(float(self.lineEdit_b.text()), 3)
        tw = round(float(self.lineEdit_tw.text()), 3)
        tfl = round(float(self.lineEdit_tfl.text()), 3)
        dist = round(float(self.lineEdit_dist.text()), 3)
        profile_name = self.lineEdit_SectionName.text()
        exist_flag = create_2upn(h, b, tw, tfl, dist, self.pathFolder, profile_name)
        if exist_flag:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Section Error")
            msg.setText(f'Please define another section')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
