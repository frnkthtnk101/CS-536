'''
CG_hw4.py
Franco Pettigrosso
creates the Superellipsoid
'''
from enum import Enum
import argparse
import numpy as np

class surface_options(Enum):
    '''
    just a way to keep things formal
    '''
    flat = 1
    smooth = 2

class given_args():
    '''
    puts all the args and properties
    in a convient package.
    '''
    def __init__(self,
                 a_scalar_input, b_scalar_input, c_scalar_input, r_input,
                 t_input, u_input, v_input, face_input):
        self.a_scalar = a_scalar_input
        self.b_scalar = b_scalar_input
        self.c_scalar = c_scalar_input
        self.r_s1 = r_input
        self.t_s2 = t_input
        self.u_point = u_input
        self.v_point = v_input
        self.face_type = face_input
        #https://docs.scipy.org/doc/numpy/reference/generated/numpy.linspace.html
        self.u_points = np.linspace(-np.pi, np.pi, u_input)
        self.v_points = np.linspace(-(np.pi / 2), (np.pi / 2), v_input)
        self.u_points_len = len(self.u_points)
        self.v_points_len = len(self.v_points)
        self.u_points_triangles = np.arange(0, 1.01, 1 / u_input)
        self.v_points_triangles = np.arange(0, 1.01, 1 / v_input)
        self.u_points_triangles_len = len(self.u_points_triangles)
        self.v_points_triangles_len = len(self.v_points_triangles)

def parse_input(given_input, default, to_number=False):
    '''
    decides if given input or just default
    '''
    is_not_given = given_input is None
    if is_not_given:
        if to_number:
            return float(default)
        return default
    if to_number:
        return float(given_input)
    return given_input

def sgn(angle):
    '''
    SGN function defined in the slides.
    '''
    if angle == 0:
        return 0
    if angle > 0:
        return 1
    return -1

auxiliary_function_c = lambda w, m: sgn(np.cos(w)) * np.power(np.absolute(np.cos(w)), m)
auxiliary_function_s = lambda w, m: sgn(np.sin(w)) * np.power(np.absolute(np.sin(w)), m)
x_function = lambda u, v, r, t, a: a * auxiliary_function_c(v, r) * auxiliary_function_c(u, t)
y_function = lambda u, v, r, t, b: b * auxiliary_function_c(v, r) * auxiliary_function_s(u, t)
z_function = lambda v, r, c: c * auxiliary_function_s(v, r)

def define_triangles(blended_matrix, given_args_params):
    '''
    creates the triangles of the 3d shape.
    '''
    the_triangles = []
    triangle_calculation = lambda x, y, z: x * y + z
    for i in range(0, given_args_params.v_points_triangles_len):
        for j in range(0, given_args_params.u_points_triangles_len):
            triangle_1 = [
                triangle_calculation(given_args_params.u_point, i, j),
                triangle_calculation(given_args_params.u_point, i, j + 1),
                triangle_calculation(given_args_params.u_point, i + 1, j + 1),
            ]
            triangle_2 = [
                triangle_calculation(given_args_params.u_point, i, j),
                triangle_calculation(given_args_params.u_point, i + 1, j + 1),
                triangle_calculation(given_args_params.u_point, i + 1, j),
            ]
            the_triangles.append(triangle_1)
            the_triangles.append(triangle_2)
    return the_triangles

def list_to_string(input_list, suffix=',', to_float=True):
    '''
    converts all the misc list into something useable
    by the iv file.
    '''
    string_builder = ''
    if to_float:
        for element in input_list:
            string_builder += '{0:.6f} {1:.6f} {2:.6f}{3}\r\n'.format(
                element[0],
                element[1],
                element[2],
                suffix
            )
    else:
        for element in input_list:
            string_builder += '{0},{1},{2},{3}\r\n'.format(
                str(int(element[0])),
                str(int(element[1])),
                str(int(element[2])),
                suffix
            )
    return string_builder

def list_to_string_normal(input_list):
    '''
    converts the normal list into something
    the iv file can interpret.
    '''
    string_builder = ''
    for element in input_list:
        string_builder += '{0:.6f} {1:.6f} {2:.6f},\r\n'.format(
            element[0],
            element[1],
            element[2]
        )
    return string_builder

