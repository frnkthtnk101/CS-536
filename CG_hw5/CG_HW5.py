'''
CG_hw5.py
Franco Pettigrosso
Creates the robot arm
'''
from enum import Enum
import argparse
import numpy as np


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
    return degrees


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

def define_model(length):
    return [
        [0.5, 0.5, length, 1], 
        [-0.5, 0.5, length, 1], 
        [-0.5, -0.5, length, 1], 
        [0.5, -0.5, length, 1], 
        [0.5, 0.5, 0, 1], 
        [-0.5, 0.5, 0, 1], 
        [-0.5, -0.5, 0, 1], 
        [0.5, -0.5, 0, 1]
    ]

def create_model(translation, rotation, length):
    model = np.array(define_model(length))
    translation = np.array(translation)
    rotation = np.array(rotation)
    dot_product_translation_rotation = translation.dot(rotation)
    return np.matmul(model, dot_product_translation_rotation)[:,[0,1,2]]

def create_separator(input_list):
    string_builder = '''Separator {
  Coordinate3 {
    point ['''
    for element in input_list:
        string_builder += '{0:.6f} {1:.6f} {2:.6f},\r\n'.format(
            element[0],
            element[1],
            element[2]
        )
    string_builder += '''
            ]
        }
    IndexedLineSet {
    coordIndex [
	 0, 1, 2, 0, -1,
	 0, 2, 3, 0, -1,
	 7, 6, 5, 7, -1,
	 7, 5, 4, 7, -1,
	 0, 3, 7, 0, -1,
	 0, 7, 4, 0, -1,
	 1, 5, 6, 1, -1,
	 1, 6, 2, 1, -1,
	 0, 4, 5, 0, -1,
	 0, 5, 1, 0, -1,
	 3, 2, 6, 3, -1,
	 3, 6, 7, 3, -1
    ]
  }
}
    '''
    return string_builder

def create_file(box_1, box_2, box_3):
    string_builder = '''Separator {
  Coordinate3 {
    point [
	 -2.000000 -2.000000 0.000000,
	 -2.000000 2.000000 0.000000,
	 2.000000 2.000000 0.000000,
	 2.000000 -2.000000 0.000000,
	 -2.000000 -2.000000 1.000000,
	 -2.000000 2.000000 1.000000,
	 2.000000 2.000000 1.000000,
	 2.000000 -2.000000 1.000000,
    ]
  }
  IndexedLineSet {
    coordIndex [
	 0, 1, 2, 0, -1,
	 0, 2, 3, 0, -1,
	 7, 6, 5, 7, -1,
	 7, 5, 4, 7, -1,
	 0, 3, 7, 0, -1,
	 0, 7, 4, 0, -1,
	 1, 5, 6, 1, -1,
	 1, 6, 2, 1, -1,
	 0, 4, 5, 0, -1,
	 0, 5, 1, 0, -1,
	 3, 2, 6, 3, -1,
	 3, 6, 7, 3, -1
    ]
  }
}
'''
    string_builder += create_separator(box_1)
    string_builder += create_separator(box_2)
    string_builder += create_separator(box_3)
    print(string_builder)

def main(given_args_params):
    #translate
    box_1_translation = Translate(axis_z=given_args_params.lenght_1)
    box_2_translation = Translate(axis_z=given_args_params.lenght_2)
    box_3_translation = Translate(axis_z=given_args_params.lenght_3)
    #rotate
    box_1_rotation = axis_z_rotation(get_degrees(given_args_params.t1_angle))
    box_2_rotation = axis_y_rotation(get_degrees(given_args_params.u2_angle))
    box_3_rotation = axis_y_rotation(get_degrees(given_args_params.v3_angle))
    #boxes
    box_1 = create_model(box_1_translation, box_1_rotation, given_args_params.lenght_1)
    box_2 = create_model(box_2_translation, box_2_rotation, given_args_params.lenght_2)
    box_3 = create_model(box_3_translation, box_3_rotation, given_args_params.lenght_3)
    #circles

    #output
    create_file(box_1, box_2, box_3)


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