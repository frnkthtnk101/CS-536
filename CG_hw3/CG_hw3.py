import argparse
import copy #to get a copy of the orginal inputs
from math import factorial
import numpy as np
from enum import Enum

class surface_options(Enum):
    flat = 1
    smooth = 2

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

blend = lambda x: [pow(1-x, 3), 3*x*pow(1-x, 2), 3*pow(x, 2)*(1-x), pow(x, 3)]

def blend_for_columns(columns, u_point, v_point):
    temp_list = []
    i, j = 0, 0
    u_points = np.arange(0, 1/u_point, 1.01)
    v_points = np.arange(0, 1/v_point, 1.01)
    index_under_limit = lambda x,y : x < y
    while(index_under_limit(i,u_point)):
        while(index_under_limit(j,v_point)):
            blended_u = blend(u_points)
            blended_v = blend(v_points)
            vert_point = 0
            for k in range(0,4):
                vert_point += blended_u * blended_v * columns[k][0]
                vert_point += blended_u * blended_v * columns[k][1]
                vert_point += blended_u * blended_v * columns[k][2]
                vert_point += blended_u * blended_v * columns[k][3]
            temp_list.append(vert_point)
            j+= 1
        i += 1
    return temp_list

def define_triangles(blended_matrix, u_point, v_point):
    the_triangles = []
    for i in len(np.arange(0,1/u_point,1.01) - 2):
        for j in len(np.arange(0,1/v_point,1.01) - 2):
            triangle_1 = list(
                blended_matrix[i][j],
                blended_matrix[i+1][j],
                blended_matrix[i+1][j+1],
            )
            triangle_2 = list(
                blended_matrix[i][j],
                blended_matrix[i+1][j+1],
                blended_matrix[i][j+1]
            )
            the_triangles.append(triangle_1)
            the_triangles.append(triangle_2)
    return the_triangles

def normalize_for_shading(colum_x, column_y, column_z, u_point, v_point):
    #https://www.guru99.com/numpy-dot-product.html
    #https://stackoverflow.com/questions/1984799/cross-product-of-two-vectors-in-python#1984817
    tangents_from_points = []
    column_x_as_numpy_array = np.array(colum_x)
    column_y_as_nump_array = np.array(column_y)
    column_z_as_nump_array = np.array(column_z)
    i, j = 0, 0
    u_points = np.arange(0, 1/u_point, 1.01)
    v_points = np.arange(0, 1/v_point, 1.01)
    index_under_limit = lambda x,y : x < y
    while index_under_limit(i,u_point):
        while index_under_limit(j,v_point):
            s_vector = get_tangent(column_x_as_numpy_array,column_y_as_nump_array, column_z_as_nump_array, u_points[i], v_points[j])
            t_vector = get_tangent(column_x_as_numpy_array,column_y_as_nump_array, column_z_as_nump_array, u_points[i], v_points[j])
            tangents_from_points.append(np.cross(s_vector, t_vector).tolist())
            j += 1
        i += 1
    return tangents_from_points

def get_tangent(column_x, column_y, column_z, u_point, v_point):
    t_part = np.array([3 * pow(u_point, 2),2 * u_point, 1, 0])
    s_part = np.array([pow(v_point, 3), pow(v_point, 2), v_point, 1])
    m_part = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]])
    return np.array([t_part.dot(m_part).dot(column_x).dot(np.transpose(s_part.dot(m_part))), t_part.dot(m_part).dot(column_y).dot(np.transpose(s_part.dot(m_part))), t_part.dot(m_part).dot(column_z).dot(np.transpose(s_part.dot(m_part)))])



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

def list_to_string(input_list, suffix = ''):
    string_builder = ''
    for element in input_list:
        string_builder += ",".join(element) + "," + suffix + "\r\n"
    return string_builder

#GIVEN_FILE, GIVEN_U, GIVEN_V, GIVEN_RADIUS, surface_options.flat
def main(file_path, u_point, v_point, radius, surface_option):
    raw_matrix = get_matrix(file_path)
    #cut them up in columns so its easier to work with
    column_x, column_y, column_z = split_up(raw_matrix)

    #put them back together
    #https://www.geeksforgeeks.org/zip-in-python/
    blended_matrix = list( 
        zip(
            blend_for_columns(column_x, u_point, v_point),
            blend_for_columns(column_y, u_point, v_point),
            blend_for_columns(column_z, u_point, v_point)
        )
    )

    #time to do triangles
    triangle_cords = []
    for i in range(0,len(blended_matrix)):
        triangle_cords.append(define_triangles(blended_matrix, u_point, v_point))

    #time to do the shading
    is_flat_shaded = surface_options is surface_options.flat

    string_builder  = '#Inventor V2.0 ascii\r\nShapeHints\{vertixOrdering COUNTERCLOCKEWISE\}\r\n'
    string_builder += 'Separator {\r\n Coordinate3 {\r\npoint ['
    string_builder += list_to_string(blended_matrix)
    string_builder += ']\r\n}\r\n'
    if is_flat_shaded:
        string_builder += 'NormalBinding \{\r\nvalue PER_VERTEX_INDEXED\}\r\nNormal {\r\nvector['
        normalized_points = normalize_for_shading(column_x, column_y, column_z, u_point, v_point)
        string_builder += list_to_string(normalized_points)
        string_builder += ']\r\n}\r\n'
    #the triangles
    string_builder += 'IndexedFaceSet {coordIndex[\r\n'
    string_builder += list_to_string(triangle_cords,'-1,')
    string_builder += ']}}'
    string_builder += create_sphere(radius, raw_matrix, len(raw_matrix))     

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
    GIVEN_FILE = parse_input(ARGS.file, './patchPoints.txt')
    GIVEN_U = parse_input(ARGS.uIteration, 11, True)
    GIVEN_V = parse_input(ARGS.vIteration, 11, True)
    GIVEN_RADIUS = parse_input(ARGS.radius, 0.1, True)
    s_is_true = ARGS.smooth_shaded == True
    if(s_is_true):
        main(GIVEN_FILE, GIVEN_U, GIVEN_V, GIVEN_RADIUS, surface_options.smooth) 
    else:
        main(GIVEN_FILE, GIVEN_U, GIVEN_V, GIVEN_RADIUS, surface_options.flat)