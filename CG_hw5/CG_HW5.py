'''
CG_hw5.py
Franco Pettigrosso
Creates the robot arm
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
    def __init__(self, t_input, u_input, v_input, l_input, m_input, n_input):
        self.t1_angle = t_input
        self.u2_angle = u_input
        self.v3_angle = v_input
        self.lenght_1 = l_input
        self.lenght_2 = m_input
        self.lenght_3 = n_input

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

def Translate(axis_x=0.0, axis_y=0.0, axis_z=0.0 ):
    return [
        [1.0, 0.0, 0.0, axis_x],
        [0.0, 1.0, 0.0, axis_y],
        [0.0, 0.0, 1.0, axis_z],
        [0.0, 0.0, 0.0, 1.0]
    ]

get_radian = lambda x: np.radians(x)
get_cos = lambda x: np.cos(get_radian(x))
get_sin = lambda x: np.sin(get_radian(x))


def get_degrees(theta):
    degrees = {}
    degrees['sin'] = get_sin(theta)
    degrees['minus_sin'] = get_sin(theta) * -1.0
    degrees['cos'] = get_cos(theta)
    degrees['minus_cos'] = get_cos(theta) * -1.0


def axis_x_rotation(degrees):
    return [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, degrees['cos'], degrees['minus_sin'], 0.0],
        [0.0, degrees['sin'], degrees['minus_cos'], 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ]

def axis_y_rotation(degrees):
    return [
        [degrees['cos'], 0.0, degrees['sin'], 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [degrees['minus_sin'], 0.0, degrees['cos'], 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ]

def axis_z_rotation(degrees):
    return [
        [degrees['cos'], degrees['minus_sin'], 0.0, 0.0],
        [degrees['sin'], degrees['cos'], 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ]





def main(given_args_params):



if __name__ == '__main__':
    '''
    parses arguements so we can make our 3d shape
    '''
    PARSER = argparse.ArgumentParser()
    ARG_GROUP = PARSER.add_argument_group()
    ARG_GROUP.add_argument('-t', '--O1', type=str)
    ARG_GROUP.add_argument('-u', '--O2', type=str)
    ARG_GROUP.add_argument('-v', '--O3', type=str)
    ARG_GROUP.add_argument('-l', '--L1', type=str)
    ARG_GROUP.add_argument('-m', '--L2', type=str)
    ARG_GROUP.add_argument('-n', '--L3', type=str)
    ARGS = PARSER.parse_args()

    INPUTS = given_args(
        t_input=parse_input(ARGS.O1, -51, True),
        u_input=parse_input(ARGS.O2, 39 , True),
        v_input=parse_input(ARGS.O3, 65 , True),
        l_input=parse_input(ARGS.L1, 4, True),
        m_input=parse_input(ARGS.L2, 3, True),
        n_input=parse_input(ARGS.L3, 2.5, True),
    )
    main(INPUTS)