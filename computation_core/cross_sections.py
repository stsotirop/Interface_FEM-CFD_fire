from computation_core.geometrical_tools import Point
import os
import glob


# !!!!!!!!!!!!!!! The nodes must be always counterclockwise to define the curve !!!!!!!!!!!!!!!!!!!!!!
# Create channel section property
def create_upn(h, b, tw, tfl, profile_path, profile_name):
    os.chdir(profile_path)
    temp_files = glob.glob('*.geo')
    _temp = profile_name + '.geo'
    exist_flag = False
    dim_dict = {'H': h, 'B': b, 'tw': tw, 'tfl': tfl}
    if _temp in temp_files:
        exist_flag = True
        pass
    else:
        a_fl = b * tfl
        a_w = (h - (2 * tfl)) * tw
        grav1 = Point(b / 2, tfl / 2, 0)
        grav2 = Point(tw / 2, h / 2, 0)
        grav3 = Point(b / 2, h - (tfl / 2), 0)
        x_gr = (grav1.x * a_fl + grav2.x * a_w + grav3.x * a_fl) / (2 * a_fl + a_w)
        # y_gr = (grav1.y * a_fl + grav2.y * a_w + grav3.y * a_fl) / (2 * a_fl + a_w)
        point1 = (- x_gr + tw, (h / 2) - tfl)
        point2 = (b - x_gr, (h / 2) - tfl)
        point3 = (b - x_gr, h / 2)
        point4 = (- x_gr, h / 2)
        point5 = (- x_gr, - (h / 2))
        point6 = (b - x_gr, - (h / 2))
        point7 = (b - x_gr, - (h / 2) + tfl)
        point8 = (- x_gr + tw, - (h / 2) + tfl)
        points = [point1, point2, point3, point4, point5, point6, point7, point8]
        write_to_txt_1surface(points, profile_path, profile_name, dim_dict)

    return exist_flag


# Create double channel section property
def create_2upn(h, b, tw, tfl, dist, profile_path, profile_name):
    os.chdir(profile_path)
    temp_files = glob.glob('*.geo')
    _temp = profile_name + '.geo'
    exist_flag = False
    dim_dict = {'H': h, 'B': b, 'tw': tw, 'tfl': tfl, 'dist': dist}
    if _temp in temp_files:
        exist_flag = True
        pass
    else:
        d = dist / 2
        point1 = (d + tw, (h / 2) - tfl)
        point2 = (d + b, (h / 2) - tfl)
        point3 = (d + b, h / 2)
        point4 = (d, h / 2)
        point5 = (d, - (h / 2))
        point6 = (d + b, - (h / 2))
        point7 = (d + b, - (h / 2) + tfl)
        point8 = (d + tw, - (h / 2) + tfl)
        points = [point1, point2, point3, point4, point5, point6, point7, point8]
        write_to_txt_1surface(points, profile_path, profile_name, dim_dict)
        point1 = (- d - tw, (h / 2) - tfl)
        point2 = (- d - tw, - (h / 2) + tfl)
        point3 = (- d - b, - (h / 2) + tfl)
        point4 = (- d - b, - (h / 2))
        point5 = (- d, - (h / 2))
        point6 = (- d, h / 2)
        point7 = (- d - b, h / 2)
        point8 = (- d - b, (h / 2) - tfl)
        points = [point1, point2, point3, point4, point5, point6, point7, point8]
        write_to_txt_num_surface(points, profile_path, profile_name, '2')

    return exist_flag


# Create angle section property
def create_l(h, b, tw, tfl, profile_path, profile_name):
    os.chdir(profile_path)
    temp_files = glob.glob('*.geo')
    _temp = profile_name + '.geo'
    exist_flag = False
    dim_dict = {'H': h, 'B': b, 'tw': tw, 'tfl': tfl}
    if _temp in temp_files:
        exist_flag = True
        pass
    else:
        a_fl = b * tfl
        a_w = (h - tfl) * tw
        grav1 = Point(b / 2, tfl / 2, 0)
        grav2 = Point(tw / 2, (h + tfl) / 2, 0)
        x_gr = (grav1.x * a_fl + grav2.x * a_w) / (a_fl + a_w)
        y_gr = (grav1.y * a_fl + grav2.y * a_w) / (a_fl + a_w)
        point1 = (- x_gr + tw, h - y_gr)
        point2 = (- x_gr, h - y_gr)
        point3 = (- x_gr, - y_gr)
        point4 = (b - x_gr, - y_gr)
        point5 = (b - x_gr, tfl - y_gr)
        point6 = (- x_gr + tw, tfl - y_gr)
        points = [point1, point2, point3, point4, point5, point6]
        write_to_txt_1surface(points, profile_path, profile_name, dim_dict)

    return exist_flag


