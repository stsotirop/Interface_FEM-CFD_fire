import math
from numpy import ogrid
import re
from computation_core.geometrical_tools import Point, Mesh


def detailed_grid(mesh1, my_struct_point, all_meshes):
    x_step = mesh1.point_step.x
    y_step = mesh1.point_step.y
    z_step = mesh1.point_step.z
    x_start = mesh1.point_min.x + round(x_step / 2, 2)
    x_stop = mesh1.point_max.x + round(x_step / 2, 2)
    y_start = mesh1.point_min.y + round(y_step / 2, 2)
    y_stop = mesh1.point_max.y + round(y_step / 2, 2)
    z_start = mesh1.point_min.z + round(z_step / 2, 2)
    z_stop = mesh1.point_max.z + round(z_step / 2, 2)
    grid_x = ogrid[x_start:x_stop:x_step]
    grid_y = ogrid[y_start:y_stop:y_step]
    grid_z = ogrid[z_start:z_stop:z_step]
    closest_x = closest(grid_x, my_struct_point.x)
    closest_y = closest(grid_y, my_struct_point.y)
    closest_z = closest(grid_z, my_struct_point.z)
    my_grid_point = Point(closest_x, closest_y, closest_z)
    rest_nodes = evaluation_xy_plane(x_step, y_step, my_grid_point, my_struct_point, my_grid_point.z, all_meshes)
    # In the z direction my structural point is in the center of the cell
    if my_struct_point.z == my_grid_point.z:
        for node in rest_nodes.values():
            node.weight_z = 1
    else:
        # In the z direction my structural point is up of the center of the cell
        w1 = 1
        w2 = -1
        if my_struct_point.z > my_grid_point.z:
            rest_nodes_temp = evaluation_xy_plane(x_step, y_step, my_grid_point, my_struct_point,
                                                  my_grid_point.z + z_step, all_meshes)
            point2 = Point(round(my_struct_point.x, 2), round(my_struct_point.y, 2), round(my_grid_point.z + z_step, 2))
            mesh_id = identify_point_in_meshes(point2, all_meshes)
            if mesh_id == 0:
                pass
            else:
                d1 = abs(my_struct_point.z - my_grid_point.z)
                d2 = abs(point2.z - my_struct_point.z)
                w1, w2 = weights_evaluation([d1, d2])
        # In the z direction my structural point is down of the center of the cell
        elif my_struct_point.z < my_grid_point.z:
            rest_nodes_temp = evaluation_xy_plane(x_step, y_step, my_grid_point, my_struct_point,
                                                  my_grid_point.z - z_step, all_meshes)
            point2 = Point(round(my_struct_point.x, 2), round(my_struct_point.y, 2), round(my_grid_point.z - z_step, 2))
            mesh_id = identify_point_in_meshes(point2, all_meshes)
            if mesh_id == 0:
                pass
            else:
                d1 = abs(my_struct_point.z - my_grid_point.z)
                d2 = abs(point2.z - my_struct_point.z)
                w1, w2 = weights_evaluation([d1, d2])
        for node in rest_nodes.values():
            node.weight_z = w1
        if w2 != -1:
            for node in rest_nodes_temp.values():
                node.weight_z = w2
            rest_nodes.update(rest_nodes_temp)

    return rest_nodes


def evaluation_xy_plane(x_step, y_step, grid_point, struct_point, z, all_meshes):
    temp_grid_point = Point(grid_point.x, grid_point.y, grid_point.z, struct_point.ID)
    temp_grid_point.ID = struct_point.ID + f'_gp_{round(z, 2)}'
    if struct_point.x == grid_point.x and struct_point.y == grid_point.y:
        temp_grid_point.z = round(z, 2)
        rest_nodes = {temp_grid_point.ID: temp_grid_point}
    else:
        points = []
        # In the xy plane my structural point is up right regarding the center of the cell
        if struct_point.x >= grid_point.x and struct_point.y >= grid_point.y:
            points.append(Point(round(grid_point.x + x_step, 2), round(grid_point.y, 2), round(z, 2),
                          f'{struct_point.ID}_p2_{round(z, 2)}'))
            points.append(Point(round(grid_point.x + x_step, 2), round(grid_point.y + y_step, 2), round(z, 2),
                          f'{struct_point.ID}_p3_{round(z, 2)}'))
            points.append(Point(round(grid_point.x, 2), round(grid_point.y + y_step, 2), round(z, 2),
                          f'{struct_point.ID}_p4_{round(z, 2)}'))
        # In the xy plane my structural point is up left regarding the center of the cell
        elif struct_point.x < grid_point.x and struct_point.y >= grid_point.y:
            points.append(Point(round(grid_point.x, 2), round(grid_point.y + y_step, 2), round(z, 2),
                          f'{struct_point.ID}_p2_{round(z, 2)}'))
            points.append(Point(round(grid_point.x - x_step, 2), round(grid_point.y + y_step, 2), round(z, 2),
                          f'{struct_point.ID}_p3_{round(z, 2)}'))
            points.append(Point(round(grid_point.x - x_step, 2), round(grid_point.y, 2), round(z, 2),
                          f'{struct_point.ID}_p4_{round(z, 2)}'))
        # In the xy plane my structural point is down left regarding the center of the cell
        elif struct_point.x < grid_point.x and struct_point.y < grid_point.y:
            points.append(Point(round(grid_point.x - x_step, 2), round(grid_point.y, 2), round(z, 2),
                          f'{struct_point.ID}_p2_{round(z, 2)}'))
            points.append(Point(round(grid_point.x - x_step, 2), round(grid_point.y - y_step, 2), round(z, 2),
                          f'{struct_point.ID}_p3_{round(z, 2)}'))
            points.append(Point(round(grid_point.x, 2), round(grid_point.y - y_step, 2), round(z, 2),
                          f'{struct_point.ID}_p4_{round(z, 2)}'))
        # In the xy plane my structural point is down right regarding the center of the cell
        elif struct_point.x >= grid_point.x and struct_point.y < grid_point.y:
            points.append(Point(round(grid_point.x, 2), round(grid_point.y - y_step, 2), round(z, 2),
                          f'{struct_point.ID}_p2_{round(z, 2)}'))
            points.append(Point(round(grid_point.x + x_step, 2), round(grid_point.y - y_step, 2), round(z, 2),
                          f'{struct_point.ID}_p3_{round(z, 2)}'))
            points.append(Point(round(grid_point.x + x_step, 2), round(grid_point.y, 2), round(z, 2),
                          f'{struct_point.ID}_p4_{round(z, 2)}'))
        # Evaluate weights and rest
        for point in list(points):
            mesh_id = identify_point_in_meshes(point, all_meshes)
            if mesh_id == 0:
                points.remove(point)
        dist = [distance(struct_point, grid_point)]
        for point in points:
            dist.append(distance(struct_point, point))
        weights = weights_evaluation(dist)

        if grid_point.z == z:
            pass
        else:
            temp_grid_point.z = round(z, 2)
        temp_grid_point.ID = struct_point.ID + f'_gp_{round(z, 2)}'
        temp_grid_point.weight_xy = weights[0]
        rest_nodes = {temp_grid_point.ID: temp_grid_point}
        sum1 = 1
        for point in points:
            point.weight_xy = weights[sum1]
            rest_nodes[point.ID] = point
            sum1 += 1

    return rest_nodes


