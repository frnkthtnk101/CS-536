'''
CG_hw2.py
Franco Pettigrosso
Produces a Catmull-Rom Spline from cords.
'''
import argparse
import copy #to get a copy of the orginal inputs
from math import factorial
from numpy import arange


def create_file(input_file, results_file, radius, number_of_points):
    '''
    abstracted function that creates the file
    '''
    #requirement 5 degree N-1 -v
    input_file_length = len(input_file) - 1
    string_builder = "#Inventor V2.0 ascii \r\n"
    string_builder = 'Separator {LightModel {model BASE_COLOR} Material ' + \
    '{diffuseColor 1.0 1.0 1.0}\r\n'
    string_builder += 'Coordinate3 { 	point [ \r\n'
    for i in results_file:
        string_builder += matrix_to_string(i)
    string_builder += '] }\r\n IndexedLineSet {coordIndex ['
    number_of_cords = (number_of_points + 1) * len(results_file)
    for i in range(0, int(number_of_cords)):
        string_builder += '{0}, '.format(i)
    string_builder += '-1, ] } }\r\n'
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

def  matrix_to_string(results_file):
    '''
    converts a the given matrix into the iv format
    '''
    string_builder = ''
    for index in results_file:
        string_builder += '{:5f} {:5f} {:5f}, \r\n' \
        .format(index[0],
                index[1],
                index[2])
    return string_builder


def get_matrix(file_path):
    '''
    reads in the input file and converts
    it into a matrix.
    '''
    input_matrix = []
    tangent_matrix = []
    tangent_line = 0
    with open(file_path, 'r') as file:
        for line in file:
            temp_matrix = []
            for column in line.split(" "):
                temp_matrix.append(float(column))
            line_only_contains_three_points = len(temp_matrix) == 3
            if line_only_contains_three_points:
                #the first two lines are the tangent points
                tangent_line_below_limit = tangent_line < 2
                if tangent_line_below_limit:
                    tangent_matrix.append(temp_matrix)
                    tangent_line += 1
                else:
                    input_matrix.append(temp_matrix)

            else:
                Exception('the rows can only contain 3d points')
    return input_matrix, tangent_matrix

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

def calculate_arb_bezier_curve(input_matrix, du_point):
    '''
    the bezier equation
    '''
    results_matrix = []
    #the k part v
    rows_length = len(input_matrix) - 1
    #used to when determining what axis the script is on
    columns = len(input_matrix[0])
    for current_u_point in arange(0.0, 1.01, du_point):
        temp_columns = [0.0] * columns
        for index_row in range(0, rows_length + 1):
            for axis_index in range(0, columns):
                cpc = control_point_calculation(rows_length, index_row)
                u_cal = u_calculation(rows_length, index_row, current_u_point)
                temp_columns[axis_index] += \
                    input_matrix[index_row][axis_index] * cpc * u_cal
        results_matrix.append(temp_columns)
    return results_matrix

def calculate_catmull_rom_splines(tanget_points, input_matrix, tension_input, du_point):
    '''
    creates the cordinates for the catmull rom spline at a high level
    '''
    tangents = create_tangent_points(tanget_points, input_matrix, tension_input)
    out_matrix = create_output_matrix(tangents, input_matrix, du_point)
    return out_matrix

def create_output_matrix(tangents, input_matrix, du_point):
    '''
    creates the cordinates for the catmull rom spline
    '''
    def is_quequed(a_list):
        return len(a_list) > 1

    def set_points():
        temp_points = []
        #p1
        temp_points.append(input_matrix[0])
        little_points = []
        #p2
        for i in range(0, 3):
            little_points.append(input_matrix[0][i] + (1/3) * tangents[0][i])
        temp_points.append(little_points)
        #p3
        little_points = []
        for i in range(0, 3):
            little_points.append(input_matrix[1][i] - (1/3) * tangents[1][i])
        temp_points.append(little_points)
        #p4
        temp_points.append(input_matrix[1])
        return temp_points

    output = []
    while is_quequed(input_matrix):
        points = set_points()
        output.append(calculate_arb_bezier_curve(points, du_point))
        input_matrix.pop(0)
        tangents.pop(0)
    return output

def create_tangent_points(tanget_points, input_matrix, tension_input):
    '''
    creates the tangent points for the bazur curve
    '''
    temp_tans = []
    temp_tans_tuple = []
    #t0 = 1-tension * pk
    for j in range(0, 3):
        temp_tans_tuple.append((1-tension_input)*tanget_points[0][j])
    temp_tans.append(temp_tans_tuple)
    #tn-1
    length_of_matrix_minus_one = len(input_matrix) - 1
    is_bigger_than_two = length_of_matrix_minus_one != 0
    if is_bigger_than_two:
        for i in range(1, length_of_matrix_minus_one):
            temp_tans_tuple = []
            for j in range(0, 3):
                #tn-1 = 1-tension * pk * .5
                temp_tans_tuple.append((1-tension_input)*0.5*(input_matrix[i+1][j]\
                    -input_matrix[i-1][j]))
            temp_tans.append(temp_tans_tuple)
    temp_tans_tuple = []
    #tn
    for j in range(0, 3):
        temp_tans_tuple.append((1-tension_input)*tanget_points[1][j])
    temp_tans.append(temp_tans_tuple)
    return temp_tans

def main(input_file, input_n_point, input_radius, input_tension):
    '''
    orcherstrates the whole thing
    '''
    input_du_point = 1/input_n_point
    input_matrix, tangent_matrix = get_matrix(input_file)
    full_matrix = copy.deepcopy(input_matrix)
    output_matrix = calculate_catmull_rom_splines(tangent_matrix, \
    input_matrix, input_tension, input_du_point)
    results_file = create_file(full_matrix, output_matrix, input_radius, input_n_point)
    print(results_file)

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

if __name__ == '__main__':
    '''
    parses arguements
    '''
    PARSER = argparse.ArgumentParser()
    ARG_GROUP = PARSER.add_argument_group()
    ARG_GROUP.add_argument('-f', '--file', help='The matrix with he input', type=str)
    ARG_GROUP.add_argument('-n', '--upoint', help='use the best', type=str)
    ARG_GROUP.add_argument('-r', '--radius', help='radius of the spheres', type=str)
    ARG_GROUP.add_argument('-t', '--tension', help='the tighness', type=str)
    ARGS = PARSER.parse_args()
    GIVEN_FILE = parse_input(ARGS.file, './cpts_in.txt')
    GIVEN_N = parse_input(ARGS.upoint, 11, True)
    GIVEN_RADIUS = parse_input(ARGS.radius, 0.1, True)
    GIVEN_TENSION = parse_input(ARGS.tension, 0, True)
    main(GIVEN_FILE, GIVEN_N, GIVEN_RADIUS, GIVEN_TENSION)
