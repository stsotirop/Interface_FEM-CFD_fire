import matplotlib.pyplot as plt
import math
from geometrical_tools import Point, Mesh, Line


def heb400_view_angles():
    h = 0.400
    b = 0.300
    tw = 0.0135
    tfl = 0.024
    r = 0.027

    points = [Point(0, 0, 0), Point(tw / 2, h / 2 - tfl, 0), Point(b / 2, h / 2 - tfl, 0), Point(b / 2, h / 2, 0),
              Point(-b / 2, h / 2, 0), Point(-b / 2, h / 2 - tfl, 0), Point(-tw / 2, h / 2 - tfl, 0),
              Point(-tw / 2, -h / 2 + tfl, 0), Point(-b / 2, -h / 2 + tfl, 0), Point(-b / 2, -h / 2, 0),
              Point(b / 2, -h / 2, 0), Point(b / 2, -h / 2 + tfl, 0), Point(tw / 2, -h / 2 + tfl, 0)]

    _fig = plt.figure()
    for i in range(1, 12):
        point1 = points[i]
        point2 = points[i + 1]
        x = [point1.x, point2.x]
        y = [point1.y, point2.y]
        plt.plot(x, y, 'black')
    point1 = points[12]
    point2 = points[1]
    x = [point1.x, point2.x]
    y = [point1.y, point2.y]
    plt.plot(x, y, 'black')

    # test for web right
    test_point = Point(0, 0, 0)

    if is_between(points[12], points[1], test_point):
        angle, bisector_orientation = evaluate_angle(test_point, points[11], points[2])
        print(f"Test point is in line 12-1 and the view angle is {angle}")
        print(bisector_orientation)
    elif is_between(points[1], points[2], test_point):
        angle, bisector_orientation = evaluate_angle(test_point, points[11], points[2])
        print(f"Test point is in line 1-2 and the view angle is {angle}")
        print(bisector_orientation)
    elif is_between(points[5], points[6], test_point):
        angle, bisector_orientation = evaluate_angle(test_point, points[5], points[8])
        print(f"Test point is in line 5-6 and the view angle is {angle}")
        print(bisector_orientation)
    elif is_between(points[6], points[7], test_point):
        angle, bisector_orientation = evaluate_angle(test_point, points[5], points[8])
        print(f"Test point is in line 6-7 and the view angle is {angle}")
        print(bisector_orientation)
    elif is_between(points[7], points[8], test_point):
        angle, bisector_orientation = evaluate_angle(test_point, points[5], points[8])
        print(f"Test point is in line 7-8 and the view angle is {angle}")
        print(bisector_orientation)
    elif is_between(points[11], points[12], test_point):
        angle, bisector_orientation = evaluate_angle(test_point, points[11], points[2])
        print(f"Test point is in line 11-12 and the view angle is {angle}")
        print(bisector_orientation)
    else:
        print("Test point is not a part of a line")

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


def is_between(a, b, c):
    epsilon = 1e-6
    cross_product = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)
    if abs(cross_product) > epsilon:
        return False
    dot_product = (c.x - a.x) * (b.x - a.x) + (c.y - a.y)*(b.y - a.y)
    if dot_product < 0:
        return False
    squared_length_ba = (b.x - a.x)*(b.x - a.x) + (b.y - a.y)*(b.y - a.y)
    if dot_product > squared_length_ba:
        return False
    return True


def evaluate_angle(test_point, point1, point2):
    # Define limits - view angle
    line1 = [point1.x - test_point.x, point1.y - test_point.y, 0]
    x = [test_point.x, point1.x]
    y = [test_point.y, point1.y]
    plt.plot(x, y, 'black')
    line2 = [point2.x - test_point.x, point2.y - test_point.y, 0]
    x = [test_point.x, point2.x]
    y = [test_point.y, point2.y]
    plt.plot(x, y, 'black')

    # Calculate the angle between the vectors
    asd = line1[0] * line2[0] + line1[1] * line2[1]
    det1 = line1[0] * line2[1] - line1[1] * line2[0]
    angle1 = math.degrees(math.atan2(-det1, -asd) + math.pi)

    # Evaluate and draw bisector
    metro1 = math.sqrt(pow(line1[0], 2) + pow(line1[1], 2))
    metro2 = math.sqrt(pow(line2[0], 2) + pow(line2[1], 2))
    line3 = [metro2 * line1[0] + metro1 * line2[0], metro2 * line1[1] + metro1 * line2[1], 0]
    x = [test_point.x, line3[0] + test_point.x]
    y = [test_point.y, line3[1] + test_point.y]
    plt.plot(x, y, 'black')

    return angle1, line3
