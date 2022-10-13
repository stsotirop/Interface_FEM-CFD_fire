from PyQt5.QtWidgets import QMainWindow, QLineEdit, QDialogButtonBox, QDialog, QFileDialog, QMessageBox
from PyQt5.QtCore import QDir, QFileInfo
from PyQt5 import uic
from utils import resolve_path
from computation_core.geometry_FEM_CFD import create_thermocouples, create_thermocouples_whole_frame, write_nodes_fds
from computation_core.grid_FEM_CFD import import_meshes, identify_point_in_meshes, detailed_grid
import copy
import os
import shutil
import pandas as pd


form, base = uic.loadUiType(resolve_path("CreateDevices.ui"))


class CreateDevicesUi(QMainWindow, form):

    def __init__(self):
        super(CreateDevicesUi, self).__init__()
        self.setupUi(self)
        self.fileNameFds = None
        self.nodes = {}
        self.connectivity = {}
        self.pathFolderFds = None

    # Select folder for transforming FDS input
    def clicker_create_folder_fds(self):
        dialog = self.open_folder_helper1(self.label_CreateFolderFds)
        path = None
        if dialog.exec_() and dialog.selectedFiles():
            path = QFileInfo(dialog.selectedFiles()[0]).absoluteFilePath()
            self.label_CreateFolderFds.setText(path)
        if path:
            self.pathFolderFds = path
            self.pushButton_LoadFileFds.setEnabled(True)

    # Select FDS file
    def clicker_load_file_fds(self):
        f_name, f_type = QFileDialog.getOpenFileName(self, "Open File", "",
                                                     "All Files (*);;Text Document (*.txt)"
                                                     ";;CSV File(*.csv);;Excel Binary File"
                                                     "(*.xls);;Excel File(*.xlsx)")
        if f_name:
            file_name = os.path.basename(f_name)
            os.chdir(self.pathFolderFds)
            if os.path.isfile(file_name):
                pass
            else:
                shutil.copy(f_name, self.pathFolderFds)
            temp = self.pathFolderFds + '/' + file_name
            self.label_OpenFileFds.setText(temp)
            self.fileNameFds = temp
            self.pushButton_Create1.setEnabled(True)
            self.pushButton_Create2.setEnabled(True)
            self.pushButton_Create3.setEnabled(True)
        if self.comboBox_Quantities1.count() == 0:
            self.comboBox_Quantities1.addItem("TEMPERATURE")
            self.comboBox_Quantities1.addItem("FLUX")
            self.comboBox_Quantities2.addItem("TEMPERATURE")
            self.comboBox_Quantities2.addItem("FLUX")
            self.comboBox_Quantities3.addItem("TEMPERATURE")
            self.comboBox_Quantities3.addItem("FLUX")

    # Create devices according to a critical length
    def clicker_create1(self):
        all_meshes = import_meshes(self.fileNameFds)
        critical = float(self.lineEdit_CriticalLength.text())
        temp_connect = copy.deepcopy(self.connectivity)
        new_connectivity = create_thermocouples(self.nodes, temp_connect, critical)
        quantity = self.comboBox_Quantities1.currentText()
        # Plot and write all the nodes
        all_nodes_dev = {x: self.nodes[x] for x in self.nodes.keys()}
        for line in new_connectivity.values():
            for point in line.devices:
                all_nodes_dev[point.ID] = point
        self.device_check_helper(quantity, all_nodes_dev, all_meshes)

    # Select a specific frame and create devices according to CFD mesh
    def clicker_create2(self):
        all_meshes = import_meshes(self.fileNameFds)
        my_column = self.comboBox_MembersId.currentText()
        temp_connect = copy.deepcopy(self.connectivity)
        new_connectivity = create_thermocouples_whole_frame(self.nodes, temp_connect, my_column, all_meshes)
        quantity = self.comboBox_Quantities2.currentText()
        # Plot and write all the nodes
        all_nodes_dev = {x: self.nodes[x] for x in self.nodes.keys()}
        for line in new_connectivity.values():
            for point in line.devices:
                all_nodes_dev[point.ID] = point
        self.device_check_helper(quantity, all_nodes_dev, all_meshes)

    # Select a node for detailed evaluation
    def clicker_create3(self):
        all_meshes = import_meshes(self.fileNameFds)
        my_point_id = self.comboBox_NodesId.currentText()
        my_point = self.nodes[my_point_id]
        mesh_id = identify_point_in_meshes(my_point, all_meshes)
        if mesh_id != 0:
            rest_nodes = detailed_grid(all_meshes[mesh_id - 1], my_point, all_meshes)
            quantity = self.comboBox_Quantities3.currentText()
            self.device_check_helper(quantity, rest_nodes, all_meshes)
            d = []
            for point in rest_nodes.values():
                d.append(
                    {
                        'ID': point.ID,
                        'w_xy': round(point.weight_xy, 4),
                        'w_z': round(point.weight_z, 4)
                    }
                )
            temp = pd.DataFrame(d)
            file_csv = self.pathFolderFds + '/' + my_point.ID + '.csv'
            temp.to_csv(file_csv, index=False, header=True)
            QMessageBox.about(self, "Create devices", "Successfully create .csv file for the weight coefficients")
        else:
            QMessageBox.about(self, "Create devices", "Select a point inside the CFD meshes")

    # Collect nodes - connectivity from main_gui.py
    def collect(self, nodes, connectivity):
        self.nodes = nodes
        self.connectivity = connectivity
        for key in connectivity.keys():
            self.comboBox_MembersId.addItem(key)
        for key in nodes.keys():
            self.comboBox_NodesId.addItem(key)

    # Helper
    def open_folder_helper1(self, label_create_folder):
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

    # helper for check validity of devices
    def device_check_helper(self, quantity, all_nodes_dev, all_meshes):
        points_out_meshes = []
        for k in list(all_nodes_dev.keys()):
            point = all_nodes_dev[k]
            mesh_id = identify_point_in_meshes(point, all_meshes)
            if mesh_id == 0:
                points_out_meshes.append(k)
                del all_nodes_dev[k]
        if len(points_out_meshes) != 0:
            temp_string = ' , '.join(points_out_meshes)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Create devices")
            msg.setText("Devices with ID:  " + temp_string + " are outside the meshes")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        if len(all_nodes_dev) != 0:
            write_nodes_fds(all_nodes_dev, self.fileNameFds, quantity)
            QMessageBox.about(self, "Create devices", "Successfully create devices in given .fds file")
        else:
            QMessageBox.about(self, "Create devices", "All devices are outside the meshes")
