from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QFileDialog, QMessageBox, \
    QVBoxLayout, QLineEdit, QDialogButtonBox, QDialog
from PyQt5.QtCore import QDir, QFileInfo, Qt
from PyQt5 import uic
from utils import resolve_path
from AddPropertyWindow import AddPropertyUi
from CreateDevices import CreateDevicesUi
from computation_core.files_trans import plot_temp, create_txt_temp, create_safir_input_temp, post_process_detailed_grid
from computation_core.geometry_FEM_CFD import create_node_connect, rotate_coordinate_system, \
     transport_coordinate_system
import math
import sys
import os
import shutil
import ntpath
import numpy as np
from mpl_toolkits.mplot3d.axes3d import Axes3D
import computation_core.drawing_tools_3d as drawing_tools_3d
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QT5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class MainWindowUi(QMainWindow):

    def __init__(self):
        super(MainWindowUi, self).__init__()

        # Load the ui file + basic properties
        uic.loadUi(resolve_path("main_gui.ui"), self)

        # Initialization
        self.window_add_prop = QMainWindow()
        self.ui_add_prop = AddPropertyUi()
        self.pathFolder1 = None
        self.pathFolder2 = None
        self.pathFolder3 = None
        self.pathFolder4 = None
        self.fileName1 = None
        self.fileName2 = None
        self.fileName3 = None
        self.fileName4 = None
        self.fileName5 = None
        self.fileName6 = None
        self.fileNameGeo = None
        self.nodes_init = {}
        self.nodes = {}
        self.connectivity = {}
        self.connectivity_init = {}
        self.plotWidgetGeometry = FigureCanvas()
        self.layGeometryPlot = QVBoxLayout(self.content_Plot)
        self.layGeometryPlot.setContentsMargins(0, 0, 0, 0)
        self.layGeometryTool = QVBoxLayout(self.content_Toolbar)
        self.layGeometryTool.setContentsMargins(0, 0, 0, 0)

        # Thermal
        self.buttonAddProperty = self.findChild(QPushButton, "pushButton_AddProperty")
        self.labelCreateFolder1 = self.findChild(QLabel, "label_CreateFolder1")
        self.labelOpenFile1 = self.findChild(QLabel, "label_OpenFile1")
        self.buttonCreateFolder1 = self.findChild(QPushButton, "pushButton_CreateFolder1")
        self.buttonLoadFile1 = self.findChild(QPushButton, "pushButton_LoadFile1")
        self.buttonCreateFile1 = self.findChild(QPushButton, "pushButton_CreateFile1")
        self.labelCreateFolder2 = self.findChild(QLabel, "label_CreateFolder2")
        self.labelOpenFile2 = self.findChild(QLabel, "label_OpenFile2")
        self.buttonCreateFolder2 = self.findChild(QPushButton, "pushButton_CreateFolder2")
        self.buttonLoadFile2 = self.findChild(QPushButton, "pushButton_LoadFile2")
        self.buttonCreateFile2 = self.findChild(QPushButton, "pushButton_CreateFile2")
        self.lineTotalTime = self.findChild(QLineEdit, "lineEdit_TotalTime")
        self.lineTimeStep = self.findChild(QLineEdit, "lineEdit_TimeStep")
        self.labelCreateFolder3 = self.findChild(QLabel, "label_CreateFolder3")
        self.labelOpenFile3 = self.findChild(QLabel, "label_OpenFile3")
        self.labelOpenFile4 = self.findChild(QLabel, "label_OpenFile4")
        self.buttonCreateFolder3 = self.findChild(QPushButton, "pushButton_CreateFolder3")
        self.buttonLoadFile3 = self.findChild(QPushButton, "pushButton_LoadFile3")
        self.buttonLoadFile4 = self.findChild(QPushButton, "pushButton_LoadFile4")
        self.buttonCreateFile3 = self.findChild(QPushButton, "pushButton_CreateFile3")
        self.labelCreateFolder4 = self.findChild(QLabel, "label_CreateFolder4")
        self.labelOpenFile5 = self.findChild(QLabel, "label_OpenFile5")
        self.labelOpenFile6 = self.findChild(QLabel, "label_OpenFile6")
        self.buttonCreateFolder4 = self.findChild(QPushButton, "pushButton_CreateFolder4")
        self.buttonLoadFile5 = self.findChild(QPushButton, "pushButton_LoadFile5")
        self.buttonLoadFile6 = self.findChild(QPushButton, "pushButton_LoadFile6")
        self.buttonCreateFile4 = self.findChild(QPushButton, "pushButton_CreateFile4")

        # Action
        self.buttonAddProperty.clicked.connect(self.clicker_add_property)
        self.buttonCreateFolder1.clicked.connect(self.clicker_create_folder1)
        self.buttonCreateFolder2.clicked.connect(self.clicker_create_folder2)
        self.buttonCreateFolder3.clicked.connect(self.clicker_create_folder3)
        self.buttonCreateFolder4.clicked.connect(self.clicker_create_folder4)
        self.buttonLoadFile1.clicked.connect(self.clicker_load_file1)
        self.buttonLoadFile1.setEnabled(False)
        self.buttonLoadFile2.clicked.connect(self.clicker_load_file2)
        self.buttonLoadFile2.setEnabled(False)
        self.buttonLoadFile3.clicked.connect(self.clicker_load_file3)
        self.buttonLoadFile3.setEnabled(False)
        self.buttonLoadFile4.clicked.connect(self.clicker_load_file4)
        self.buttonLoadFile4.setEnabled(False)
        self.buttonLoadFile5.clicked.connect(self.clicker_load_file5)
        self.buttonLoadFile5.setEnabled(False)
        self.buttonLoadFile6.clicked.connect(self.clicker_load_file6)
        self.buttonLoadFile6.setEnabled(False)
        self.buttonCreateFile1.clicked.connect(self.clicker_create_file1)
        self.buttonCreateFile2.clicked.connect(self.clicker_create_file2)
        self.buttonCreateFile3.clicked.connect(self.clicker_create_file3)
        self.buttonCreateFile4.clicked.connect(self.clicker_create_file4)

        # Mechanical
        self.labelOpenFileGeo = self.findChild(QLabel, "label_OpenFileGeo")
        self.buttonLoadFileGeo = self.findChild(QPushButton, "pushButton_LoadFileGeo")
        self.lineRotateX = self.findChild(QLineEdit, "lineEdit_RotateX")
        self.lineRotateY = self.findChild(QLineEdit, "lineEdit_RotateY")
        self.lineRotateZ = self.findChild(QLineEdit, "lineEdit_RotateZ")
        self.buttonRotate = self.findChild(QPushButton, "pushButton_Rotate")
        self.lineTransportX = self.findChild(QLineEdit, "lineEdit_TransportX")
        self.lineTransportY = self.findChild(QLineEdit, "lineEdit_TransportY")
        self.lineTransportZ = self.findChild(QLineEdit, "lineEdit_TransportZ")
        self.buttonTransport = self.findChild(QPushButton, "pushButton_Transport")
        self.buttonClearChanges = self.findChild(QPushButton, "pushButton_ClearChanges")

        # Action
        self.buttonLoadFileGeo.clicked.connect(self.clicker_load_file_geo)
        self.buttonRotate.clicked.connect(self.clicker_submit_rot)
        self.buttonTransport.clicked.connect(self.clicker_submit_tra)
        self.buttonClearChanges.clicked.connect(self.clicker_clear_changes)

        # Create Devices UI
        self.window_create_device = QMainWindow()
        self.ui_create_device = CreateDevicesUi()
        self.buttonCreateDevices = self.findChild(QPushButton, "pushButton_CreateDevices")
        self.buttonCreateDevices.clicked.connect(self.clicker_create_devices)
        self.buttonCreateDevices.setEnabled(False)

        self.show()

    # Open a new main window for the section properties
    def clicker_add_property(self):
        self.ui_add_prop.setupUi(self.window_add_prop)
        self.ui_add_prop.pushButton_Angle.clicked.connect(self.ui_add_prop.clicker_add_angle)
        self.ui_add_prop.pushButton_Double_Angle.clicked.connect(self.ui_add_prop.clicker_add_double_angle)
        self.ui_add_prop.pushButton_Channel.clicked.connect(self.ui_add_prop.clicker_add_channel)
        self.ui_add_prop.pushButton_Double_Channel.clicked.connect(self.ui_add_prop.clicker_add_double_channel)
        self.ui_add_prop.pushButton_Cruciform4Angle.clicked.connect(self.ui_add_prop.clicker_add_cruciform4angle)
        self.ui_add_prop.pushButton_Cruciform2Angle.clicked.connect(self.ui_add_prop.clicker_add_cruciform2angle)
        self.ui_add_prop.pushButton_Cruciform.clicked.connect(self.ui_add_prop.clicker_add_cruciform)
        self.ui_add_prop.pushButton_Isection.clicked.connect(self.ui_add_prop.clicker_add_Isection)
        self.ui_add_prop.pushButton_Tee.clicked.connect(self.ui_add_prop.clicker_add_tee)
        self.window_add_prop.show()

    # Select folder for transforming the FDS output (.csv) in .txt files ready for use in SAFIR
    def clicker_create_folder1(self):
        dialog = self.open_folder_helper(self.labelCreateFolder1)
        path = None
        if dialog.exec_() and dialog.selectedFiles():
            path = QFileInfo(dialog.selectedFiles()[0]).absoluteFilePath()
            self.labelCreateFolder1.setText(path)
        if path:
            self.pathFolder1 = path
            self.buttonLoadFile1.setEnabled(True)

    # Select folder for adjusting temperature in specific time step
    def clicker_create_folder2(self):
        dialog = self.open_folder_helper(self.labelCreateFolder2)
        path = None
        if dialog.exec_() and dialog.selectedFiles():
            path = QFileInfo(dialog.selectedFiles()[0]).absoluteFilePath()
            self.labelCreateFolder2.setText(path)
        if path:
            self.pathFolder2 = path
            self.buttonLoadFile2.setEnabled(True)

    # Select folder for creating .in files from different t-T - given in .txt
    def clicker_create_folder3(self):
        dialog = self.open_folder_helper(self.labelCreateFolder3)
        path = None
        if dialog.exec_() and dialog.selectedFiles():
            path = QFileInfo(dialog.selectedFiles()[0]).absoluteFilePath()
            self.labelCreateFolder3.setText(path)
        if path:
            self.pathFolder3 = path
            self.buttonLoadFile3.setEnabled(True)
            self.buttonLoadFile4.setEnabled(True)

    # Select folder for evaluating the temperature in structural point with weight coefficients
    def clicker_create_folder4(self):
        dialog = self.open_folder_helper(self.labelCreateFolder4)
        path = None
        if dialog.exec_() and dialog.selectedFiles():
            path = QFileInfo(dialog.selectedFiles()[0]).absoluteFilePath()
            self.labelCreateFolder4.setText(path)
        if path:
            self.pathFolder4 = path
            self.buttonLoadFile5.setEnabled(True)
            self.buttonLoadFile6.setEnabled(True)

    # Select .csv file for transforming in .txt files
    def clicker_load_file1(self):
        f_name, f_type = QFileDialog.getOpenFileName(self, "Open File", "",
                                                     "All Files (*);;Text Document (*.txt)"
                                                     ";;CSV File(*.csv);;Excel Binary File"
                                                     "(*.xls);;Excel File(*.xlsx)")
        if f_name:
            file_name = os.path.basename(f_name)
            os.chdir(self.pathFolder1)
            if os.path.isfile(file_name):
                pass
            else:
                shutil.copy(f_name, self.pathFolder1)
            self.labelOpenFile1.setText(f_name)
            self.fileName1 = file_name

    # Select .txt file for adjusting temperature in specific time step
    def clicker_load_file2(self):
        f_name, f_type = QFileDialog.getOpenFileNames(self, "Open File", "",
                                                      "All Files (*);;Text Document (*.txt)"
                                                      ";;CSV File(*.csv);;Excel Binary File"
                                                      "(*.xls);;Excel File(*.xlsx)")
        self.fileName2 = f_name

        if f_name:
            self.labelOpenFile2.setText(f_name[0])

    # Select prototype .in file for producing same in. files with different .txt curves
    def clicker_load_file3(self):
        f_name, f_type = QFileDialog.getOpenFileName(self, "Open File", "",
                                                     "All Files (*);;Text Document (*.txt)"
                                                     ";;CSV File(*.csv);;Excel Binary File"
                                                     "(*.xls);;Excel File(*.xlsx)")
        if f_name:
            file_name = os.path.basename(f_name)
            os.chdir(self.pathFolder3)
            if os.path.isfile(file_name):
                pass
            else:
                shutil.copy(f_name, self.pathFolder3)
            self.labelOpenFile3.setText(f_name)
            self.fileName3 = file_name

    # Select .txt files for replacing time-temperature curve in existing .in file.
    # Always select first the .txt in the prototype .in
    def clicker_load_file4(self):
        f_name, f_type = QFileDialog.getOpenFileNames(self, "Open File", "",
                                                      "All Files (*);;Text Document (*.txt)"
                                                      ";;CSV File(*.csv);;Excel Binary File"
                                                      "(*.xls);;Excel File(*.xlsx)")
        self.fileName4 = f_name

        if f_name:
            self.labelOpenFile4.setText(f_name[0])

    # Select .csv file that contains weight coefficient of detailed structural point
    def clicker_load_file5(self):
        f_name, f_type = QFileDialog.getOpenFileName(self, "Open File", "",
                                                     "All Files (*);;Text Document (*.txt)"
                                                     ";;CSV File(*.csv);;Excel Binary File"
                                                     "(*.xls);;Excel File(*.xlsx)")
        if f_name:
            file_name = os.path.basename(f_name)
            os.chdir(self.pathFolder4)
            if os.path.isfile(file_name):
                pass
            else:
                shutil.copy(f_name, self.pathFolder4)
            self.labelOpenFile5.setText(f_name)
            self.fileName5 = file_name

    # Select .txt files with time-temperature curves from selected points in the grid for detailed evaluation
    def clicker_load_file6(self):
        f_name, f_type = QFileDialog.getOpenFileNames(self, "Open File", "",
                                                      "All Files (*);;Text Document (*.txt)"
                                                      ";;CSV File(*.csv);;Excel Binary File"
                                                      "(*.xls);;Excel File(*.xlsx)")
        self.fileName6 = f_name

        if f_name:
            self.labelOpenFile6.setText(f_name[0])

    # Transform .csv file in .txt files
    def clicker_create_file1(self):
        if self.fileName1:
            create_txt_temp(self.pathFolder1, self.fileName1)
            QMessageBox.about(self, "Temperature files", "Successfully transformed to .txt!")

    # Adjust temperature in specific time step
    def clicker_create_file2(self):
        if self.fileName2:
            for file in self.fileName2:
                total_time = int(self.lineTotalTime.text())
                time_step = int(self.lineTimeStep.text())
                plot_temp(file, self.pathFolder2, total_time, time_step)
            QMessageBox.about(self, "Temperature files", "Successfully interpolated in selected time and time step!")

    # Create safir input file for multiple cross-sections
    def clicker_create_file3(self):
        if self.fileName3 and self.fileName4:
            root_temp = ntpath.basename(self.fileName4[0])
            root_txt_0, extension_txt = os.path.splitext(root_temp)
            for file in self.fileName4:
                create_safir_input_temp(self.fileName3, file, root_txt_0, self.pathFolder3)
            QMessageBox.about(self, "Safir files", "Successfully generate safir inputs based on selected .in file!")

    # Evaluation of the temperature of a structural point with weight coefficient
    def clicker_create_file4(self):
        if self.fileName5 and self.fileName6:
            root_temp = ntpath.basename(self.fileName5)
            txt_name, extension_txt = os.path.splitext(root_temp)
            check_files = post_process_detailed_grid(self.fileName5, self.fileName6, self.pathFolder4, txt_name)
            if check_files == 0:
                QMessageBox.about(self, "Temperature files", "Successfully generate temperature file in exact point!")
            elif check_files == -1:
                QMessageBox.about(self, "Temperature files", "The nodes' ID of .csv doesn't coincide with the .txt "
                                                             "files")

    # Helper
    def open_folder_helper(self, label_create_folder):
        dialog = QFileDialog(self)
        if label_create_folder.text():
            dialog.setDirectory(label_create_folder.text())
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
        button = dialog.findChild(QDialogButtonBox).button(
            QDialogButtonBox.Open)

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

        return dialog

    # Load geometry from .geo file
    def clicker_load_file_geo(self):
        f_name, f_type = QFileDialog.getOpenFileName(self, "Open File", "",
                                                     "All Files (*);;Text Document (*.txt)"
                                                     ";;CSV File(*.csv);;Excel Binary File"
                                                     "(*.xls);;Excel File(*.xlsx)")
        if f_name:
            self.labelOpenFileGeo.setText(f_name)
            self.fileNameGeo = f_name
            nodes, connectivity = create_node_connect(f_name)
            self.nodes_init = nodes
            self.nodes = nodes
            self.connectivity = connectivity
            self.connectivity_init = connectivity
            self.plot_geometry_gui(nodes, connectivity)
            self.buttonCreateDevices.setEnabled(True)

    # Rotate structure around a specific axis and angle
    def clicker_submit_rot(self):
        if self.lineRotateY.text() == '0' and self.lineRotateZ.text() == '0':
            rotation_axis = 'x'
            rot_x = int(self.lineRotateX.text())
            rotation = math.radians(rot_x)
            self.nodes = rotate_coordinate_system(self.nodes, rotation_axis, rotation)
            self.plot_geometry_gui(self.nodes, self.connectivity)
            QMessageBox.about(self, "Rotate structure", "Successfully rotated around x axis!")
        elif self.lineRotateX.text() == '0' and self.lineRotateZ.text() == '0':
            rotation_axis = 'y'
            rot_y = int(self.lineRotateY.text())
            rotation = math.radians(rot_y)
            self.nodes = rotate_coordinate_system(self.nodes, rotation_axis, rotation)
            self.plot_geometry_gui(self.nodes, self.connectivity)
            QMessageBox.about(self, "Rotate structure", "Successfully rotated around y axis!")
        elif self.lineRotateX.text() == '0' and self.lineRotateY.text() == '0':
            rotation_axis = 'z'
            rot_z = int(self.lineRotateZ.text())
            rotation = math.radians(rot_z)
            self.nodes = rotate_coordinate_system(self.nodes, rotation_axis, rotation)
            self.plot_geometry_gui(self.nodes, self.connectivity)
            QMessageBox.about(self, "Rotate structure", "Successfully rotated around z axis!")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Rotate Error")
            msg.setText(f'Please define one axis of rotation')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    # Transport the structure according to a given vector
    def clicker_submit_tra(self):
        tra_x = round(float(self.lineTransportX.text()), 2)
        tra_y = round(float(self.lineTransportY.text()), 2)
        tra_z = round(float(self.lineTransportZ.text()), 2)
        transport_vec = (tra_x, tra_y, tra_z)
        self.nodes = transport_coordinate_system(self.nodes, transport_vec)
        self.plot_geometry_gui(self.nodes, self.connectivity)
        QMessageBox.about(self, "Transport structure", "Successfully structure transportation!")

    # Clear rotation and transportation
    def clicker_clear_changes(self):
        temp1 = {x: self.nodes_init[x] for x in self.nodes_init.keys()}
        self.nodes = temp1
        temp2 = {x: self.connectivity_init[x] for x in self.connectivity_init.keys()}
        self.connectivity = temp2
        self.plot_geometry_gui(self.nodes, self.connectivity)

    # Plot the structure in my GUI
    def plot_geometry_gui(self, nodes, connectivity, plot_devices=False):
        self.remove_widget(self.layGeometryTool)
        self.layGeometryPlot.removeWidget(self.plotWidgetGeometry)
        setattr(Axes3D, 'annotate3D', drawing_tools_3d.annotate3d)
        _fig = plt.figure()
        ax = plt.axes(projection="3d")
        for line in connectivity.values():
            p1 = nodes[line.point_start.ID]
            p2 = nodes[line.point_end.ID]
            xx = [p1.x, p2.x]; yy = [p1.y, p2.y]; zz = [p1.z, p2.z]
            ax.plot3D(xx, yy, zz, 'black')
            ax.scatter(xx, yy, zz, color="black", marker='o')
            ax.annotate3D(f'P' + p1.ID, (xx[0], yy[0], zz[0]), xytext=(3, 3), textcoords='offset points')
            ax.annotate3D(f'P' + p2.ID, (xx[1], yy[1], zz[1]), xytext=(3, 3), textcoords='offset points')
            if plot_devices:
                if len(line.devices) > 0:
                    for point in line.devices:
                        ax.scatter(point.x, point.y, point.z, color="black", marker='o')
                        ax.annotate3D(f'P' + point.ID, (point.x, point.y, point.z), xytext=(3, 3),
                                      textcoords='offset points')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        x = ax.get_xlim3d()
        y = ax.get_ylim3d()
        z = ax.get_zlim3d()
        a = [x[1] - x[0], y[1] - y[0], z[1] - z[0]]
        b = np.amax(a)
        ax.set_xlim3d(x[0] - (b - a[0]) / 2, x[1] + (b - a[0]) / 2)
        ax.set_ylim3d(y[0] - (b - a[1]) / 2, y[1] + (b - a[1]) / 2)
        ax.set_zlim3d(z[0] - (b - a[2]) / 2, z[1] + (b - a[2]) / 2)
        # Add layouts + widgets
        self.plotWidgetGeometry = FigureCanvas(_fig)
        self.layGeometryPlot.addWidget(self.plotWidgetGeometry)
        _toolWidget = NavigationToolbar(self.plotWidgetGeometry, self)
        self.layGeometryTool.addWidget(_toolWidget)
        plt.close(_fig)

    # Open new main window for creating the devices
    def clicker_create_devices(self):
        self.ui_create_device.setupUi(self.window_create_device)
        self.ui_create_device.pushButton_CreateFolderFds.clicked.connect(self.ui_create_device.clicker_create_folder_fds)
        self.ui_create_device.pushButton_LoadFileFds.clicked.connect(self.ui_create_device.clicker_load_file_fds)
        self.ui_create_device.pushButton_LoadFileFds.setEnabled(False)
        self.ui_create_device.collect(self.nodes, self.connectivity)
        self.ui_create_device.pushButton_Create1.clicked.connect(self.ui_create_device.clicker_create1)
        self.ui_create_device.pushButton_Create1.setEnabled(False)
        self.ui_create_device.pushButton_Create2.clicked.connect(self.ui_create_device.clicker_create2)
        self.ui_create_device.pushButton_Create2.setEnabled(False)
        self.ui_create_device.pushButton_Create3.clicked.connect(self.ui_create_device.clicker_create3)
        self.ui_create_device.pushButton_Create3.setEnabled(False)

        self.window_create_device.show()

    @staticmethod
    def remove_widget(lay_tool):
        for i in reversed(range(lay_tool.count())):
            widget_to_remove = lay_tool.itemAt(i).widget()
            # remove it from the layout list
            lay_tool.removeWidget(widget_to_remove)
            # remove it from the gui
            widget_to_remove.setParent(None)


# Run program
def run():
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    UIWindow = MainWindowUi()
    app.exec_()
