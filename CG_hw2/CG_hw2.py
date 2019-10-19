import argparse
from math import factorial
from numpy import arange

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
            #reqirement 1 3d point -v
            if line_only_contains_three_points:
                tangent_line_below_limit = 2 > tangent_line 
                if tangent_line_below_limit:
                    tangent_matrix.append(temp_matrix)
                    tangent_line+=1
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

def calculate_Catmull_Rom_Splines(tanget_points, input_matrix, T_input, du_point):
    tangents = create_tangent_points(tanget_points, input_matrix, T_input)
    out_matrix = create_output_matrix(tangents, input_matrix, du_point)
    return out_matrix
    
def create_output_matrix(tangents, input_matrix, du_point):
    def is_quequed(a_list):
        return len(a_list) > 1

    def set_points():
        temp_points = []
        temp_points.append(input_matrix[0])
        little_points = []
        for i in range(0,3):
            little_points.append(input_matrix[0][i] + (1/3) * tangents[0][i])
        temp_points.append(little_points)
        temp_points.append(input_matrix[1])
        little_points = []
        for i in range(0,3):
            little_points.append(input_matrix[1][i] + (1/3) * tangents[1][i])
        temp_points.append(little_points)
        return temp_points
    
    output = []
    while is_quequed(input_matrix):
        points = set_points()
        output.append(calculate_arb_bezier_curve(points,du_point))
        input_matrix.pop(0)
        tangents.pop(0)
    return output



def create_tangent_points(tanget_points, input_matrix, T_input):
    temp_tans = []
    temp_tans_tuple = []
    for j in range(0,3):
        temp_tans_tuple.append((1-T_input)*tanget_points[0][j])
    temp_tans.append(temp_tans_tuple)
    for i in range(1, len(input_matrix)-1):
        temp_tans_tuple = []
        for j in range(0,3):
            temp_tans_tuple.append((1-T_input)*0.5*(input_matrix[i+1][j]-input_matrix[i-1][j]))
        temp_tans.append(temp_tans_tuple)
    temp_tans_tuple = []
    for j in range(0,3):
        temp_tans_tuple.append((1-T_input)*tanget_points[1][j])
    temp_tans.append(temp_tans_tuple)
    return temp_tans


#n = 40 (du = 0.025), radius = 0.05, tension = 0
def main(input_file, input_n_point, input_radius, input_tension):
    input_du_point = 1/input_n_point
    input_matrix, tangent_matrix = get_matrix(input_file)
    output_matrix = calculate_Catmull_Rom_Splines(tangent_matrix, \
        input_matrix,input_tension,input_du_point)
    for i in output_matrix:
        for j in i:
            print('\t{:5f} {:5f} {:5f},'.format(j[0],j[1],j[2]))


main("/Users/francopettigrosso/ws/CS-536/CG_hw2/input.txt",20,.05,0)