def create_file(points, normalized_points, triangle_points, face_type):
    '''
    prints out the iv file
    '''
    is_smooth_shaded = face_type is surface_options.smooth
    string_builder = '#Inventor V2.0 ascii\r\nShapeHints '
    string_builder += '{\r\n vertexOrdering COUNTERCLOCKWISE \r\n}\r\n'
    string_builder += 'Separator {\r\n Coordinate3 {\r\npoint [\r\n'
    string_builder += list_to_string(points)
    string_builder += ']\r\n}\r\n'
    if is_smooth_shaded:
        string_builder += 'NormalBinding {\r\nvalue PER_VERTEX_INDEXED}\r\nNormal {\r\nvector [\r\n'
        string_builder += list_to_string_normal(normalized_points)
        string_builder += ']\r\n}\r\n'
    string_builder += 'IndexedFaceSet {\r\ncoordIndex[\r\n'
    string_builder += list_to_string(triangle_points, '-1,', False)
    string_builder += ']\r\n}\r\n}'
    print(string_builder)

def main(given_args_params):
    '''
    Main function of this script:
    gets the point then smooths them.
    Makes the triangles and then prints
    the results.
    '''
    points = []
    normalized_points = []
    triangle_points = []
    #gen points
    points.append([0.000000, 0.000000, 1.000000])
    for v_point in given_args_params.v_points:
        for u_point in given_args_params.u_points:
            points.append(
                [
                    x_function(
                        u_point, v_point, given_args_params.r_s1,
                        given_args_params.t_s2,
                        given_args_params.a_scalar
                        ),
                    y_function(
                        u_point, v_point, given_args_params.r_s1,
                        given_args_params.t_s2,
                        given_args_params.b_scalar
                        ),
                    z_function(v_point, given_args_params.r_s1,
                               given_args_params.c_scalar),
                ]
            )
            normalized_points.append(
                [
                    x_function(
                        u_point, v_point, 2 - given_args_params.r_s1,
                        2 - given_args_params.t_s2,
                        1 / given_args_params.a_scalar
                        ),
                    y_function(
                        u_point, v_point, 2 - given_args_params.r_s1,
                        2 - given_args_params.t_s2,
                        1 / given_args_params.b_scalar
                        ),
                    z_function(v_point, 2 - given_args_params.r_s1,
                               1 / given_args_params.c_scalar),
                ]
            )
    points.append([0.000000, 0.000000, -1.000000])
    triangle_points = define_triangles(points, given_args_params)
    create_file(points, normalized_points, triangle_points, given_args_params.face_type)

if __name__ == '__main__':
    '''
    parses arguements so we can make our 3d shape
    '''
    PARSER = argparse.ArgumentParser()
    ARG_GROUP = PARSER.add_argument_group()
    ARG_GROUP.add_argument('-u', '--u_iteration', type=str)
    ARG_GROUP.add_argument('-v', '--v_iteration', type=str)
    ARG_GROUP.add_argument('-A', '--a_scalar', type=str)
    ARG_GROUP.add_argument('-B', '--b_scalar', type=str)
    ARG_GROUP.add_argument('-C', '--c_scalar', type=str)
    ARG_GROUP.add_argument('-r', '--s1', type=str)
    ARG_GROUP.add_argument('-t', '--s2', type=str)
    ARG_GROUP.add_argument('-F', '--flat', action='store_true')
    ARG_GROUP.add_argument('-S', '--smooth', action='store_true')
    ARGS = PARSER.parse_args()
    USE_SMOOTHING = ARGS.smooth is True
    if USE_SMOOTHING:
        FACE_INPUT = surface_options.smooth
    else:
        FACE_INPUT = surface_options.flat
    INPUTS = given_args(
        a_scalar_input=parse_input(ARGS.a_scalar, 1, True),
        b_scalar_input=parse_input(ARGS.b_scalar, 1, True),
        c_scalar_input=parse_input(ARGS.c_scalar, 1, True),
        r_input=parse_input(ARGS.s1, 1, True),
        t_input=parse_input(ARGS.s2, 1, True),
        u_input=parse_input(ARGS.u_iteration, 19, True),
        v_input=parse_input(ARGS.v_iteration, 19, True),
        face_input=FACE_INPUT
    )
    main(INPUTS)