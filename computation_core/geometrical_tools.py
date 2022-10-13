import math


class Mesh:
    def __init__(self, num_id, point_min, point_max, point_step):
        self.ID = num_id
        self.point_min = point_min
        self.point_max = point_max
        self.point_step = point_step


class Point:
    def __init__(self, x, y, z, num_id='1', weight_xy=1, weight_z=1):
        self.ID = num_id
        self.x = x
        self.y = y
        self.z = z
        self.weight_xy = weight_xy
        self.weight_z = weight_z


class Line:
    line_length = 0
    point_start = Point(0, 0, 0)
    point_end = Point(0, 0, 0)

    def __init__(self, num_id, point_start, point_end, devices=None):
        if devices is None:
            devices = []
        self.ID = num_id
        self.point_start = point_start
        self.point_end = point_end
        self.devices = devices

    def length(self):
        self.line_length = math.sqrt(pow(self.point_end.x - self.point_start.x, 2) + pow(self.point_end.y -
                                     self.point_start.y, 2) + pow(self.point_end.z - self.point_start.z, 2))
