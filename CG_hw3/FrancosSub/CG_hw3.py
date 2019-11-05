'''
CG_hw3.py
Franco Pettigrosso
My submission for Bi-cubic Bezier Patch
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
    '''
    we split up the columns so it is 
    easier to work with
    '''
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
    '''
    blending the columns
    '''
    columns = np.array(columns).reshape(4,4)
    temp_list = []
    i, j = 0, 0
    u_points = np.arange(0, 1.01 , 1/u_point)
    v_points = np.arange(0, 1.01, 1/v_point)
    index_under_limit = lambda x,y : x < y
    while(index_under_limit(i,u_point)):
        while(index_under_limit(j,v_point)):
            blended_u = np.array(blend(u_points[i]))
            blended_v = np.array(blend(v_points[j]))
            temp_verts = []
            for k in range(0,4):
                for l in range(0,4):
                    vert_point = blended_u[k] * blended_v[l] * columns[k][l]
                    temp_verts.append(vert_point)
            temp_list.append(sum(temp_verts))
            j+= 1
        j = 0
        i += 1
    return temp_list

def define_triangles(blended_matrix, u_point, v_point):
    '''
    defining the triangles
    '''
    the_triangles = []
    triangle_calculation = lambda x,y,z: x * y + z
    u_point_length = len(np.arange(0, 1.01 , 1/u_point)) - 2
    v_point_length = len(np.arange(0, 1.01 , 1/v_point)) - 2
    for i in range(0, u_point_length):
        for j in range(0, v_point_length):
            triangle_1 = [
                triangle_calculation(v_point,i,j),
                triangle_calculation(v_point,i,j + 1),
                triangle_calculation(v_point,i + 1, j + 1),
            ]
            triangle_2 = [
                triangle_calculation(v_point,i,j),
                triangle_calculation(v_point,i + 1,j + 1),
                triangle_calculation(v_point,i + 1,j),
            ]
            the_triangles.append(triangle_1)
            the_triangles.append(triangle_2)
    return the_triangles

def normalize_for_shading(colum_x, column_y, column_z, u_point, v_point):
    #https://www.guru99.com/numpy-dot-product.html
    #https://stackoverflow.com/questions/1984799/cross-product-of-two-vectors-in-python#1984817
    tangents_from_points = []
    column_x_as_numpy_array = np.array(colum_x).reshape(4,4)
    column_y_as_nump_array = np.array(column_y).reshape(4,4)
    column_z_as_nump_array = np.array(column_z).reshape(4,4)
    i, j = 0, 0
    u_points = np.arange(0, 1.01 , 1/u_point)
    v_points = np.arange(0, 1.01 , 1/u_point)
    index_under_limit = lambda x,y : x < y
    while index_under_limit(i,u_point):
        while index_under_limit(j,v_point):
            s_vector = get_tangent_s(column_x_as_numpy_array,column_y_as_nump_array, column_z_as_nump_array, u_points[i], v_points[j])
            t_vector = get_tangent_t(column_x_as_numpy_array,column_y_as_nump_array, column_z_as_nump_array, u_points[i], v_points[j])
            tangents_from_points.append(np.cross(s_vector, t_vector).tolist())
            j += 1
        j = 0
        i += 1
    return tangents_from_points

def get_tangent_s(column_x, column_y, column_z, u_point, v_point):
    V = np.array([pow(v_point, 3), pow(v_point, 2), v_point, 1])
    Ut = np.array([3 * pow(u_point, 2), 2 * u_point, 1, 0])
    M = np.array(([-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]))
    s_tan_vector = np.array([Ut.dot(M).dot(column_x).dot(np.transpose(V.dot(M))), Ut.dot(M).dot(column_y).dot(np.transpose(V.dot(M))), Ut.dot(M).dot(column_z).dot(np.transpose(V.dot(M)))])
    return s_tan_vector

def get_tangent_t(column_x, column_y, column_z, u_point, v_point):
    U = np.array([pow(u_point, 3), pow(u_point, 2), u_point, 1])
    Vt = np.array([3 * pow(v_point, 2), 2 * v_point, 1, 0])
    M = np.array(([-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]))
    t_tan_vector = np.array([U.dot(M).dot(column_x).dot(np.transpose(Vt.dot(M))), U.dot(M).dot(column_y).dot(np.transpose(Vt.dot(M))), U.dot(M).dot(column_z).dot(np.transpose(Vt.dot(M)))])
    return t_tan_vector

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

def list_to_string(input_list, suffix = ',', to_float = True):
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
    string_builder = ''
    for element in input_list:
        string_builder += '{0:.6f} {1:.6f} {2:.6f},\r\n'.format(
            element[0],
            element[1],
            element[2]
        )
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
    triangle_cords = define_triangles(blended_matrix, u_point, v_point)
    #time to do the shading
    is_smooth_shaded = surface_option is surface_options.smooth
    string_builder  = '#Inventor V2.0 ascii\r\nShapeHints {\r\n vertexOrdering COUNTERCLOCKWISE \r\n}\r\n'
    string_builder += 'Separator {\r\n Coordinate3 {\r\npoint [\r\n'
    string_builder += list_to_string(blended_matrix)
    string_builder += ']\r\n}\r\n'
    if is_smooth_shaded:
        string_builder += 'NormalBinding {\r\nvalue PER_VERTEX_INDEXED}\r\nNormal {\r\nvector [\r\n'
        normalized_points = normalize_for_shading(column_x, column_y, column_z, u_point, v_point)
        string_builder += list_to_string_normal(normalized_points)
        string_builder += ']\r\n}\r\n'
    #the triangles
    string_builder += 'IndexedFaceSet {\r\ncoordIndex[\r\n'
    string_builder += list_to_string(triangle_cords,'-1,', False)
    string_builder += ']\r\n}\r\n}'
    string_builder += create_sphere(radius, raw_matrix, len(raw_matrix) - 1) 
    print(string_builder)    

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
    ARG_GROUP.add_argument('-F', '--flat', action = 'store_true')
    ARG_GROUP.add_argument('-S', '--smooth', action = 'store_true')
    ARGS = PARSER.parse_args()
    GIVEN_FILE = parse_input(ARGS.file, './patchPoints.txt')
    GIVEN_U = parse_input(ARGS.uIteration, 11, True)
    GIVEN_V = parse_input(ARGS.vIteration, 11, True)
    GIVEN_RADIUS = parse_input(ARGS.radius, 0.1, True)
    use_smoothing = ARGS.flat is False
    if(use_smoothing) :
        main(GIVEN_FILE, GIVEN_U, GIVEN_V, GIVEN_RADIUS, surface_options.smooth) 
    else:
        main(GIVEN_FILE, GIVEN_U, GIVEN_V, GIVEN_RADIUS, surface_options.flat)