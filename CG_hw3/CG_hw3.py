import argparse
import copy #to get a copy of the orginal inputs
from math import factorial
from numpy import arange
from enum import Enum

class surface_options(Enum):
    flat = 1
    smooth = 2

def get_matrix(file_path):
    '''
    reads in the input file and converts
    it into a matrix.
    '''
    input_matrix = []
    with open(file_path, 'r') as file:
        for line in file:
            temp_matrix = []
            for column in line.split(" "):
                temp_matrix.append(float(column))
            line_only_contains_three_points = len(temp_matrix) == 3
            if line_only_contains_three_points:
                    input_matrix.append(temp_matrix)

            else:
                Exception('the rows can only contain 3d points')
    return input_matrix

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

def split_up(list_to_split_up):
    temp_x = []
    temp_y = []
    temp_z = []
    for row in list_to_split_up:
        temp_x.append(row[0] * 1.0)
        temp_y.append(row[1] * 1.0)
        temp_z.append(row[2] * 1.0)
    return temp_x, temp_y, temp_z



#GIVEN_FILE, GIVEN_U, GIVEN_V, GIVEN_RADIUS, surface_options.flat
def main(file_path, u_point, v_point, radius, surface_option):
    raw_matrix = get_matrix(file_path)
    #cut them up in columns so its easier to work with
    column_x, column_y, column_z = split_up(raw_matrix)

if __name__ == '__main__':
    '''
    parses arguements
    '''
    PARSER = argparse.ArgumentParser()
    ARG_GROUP = PARSER.add_argument_group()
    ARG_GROUP.add_argument('-f', '--file', help='The matrix with he input', type=str)
    ARG_GROUP.add_argument('-u', '--uIteration', help='How many times to iterate over the first Bernstein polynomial', type=str)
    ARG_GROUP.add_argument('-v', '--vIteration', help='How many times to iterate over the second Bernstein polynomial', type=str)
    ARG_GROUP.add_argument('-r', '--radius', help='radius of the spheres', type=str)
    ARG_GROUP.add_argument('-F', '--flat_shaded', help='flat-shaded', type= bool, nargs='?', const=True, default=False)
    ARG_GROUP.add_argument('-S', '--smooth_shaded', help='smooth-shaded', type= bool, nargs='?', const=True, default=False)
    ARGS = PARSER.parse_args()
    GIVEN_FILE = parse_input(ARGS.file, './cpts_in.txt')
    GIVEN_U = parse_input(ARGS.uIteration, 11, True)
    GIVEN_V = parse_input(ARGS.vIteration, 11, True)
    GIVEN_RADIUS = parse_input(ARGS.radius, 0.1, True)
    s_is_true = ARGS.smooth_shaded == True
    if(s_is_true):
        main(GIVEN_FILE, GIVEN_U, GIVEN_V, GIVEN_RADIUS, surface_options.smooth) 
    else:
        main(GIVEN_FILE, GIVEN_U, GIVEN_V, GIVEN_RADIUS, surface_options.flat)