# Create double angle section property
def create_2l(h, b, tw, tfl, dist, profile_path, profile_name):
    os.chdir(profile_path)
    temp_files = glob.glob('*.geo')
    _temp = profile_name + '.geo'
    exist_flag = False
    dim_dict = {'H': h, 'B': b, 'tw': tw, 'tfl': tfl, 'dist': dist}
    if _temp in temp_files:
        exist_flag = True
        pass
    else:
        a_fl = b * tfl
        a_w = (h - tfl) * tw
        grav1 = Point(b / 2, tfl / 2, 0)
        grav2 = Point(tw / 2, (h + tfl) / 2, 0)
        x_gr = (grav1.x * a_fl + grav2.x * a_w) / (a_fl + a_w)
        y_gr = (grav1.y * a_fl + grav2.y * a_w) / (a_fl + a_w)
        d = dist / 2
        point1 = (d + tw, h - y_gr)
        point2 = (d, h - y_gr)
        point3 = (d, - y_gr)
        point4 = (d + b, - y_gr)
        point5 = (d + b, tfl - y_gr)
        point6 = (d + tw, tfl - y_gr)
        points = [point1, point2, point3, point4, point5, point6]
        write_to_txt_1surface(points, profile_path, profile_name, dim_dict)
        point1 = (- d, h - y_gr)
        point2 = (- d - tw, h - y_gr)
        point3 = (- d - tw, tfl - y_gr)
        point4 = (- d - b, tfl - y_gr)
        point5 = (- d - b, - y_gr)
        point6 = (- d, - y_gr)
        points = [point1, point2, point3, point4, point5, point6]
        write_to_txt_num_surface(points, profile_path, profile_name, '2')

    return exist_flag


# Create double cruciform angle section property
def create_2l_cruciform(h, b, tw, tfl, dist, profile_path, profile_name):
    os.chdir(profile_path)
    temp_files = glob.glob('*.geo')
    _temp = profile_name + '.geo'
    exist_flag = False
    dim_dict = {'H': h, 'B': b, 'tw': tw, 'tfl': tfl, 'dist': dist}
    if _temp in temp_files:
        exist_flag = True
        pass
    else:
        a_fl = b * tfl
        a_w = (h - tfl) * tw
        grav1 = Point(b / 2, tfl / 2, 0)
        grav2 = Point(tw / 2, (h + tfl) / 2, 0)
        x_gr1 = (grav1.x * a_fl + grav2.x * a_w) / (a_fl + a_w)
        y_gr1 = (grav1.y * a_fl + grav2.y * a_w) / (a_fl + a_w)
        x_tel = (x_gr1 * (a_fl + a_w) + (- x_gr1 + tw) * (a_fl + a_w)) / (2 * (a_fl + a_w))
        y_tel = (y_gr1 * (a_fl + a_w) + (- y_gr1 - dist) * (a_fl + a_w)) / (2 * (a_fl + a_w))
        d = dist / 2
        point1 = (tw / 2, h + d)
        point2 = (- (tw / 2), h + d)
        point3 = (- (tw / 2), tfl + d)
        point4 = (- b + (tw / 2), tfl + d)
        point5 = (- b + (tw / 2), d)
        point6 = (tw / 2, d)
        points = [point1, point2, point3, point4, point5, point6]
        write_to_txt_1surface(points, profile_path, profile_name, dim_dict)
        point1 = (- (tw / 2), - h - d)
        point2 = (tw / 2, - h - d)
        point3 = (tw / 2, - tfl - d)
        point4 = (b - (tw / 2), - tfl - d)
        point5 = (b - (tw / 2), - d)
        point6 = (- (tw / 2), - d)
        points = [point1, point2, point3, point4, point5, point6]
        write_to_txt_num_surface(points, profile_path, profile_name, '2')

    return exist_flag


