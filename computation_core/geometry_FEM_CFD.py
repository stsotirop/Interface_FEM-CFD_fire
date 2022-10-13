import math
import re
from computation_core.geometrical_tools import Point, Line
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import computation_core.drawing_tools_3d as drawing_tools_3d
from computation_core.grid_FEM_CFD import identify_point_in_meshes


# Read geo file and create nodes - connectivity info
def create_node_connect(file):
    nodes = {}
    connectivity = {}
    with open(file, 'r', encoding='UTF8', newline='') as read_obj:
        for line in read_obj:
            if line.startswith("Point("):
                # Retrieve number of point from geo file
                index1 = 6
                index2 = len(line)
                for i in range(index1, index2):
                    if line[i] == ')':
                        break
                num_i = i - index1
                temp_list = []
                temp_string = ''
                for i in range(num_i):
                    temp_list.append(line[index1 + i])
                id_string = temp_string.join(temp_list)
                index3 = line.find('{')
                result = [_.start() for _ in re.finditer(',', line)]
                x_string = retrieve_fem_data(result[0], index3, line)
                y_string = retrieve_fem_data(result[1], result[0], line)
                y_string = ''.join(y_string.split())
                z_string = retrieve_fem_data(result[2], result[1], line)
                z_string = ''.join(z_string.split())
                point = Point(float(x_string), float(y_string), float(z_string), str(id_string))
                nodes[str(id_string)] = point
            if line.startswith("Line("):
                # Retrieve number of point from geo file
                index1 = 5
                index2 = len(line)
                for i in range(index1, index2):
                    if line[i] == ')':
                        break
                num_i = i - index1
                temp_list = []
                temp_string = ''
                for i in range(num_i):
                    temp_list.append(line[index1 + i])
                id_string = temp_string.join(temp_list)
                index3 = line.find('{')
                result = [_.start() for _ in re.finditer(',', line)]
                point_start_id = retrieve_fem_data(result[0], index3, line)
                point_end_id = retrieve_fem_data(index2 - 4, result[0], line)
                point_start = nodes[str(point_start_id.strip())]
                point_end = nodes[str(point_end_id.strip())]
                line_member = Line(str(id_string), point_start, point_end)
                connectivity[str(id_string)] = line_member
    return nodes, connectivity


# Helper for retrieve data from file
def retrieve_fem_data(char_f, char_i, new_string):
    num_i = char_f - char_i - 1
    temp_list = []
    temp_string = ''
    for i in range(num_i):
        temp_list.append(new_string[char_i + 1 + i])
    asd = temp_string.join(temp_list)

    return asd


# Rotate the structure along an axis - rotation_axis and a specific angle
def rotate_coordinate_system(nodes, rotation_axis, rotation):
    nodes_mat = np.zeros((1, 3))
    new_nodes = {}
    if rotation_axis == 'x':
        rx = np.array([[1, 0, 0], [0, round(math.cos(rotation), 4), - round(math.sin(rotation), 4)],
                   [0, round(math.sin(rotation), 4), round(math.cos(rotation), 4)]])
        for node in nodes.values():
            nodes_mat[0][0] = node.x
            nodes_mat[0][1] = node.y
            nodes_mat[0][2] = node.z
            new_node_mat = np.dot(nodes_mat, rx)
            new_node = Point(new_node_mat[0][0], new_node_mat[0][1], new_node_mat[0][2], node.ID)
            new_nodes[node.ID] = new_node
    elif rotation_axis == 'y':
        ry = np.array([[round(math.cos(rotation), 4), 0, round(math.sin(rotation), 4)], [0, 1, 0],
                   [- round(math.sin(rotation), 4), 0, round(math.cos(rotation), 4)]])
        for node in nodes.values():
            nodes_mat[0][0] = node.x
            nodes_mat[0][1] = node.y
            nodes_mat[0][2] = node.z
            new_node_mat = np.dot(nodes_mat, ry)
            new_node = Point(new_node_mat[0][0], new_node_mat[0][1], new_node_mat[0][2], node.ID)
            new_nodes[node.ID] = new_node
    elif rotation_axis == 'z':
        rz = np.array([[round(math.cos(rotation), 4), - round(math.sin(rotation), 4), 0],
                   [round(math.sin(rotation), 4), round(math.cos(rotation), 4), 0], [0, 0, 1]])
        for node in nodes.values():
            nodes_mat[0][0] = node.x
            nodes_mat[0][1] = node.y
            nodes_mat[0][2] = node.z
            new_node_mat = np.dot(nodes_mat, rz)
            new_node = Point(new_node_mat[0][0], new_node_mat[0][1], new_node_mat[0][2], node.ID)
            new_nodes[node.ID] = new_node

    return new_nodes


