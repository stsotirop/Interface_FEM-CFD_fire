from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5 import uic
from utils import resolve_path
from section_properties_ui.Angle import AddAngleUi
from section_properties_ui.Channel import AddChannelUi
from section_properties_ui.DoubleAngle import AddDoubleAngleUi
from section_properties_ui.DoubleChannel import AddDoubleChannelUi
from section_properties_ui.Cruciform4Angle import AddCruciform4AngleUi
from section_properties_ui.Cruciform2Angle import AddCruciform2AngleUi
from section_properties_ui.Cruciform import AddCruciformUi
from section_properties_ui.Isection import AddIsectionUi
from section_properties_ui.Tee import AddTeeUi


form, base = uic.loadUiType(resolve_path("AddPropertyWindow.ui"))


class AddPropertyUi(QMainWindow, form):

    def __init__(self):
        super(AddPropertyUi, self).__init__()
        self.setupUi(self)
        self.window_add_angle = QDialog()
        self.ui_add_angle = AddAngleUi()
        self.window_add_double_angle = QDialog()
        self.ui_add_double_angle = AddDoubleAngleUi()
        self.window_add_channel = QDialog()
        self.ui_add_channel = AddChannelUi()
        self.window_add_double_channel = QDialog()
        self.ui_add_double_channel = AddDoubleChannelUi()
        self.window_add_cruciform4angle = QDialog()
        self.ui_add_cruciform4angle = AddCruciform4AngleUi()
        self.window_add_cruciform2angle = QDialog()
        self.ui_add_cruciform2angle = AddCruciform2AngleUi()
        self.window_add_cruciform = QDialog()
        self.ui_add_cruciform = AddCruciformUi()
        self.window_add_Isection = QDialog()
        self.ui_add_Isection = AddIsectionUi()
        self.window_add_tee = QDialog()
        self.ui_add_tee = AddTeeUi()

    def clicker_add_angle(self):
        self.clicker_helper(self.window_add_angle, self.ui_add_angle)

    def clicker_add_double_angle(self):
        self.clicker_helper(self.window_add_double_angle, self.ui_add_double_angle)

    def clicker_add_channel(self):
        self.clicker_helper(self.window_add_channel, self.ui_add_channel)

    def clicker_add_double_channel(self):
        self.clicker_helper(self.window_add_double_channel, self.ui_add_double_channel)

    def clicker_add_cruciform4angle(self):
        self.clicker_helper(self.window_add_cruciform4angle, self.ui_add_cruciform4angle)

    def clicker_add_cruciform2angle(self):
        self.clicker_helper(self.window_add_cruciform2angle, self.ui_add_cruciform2angle)

    def clicker_add_cruciform(self):
        self.clicker_helper(self.window_add_cruciform, self.ui_add_cruciform)

    def clicker_add_Isection(self):
        self.clicker_helper(self.window_add_Isection, self.ui_add_Isection)

    def clicker_add_tee(self):
        self.clicker_helper(self.window_add_tee, self.ui_add_tee)

    @staticmethod
    def clicker_helper(window_add, ui_add):
        ui_add.setupUi(window_add)
        ui_add.pushButton_DefineFolder.clicked.connect(ui_add.clicker_browse)
        ui_add.pushButton_CreateSection.clicked.connect(ui_add.clicker_create_profile)
        window_add.show()