# Create cruciform 4 angle section property
def create_4l(h, b, tw, tfl, dist, profile_path, profile_name):
    os.chdir(profile_path)
    temp_files = glob.glob('*.geo')
    _temp = profile_name + '.geo'
    exist_flag = False
    dim_dict = {'H': h, 'B': b, 'tw': tw, 'tfl': tfl, 'dist': dist}
    if _temp in temp_files:
        exist_flag = True
        pass
    else:
        a_fl = b * tfl
        a_w = (h - tfl) * tw
        grav1 = Point(b / 2, tfl / 2, 0)
        grav2 = Point(tw / 2, (h + tfl) / 2, 0)
        x_gr = (grav1.x * a_fl + grav2.x * a_w) / (a_fl + a_w)
        y_gr = (grav1.y * a_fl + grav2.y * a_w) / (a_fl + a_w)
        d = dist / 2
        point1 = (d + tw, d + h)
        point2 = (d, d + h)
        point3 = (d, d)
        point4 = (d + b, d)
        point5 = (d + b, d + tfl)
        point6 = (d + tw, d + tfl)
        points = [point1, point2, point3, point4, point5, point6]
        write_to_txt_1surface(points, profile_path, profile_name, dim_dict)
        point1 = (- d, d + h)
        point2 = (- d - tw, d + h)
        point3 = (- d - tw, d + tfl)
        point4 = (- d - b, d + tfl)
        point5 = (- d - b, d)
        point6 = (- d, d)
        points = [point1, point2, point3, point4, point5, point6]
        write_to_txt_num_surface(points, profile_path, profile_name, '2')
        point1 = (- d - tw, - d - h)
        point2 = (- d, - d - h)
        point3 = (- d, - d)
        point4 = (- d - b, - d)
        point5 = (- d - b, - d - tfl)
        point6 = (- d - tw, - d - tfl)
        points = [point1, point2, point3, point4, point5, point6]
        write_to_txt_num_surface(points, profile_path, profile_name, '3')
        point1 = (d, - d - h)
        point2 = (d + tw, - d - h)
        point3 = (d + tw, - d - tfl)
        point4 = (d + b, - d - tfl)
        point5 = (d + b, - d)
        point6 = (d, - d)
        points = [point1, point2, point3, point4, point5, point6]
        write_to_txt_num_surface(points, profile_path, profile_name, '4')

    return exist_flag


# Create cruciform section property
def create_cruciform(h, b, tw, tfl, profile_path, profile_name):
    os.chdir(profile_path)
    temp_files = glob.glob('*.geo')
    _temp = profile_name + '.geo'
    exist_flag = False
    dim_dict = {'H': h, 'B': b, 'tw': tw, 'tfl': tfl}
    if _temp in temp_files:
        exist_flag = True
        pass
    else:
        a_fl = b * tfl
        a_w = (h - tfl) * tw
        point1 = (tw / 2, tfl / 2)
        point2 = (tw / 2, h / 2)
        point3 = (- (tw / 2), h / 2)
        point4 = (- (tw / 2), tfl / 2)
        point5 = (- (b / 2), tfl / 2)
        point6 = (- (b / 2), - (tfl / 2))
        point7 = (- (tw / 2), - (tfl / 2))
        point8 = (- (tw / 2), - (h / 2))
        point9 = (tw / 2, - (h / 2))
        point10 = (tw / 2, - (tfl / 2))
        point11 = (b / 2, - (tfl / 2))
        point12 = (b / 2, tfl / 2)
        points = [point1, point2, point3, point4, point5, point6, point7, point8, point9, point10, point11, point12]
        write_to_txt_1surface(points, profile_path, profile_name, dim_dict)

    return exist_flag


# Create I section property
def create_Isection(h, b, tw, tfl, profile_path, profile_name):
    os.chdir(profile_path)
    temp_files = glob.glob('*.geo')
    _temp = profile_name + '.geo'
    exist_flag = False
    dim_dict = {'H': h, 'B': b, 'tw': tw, 'tfl': tfl}
    if _temp in temp_files:
        exist_flag = True
        pass
    else:
        a_fl = b * tfl
        a_w = (h - tfl) * tw
        point1 = (tw / 2, (h / 2) - tfl)
        point2 = (b / 2, (h / 2) - tfl)
        point3 = (b / 2, h / 2)
        point4 = (- (b / 2), h / 2)
        point5 = (- (b / 2), (h / 2) - tfl)
        point6 = (- (tw / 2), (h / 2) - tfl)
        point7 = (- (tw / 2), - (h / 2) + tfl)
        point8 = (- (b / 2), - (h / 2) + tfl)
        point9 = (- (b / 2), - (h / 2))
        point10 = (b / 2, - (h / 2))
        point11 = (b / 2, - (h / 2) + tfl)
        point12 = (tw / 2, - (h / 2) + tfl)
        points = [point1, point2, point3, point4, point5, point6, point7, point8, point9, point10, point11, point12]
        write_to_txt_1surface(points, profile_path, profile_name, dim_dict)

    return exist_flag