# Transport the structure given a 3D vector
def transport_coordinate_system(nodes, transport_vec):
    new_nodes = {}
    for node in nodes.values():
        new_node = Point(node.x + transport_vec[0], node.y + transport_vec[1], node.z + transport_vec[2], node.ID)
        new_nodes[node.ID] = new_node

    return new_nodes


# Plot frame structure
def plot_geometry(nodes, connectivity, plot_devices=False):
    setattr(Axes3D, 'annotate3D', drawing_tools_3d.annotate3d)
    _fig = plt.figure()
    ax = plt.axes(projection="3d")
    for line in connectivity.values():
        p1 = nodes[line.point_start.ID]
        p2 = nodes[line.point_end.ID]
        print(p1.ID, p1.x, p1.y, p1.z)
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
    plt.show()


# Write the nodes in .fds file as devices
def write_nodes_fds(nodes, file, quantity):
    add_lines = []
    for node in nodes.values():
        temp_x = round(node.x, 2); temp_y = round(node.y, 2); temp_z = round(node.z, 2)
        line = r"&DEVC ID='" + f'{node.ID}' + "', QUANTITY='" + quantity + f"', XYZ={temp_x},{temp_y},{temp_z}/" + '\n'
        add_lines.append(line)
    index = 0
    counter = 0
    with open(file, 'r', encoding='UTF8', newline='') as read_obj:
        for line in read_obj:
            if line.startswith("&DEVC"):
                index = counter
                break
            counter += 1
    with open(file, 'r+') as fd:
        contents = fd.readlines()
        first_file = contents[0:index]
        second_file = contents[index:]
        new_contents = first_file + add_lines + second_file
        fd.seek(0)
        fd.writelines(new_contents)


# Create devices with a specific critical length
def create_thermocouples(nodes, connectivity, critical):
    for line in connectivity.values():
        p1 = nodes[line.point_start.ID]
        p2 = nodes[line.point_end.ID]
        x = p1.x + 0.5 * (p2.x - p1.x)
        y = p1.y + 0.5 * (p2.y - p1.y)
        z = p1.z + 0.5 * (p2.z - p1.z)
        p_mid = Point(round(x, 2), round(y, 2), round(z, 2), f'Line_{line.ID}' + r' mid')
        line.length()
        mid_line = Line(line.ID + r'_mid', p1, p_mid)
        mid_line.length()
        int_x = mid_line.line_length // critical
        nodes1 = [p_mid]
        if int_x > 0:
            for i in range(int(int_x) - 1):
                x = p1.x + ((i + 1) / int_x) * (p_mid.x - p1.x)
                y = p1.y + ((i + 1) / int_x) * (p_mid.y - p1.y)
                z = p1.z + ((i + 1) / int_x) * (p_mid.z - p1.z)
                temp = f'Line_{line.ID}' + ' extra_1' + f'{i}'
                p3 = Point(round(x, 2), round(y, 2), round(z, 2), temp)
                nodes1.append(p3)
                x = p_mid.x + ((i + 1) / int_x) * (p2.x - p_mid.x)
                y = p_mid.y + ((i + 1) / int_x) * (p2.y - p_mid.y)
                z = p_mid.z + ((i + 1) / int_x) * (p2.z - p_mid.z)
                temp = f'Line_{line.ID}' + ' extra_2' + f'{i}'
                p4 = Point(round(x, 2), round(y, 2), round(z, 2), temp)
                nodes1.append(p4)
        line.devices = nodes1

    return connectivity