def weights_evaluation(distances):
    d_total = 0
    w = []
    for dist in distances:
        d_total += 1 / dist
    for dist in distances:
        temp = round((1 / dist) / d_total, 4)
        w.append(temp)

    return w


def distance(point1, point2):
    return math.sqrt(pow(point1.x - point2.x, 2) + pow(point1.y - point2.y, 2))


def import_meshes(file):
    all_meshes = []
    with open(file, 'r') as read_obj:
        for line in read_obj:
            if line.startswith("&MESH"):
                # Retrieve IJK from fds file
                index1 = line.find('IJK=')
                index2 = line.find('XB=')
                new_string = line[index1:index2]
                result = [_.start() for _ in re.finditer(',', new_string)]
                num_i = result[0] - 4
                temp_list = []
                temp_string = ''
                for i in range(num_i):
                    temp_list.append(new_string[4 + i])
                i_string = temp_string.join(temp_list)
                j_string = retrieve_mesh_data(result[1], result[0], new_string)
                k_string = retrieve_mesh_data(result[2], result[1], new_string)
                ijk = [int(i_string), int(j_string), int(k_string)]
                # Retrieve XB from fds file
                index3 = len(line)
                new_string = line[index2:index3]
                result = [_.start() for _ in re.finditer(',', new_string)]
                num_i = result[0] - 3
                temp_list = []
                temp_string = ''
                for i in range(num_i):
                    temp_list.append(new_string[3 + i])
                x_min = temp_string.join(temp_list)
                x_max = retrieve_mesh_data(result[1], result[0], new_string)
                y_min = retrieve_mesh_data(result[2], result[1], new_string)
                y_max = retrieve_mesh_data(result[3], result[2], new_string)
                z_min = retrieve_mesh_data(result[4], result[3], new_string)
                index4 = len(new_string)
                z_max = retrieve_mesh_data(index4 - 2, result[4], new_string)
                xb = [float(x_min), float(x_max), float(y_min), float(y_max), float(z_min), float(z_max)]
                point_min = Point(xb[0], xb[2], xb[4])
                point_max = Point(xb[1], xb[3], xb[5])
                x_step = round((point_max.x - point_min.x) / ijk[0], 4)
                y_step = round((point_max.y - point_min.y) / ijk[1], 4)
                z_step = round((point_max.z - point_min.z) / ijk[2], 4)
                point_step = Point(x_step, y_step, z_step)
                index5 = line.find('ID=')
                mesh1 = Mesh(int(line[index5 + 4]), point_min, point_max, point_step)
                all_meshes.append(mesh1)

    return all_meshes


def retrieve_mesh_data(char_f, char_i, new_string):
    num_i = char_f - char_i
    temp_list = []
    temp_string = ''
    for i in range(num_i - 1):
        temp_list.append(new_string[char_i + 1 + i])
    asd = temp_string.join(temp_list)

    return asd


def identify_point_in_meshes(my_point, all_meshes):
    mesh_id = 0
    for mesh in all_meshes:
        if mesh.point_min.x <= my_point.x <= mesh.point_max.x:
            if mesh.point_min.y <= my_point.y <= mesh.point_max.y:
                if mesh.point_min.z <= my_point.z <= mesh.point_max.z:
                    mesh_id = mesh.ID
                    break

    return mesh_id


def closest(lst, k):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - k))]