# Create tee section property
def create_tee(h, b, tw, tfl, profile_path, profile_name):
    os.chdir(profile_path)
    temp_files = glob.glob('*.geo')
    _temp = profile_name + '.geo'
    exist_flag = False
    dim_dict = {'H': h, 'B': b, 'tw': tw, 'tfl': tfl}
    if _temp in temp_files:
        exist_flag = True
        pass
    else:
        a_fl = b * tfl
        a_w = (h - tfl) * tw
        grav1 = Point(0, h - (tfl / 2), 0)
        grav2 = Point(0, (h - tfl) / 2, 0)
        y_gr = (grav1.y * a_fl + grav2.y * a_w) / (a_fl + a_w)
        point1 = (tw / 2, h - y_gr - tfl)
        point2 = (b / 2, h - y_gr - tfl)
        point3 = (b / 2, h - y_gr)
        point4 = (- (b / 2), h - y_gr)
        point5 = (- (b / 2), h - y_gr - tfl)
        point6 = (- (tw / 2), h - y_gr - tfl)
        point7 = (- (tw / 2), - y_gr)
        point8 = (tw / 2, - y_gr)
        points = [point1, point2, point3, point4, point5, point6, point7, point8]
        write_to_txt_1surface(points, profile_path, profile_name, dim_dict)

    return exist_flag


@staticmethod
def write_to_txt_1surface(points, profile_path, profile_name, dim_dict):
    _temp = profile_path + '/' + profile_name + '.geo'
    with open(_temp, 'w', encoding='UTF8', newline='') as f:
        f.write('// Gmsh project')
        f.write('\nSetFactory("OpenCASCADE");')
        for key in dim_dict:
            f.write('\n' + f'{key} = ' + f'{dim_dict[key]}' + ';')
        for i in range(len(points)):
            f.write('\n// +')
            help1 = round(points[i][0], 6)
            help2 = round(points[i][1], 6)
            f.write('\nPoint(' + f'{i+1}' + ') = {' + f'{help1}' + ', ' + f'{help2}' + ', 0, 1.0};')
        for i in range(len(points) - 1):
            f.write('\n// +')
            f.write('\nLine(' + f'{i + 1}' + ') = {' + f'{i + 1}' + ', ' + f'{i + 2}' + '};')
        curve = list(range(1, len(points) + 1))
        curve = curve[-1:] + curve[:-1]
        f.write('\n// +')
        f.write('\nLine(' + f'{len(points)}' + ') = {' + f'{len(points)}' + ', ' + '1};')
        f.write('\n// +')
        f.write('\nCurve Loop(1) = {')
        for i in range(len(points) - 1):
            f.write(f'{curve[i]}' + ', ')
        f.write(f'{curve[len(points) - 1]}' + '};')
        f.write('\n// +')
        f.write('\nPlane Surface(1) = {1};')
        f.write('\n')


@staticmethod
def write_to_txt_num_surface(points, profile_path, profile_name, num):
    int_num = int(num)
    num_points = len(points)
    _temp = profile_path + '/' + profile_name + '.geo'
    with open(_temp, 'a', encoding='UTF8', newline='') as f:
        for i in range(num_points):
            f.write('\n// +')
            help1 = round(points[i][0], 6)
            help2 = round(points[i][1], 6)
            f.write('\nPoint(' + f'{i + 1 + (int_num - 1) * num_points}' + ') = {' + f'{help1}' + ', ' + f'{help2}' +
                    ', 0, 1.0};')
        for i in range(num_points - 1):
            f.write('\n// +')
            f.write('\nLine(' + f'{i + 1 + (int_num - 1) *  num_points}' + ') = {' +
                    f'{i + 1 + (int_num - 1) *  num_points}' + ', ' + f'{i + 2 + (int_num - 1) *  num_points}' + '};')
        curve = list(range(1, num_points + 1))
        curve = curve[-1:] + curve[:-1]
        f.write('\n// +')
        f.write('\nLine(' + f'{int_num * num_points}' + ') = {' + f'{int_num * num_points}' + ', ' +
                f'{(int_num - 1) * num_points + 1}' + '};')
        f.write('\n// +')
        f.write('\nCurve Loop(' + num + ') = {')
        for i in range(num_points - 1):
            f.write(f'{curve[i] + num_points}' + ', ')
        f.write(f'{curve[num_points - 1] + num_points}' + '};')
        f.write('\n// +')
        f.write('\nPlane Surface(' + num + ') = {' + num + '};')
        f.write('\n')

