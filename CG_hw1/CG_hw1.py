'''
CG_hw1.py
Arbitrary-degree Bezier Curves
Franco Pettigrosso

Creates and file for Arbitrary-degree Bezier Curves
given a file du and radios

you can do a search for requirement[space][number] to go
the locations of the requirements of the homework

module references
areparse - used to get input in python (or atleast how I know how to do it)
factorial - used to get n! so I do not have to program it
arange - used to spread the du into nice pieces
'''
import argparse
from math import factorial
from numpy import arange


def control_point_calculation(length, index):
    '''
    This is the (k,u) part of the equation
    '''
    return factorial(length) / (factorial(index) * factorial(length - index))

def u_calculation(length, index, current_u_point):
    '''
    This is the far right side of the equation
    '''
    reverse_u = 1 - current_u_point
    pow_by = length - index
    left = pow(reverse_u, pow_by)
    right = pow(current_u_point, index)
    return left * right

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
            #reqirement 1 3d point -v
            if line_only_contains_three_points:
                input_matrix.append(temp_matrix)
            else:
                Exception('the rows can only contain 3d points')
    return input_matrix

def calculate_arb_bezier_curve(input_matrix, du_point):
    '''
    the bezier equation
    '''
    results_matrix = []
    #the k part v
    rows_length = len(input_matrix) - 1
    #used to when determining what axis the script is on
    columns = len(input_matrix[0])
    for current_u_point in arange(0.0, 1.01, (1/du_point)):
        temp_columns = [0.0] * columns
        for index_row in range(0, rows_length + 1):
            for axis_index in range(0, columns):
                cpc = control_point_calculation(rows_length, index_row)
                u_cal = u_calculation(rows_length, index_row, current_u_point)
                temp_columns[axis_index] += \
                    input_matrix[index_row][axis_index] * cpc * u_cal
        results_matrix.append(temp_columns)
    return results_matrix

def create_file(input_file, results_file, radius):
    '''
    abstracted function that creates the file
    #requirement 7 open inventor format
    '''
    results_file_length = len(results_file)
    #requirement 5 degree N-1 -v
    input_file_length = len(input_file) - 1
    string_builder = "#Inventor V2.0 ascii \r\n"
    string_builder += matrix_to_string(results_file, results_file_length)
    string_builder += create_sphere(radius, input_file, input_file_length)
    return string_builder

def create_sphere(radius, input_file, results_file_column_length):
    '''
    used to create a sphere in the file
    requirement 3 the controll points are rep by spheres
    '''
    results_file_column_length_lth_zero = results_file_column_length < 0
    if results_file_column_length_lth_zero:
        return ''
    string_builder = 'Separator {LightModel {model PHONG}Material {	diffuseColor 1.0 1.0 1.0}'
    string_builder += 'Transform {translation\r\n'
    string_builder += '{0}  {1}  {2}\r\n' \
    .format(input_file[results_file_column_length][0],
            input_file[results_file_column_length][1],
            input_file[results_file_column_length][2])
    string_builder += '}}Sphere {{	radius {0} }}}}\r\n'.format(radius)
    return string_builder + create_sphere(radius, input_file, results_file_column_length - 1)

def  matrix_to_string(results_file, results_file_length):
    '''
    converts a the given matrix into the iv format
    '''
    string_builder = 'Separator {LightModel {model BASE_COLOR} Material ' + \
    '{diffuseColor 1.0 1.0 1.0}\r\n'
    string_builder += 'Coordinate3 { 	point [ \r\n'
    for index in range(0, results_file_length):
        is_last_row = results_file_length - 1 == index
        if is_last_row:
            string_builder += '{:5f} {:5f} {:5f}\r\n' \
            .format(results_file[index][0],
                    results_file[index][1],
                    results_file[index][2])
        else:
            string_builder += '{:5f} {:5f} {:5f}, \r\n' \
            .format(results_file[index][0],
                    results_file[index][1],
                    results_file[index][2])
    string_builder += '] }\r\n IndexedLineSet {coordIndex ['
    for i in range(0, results_file_length):
        string_builder += '{0}, '.format(i)
    string_builder += '-1, ] } }\r\n'
    return string_builder


def parse_input(given_input, default):
    '''
    decides if given input or just default
    '''
    is_not_given = given_input is None
    if is_not_given:
        return default
    return given_input

def main(input_matrix, given_du, radius=0.1):
    '''
    The main function
    creates the matrix then creates the final output
    '''
    results_matrix = calculate_arb_bezier_curve(input_matrix, given_du)
    results_file = create_file(input_matrix, results_matrix, radius)
    print(results_file)

if __name__ == '__main__':
    '''
    parses arguements
    '''
    PARSER = argparse.ArgumentParser()
    ARG_GROUP = PARSER.add_argument_group()
    #requirement 1 -f for filename --v
    ARG_GROUP.add_argument('-f', '--file', help='The matrix with he input', type=str)
    #requirement 2 -u for du --v
    ARG_GROUP.add_argument('-n', '--upoint', help='use the best', type=str)
    #requirement 4 spheres modification -r -v
    ARG_GROUP.add_argument('-r', '--radius', help='radius of the spheres', type=str)
    ARGS = PARSER.parse_args()
    #requirement 1 defaults to cpts_in.txt -V
    GIVEN_MATRIX = get_matrix(parse_input(ARGS.file, './cpts_in.txt'))
    #requirement 2 du defaults to 0.05 -v
    GIVEN_DU = float(parse_input(ARGS.upoint, 20))
    #requirement 2 du is between or equal to 0 and 1
    DU_IS_BETWEEN_ZERO_AND_ONE = True
    #requirement 4 spheres default to .1 -v
    GIVEN_RADIUS = parse_input(ARGS.radius, 0.1)
    if DU_IS_BETWEEN_ZERO_AND_ONE:
        main(GIVEN_MATRIX, GIVEN_DU, GIVEN_RADIUS)
    else:
        print("du is not between/or 0 and 1")