# Create devices in a frame in distances equal with the size of the CFD cells
def create_thermocouples_whole_frame(nodes_tran, connectivity, my_column_id, all_meshes):
    my_column = connectivity[my_column_id]
    point_st = nodes_tran[my_column.point_start.ID]
    point_end = nodes_tran[my_column.point_end.ID]
    mesh_id_st = identify_point_in_meshes(point_st, all_meshes)
    mesh_id_end = identify_point_in_meshes(point_end, all_meshes)
    mesh_id = 0
    if mesh_id_st != 0:
        mesh_id = mesh_id_st
    elif mesh_id_st == 0 and mesh_id_end != 0:
        mesh_id = mesh_id_end
    vec = [(point_end.x - point_st.x), (point_end.y - point_st.y), (point_end.z - point_st.z)]
    nonzero_ind = np.nonzero(vec)[0]
    critical_length = 0
    if mesh_id_st != 0:
        if len(nonzero_ind) == 1:
            if nonzero_ind[0] == 0:     # direction - x
                critical_length = all_meshes[mesh_id - 1].point_step.x
            elif nonzero_ind[0] == 1:     # direction - y
                critical_length = all_meshes[mesh_id - 1].point_step.y
            elif nonzero_ind[0] == 2:     # direction - z
                critical_length = all_meshes[mesh_id - 1].point_step.z
        elif len(nonzero_ind) == 2:
            if nonzero_ind[0] == 0 and nonzero_ind[1] == 1:     # direction - xy
                critical_length = min(all_meshes[mesh_id - 1].point_step.x, all_meshes[mesh_id - 1].point_step.y)
            elif nonzero_ind[0] == 0 and nonzero_ind[1] == 2:     # direction - xz
                critical_length = min(all_meshes[mesh_id - 1].point_step.x, all_meshes[mesh_id - 1].point_step.z)
            elif nonzero_ind[0] == 1 and nonzero_ind[1] == 2:     # direction - yz
                critical_length = min(all_meshes[mesh_id - 1].point_step.y, all_meshes[mesh_id - 1].point_step.z)
        elif len(nonzero_ind) == 3:     # direction - xyz
            critical_length = min(all_meshes[mesh_id - 1].point_step.x, all_meshes[mesh_id - 1].point_step.y,
                                  all_meshes[mesh_id - 1].point_step.z)
        x = point_st.x + 0.5 * (point_end.x - point_st.x)
        y = point_st.y + 0.5 * (point_end.y - point_st.y)
        z = point_st.z + 0.5 * (point_end.z - point_st.z)
        p_mid = Point(round(x, 2), round(y, 2), round(z, 2), f'Line_{my_column.ID}' + r' mid')
        my_column.length()
        mid_line = Line(my_column.ID + r'_mid', point_st, p_mid)
        mid_line.length()
        int_x = mid_line.line_length // critical_length
        nodes1 = [p_mid]
        if int_x > 0:
            for i in range(int(int_x) - 1):
                x = point_st.x + ((i + 1) / int_x) * (p_mid.x - point_st.x)
                y = point_st.y + ((i + 1) / int_x) * (p_mid.y - point_st.y)
                z = point_st.z + ((i + 1) / int_x) * (p_mid.z - point_st.z)
                temp = f'Line_{my_column.ID}' + ' extra_1' + f'{i}'
                p3 = Point(round(x, 2), round(y, 2), round(z, 2), temp)
                nodes1.append(p3)
                x = p_mid.x + ((i + 1) / int_x) * (point_end.x - p_mid.x)
                y = p_mid.y + ((i + 1) / int_x) * (point_end.y - p_mid.y)
                z = p_mid.z + ((i + 1) / int_x) * (point_end.z - p_mid.z)
                temp = f'Line_{my_column.ID}' + ' extra_2' + f'{i}'
                p4 = Point(round(x, 2), round(y, 2), round(z, 2), temp)
                nodes1.append(p4)
        my_column.devices = nodes1

    return connectivity
