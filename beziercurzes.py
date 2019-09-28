import argparse
from math import factorial
from numpy import arange


def control_point_calculation(Length, index):
    return factorial(Length) / (factorial( index ) * factorial(Length - index))

def u_calculation(length, index, u_point):
    reverse_u = 1 - u_point
    pow_by = length - index
    left = pow(reverse_u,pow_by)
    right = pow(u_point, index)
    return left * right

def main(input_matrix, du, printtoscreen, radius = 0.1, ):
    results_matrix = []
    rows_length = len(input_matrix) - 1
    columns = len(input_matrix[0])

    for u_point in arange(0.0,1.01,du): 
        temp_columns = [0.0] * columns
        for index_row in range(0,rows_length + 1):
            for columns_index in range(0,columns):
                cpc = control_point_calculation(rows_length,index_row )
                u_cal = u_calculation(rows_length,index_row,u_point)
                temp_columns[columns_index] += \
                    input_matrix[index_row][columns_index] * cpc * u_cal
        results_matrix.append(temp_columns)

    for j in range(len(results_matrix)):
        print('{:5f} {:5f} {:5f},'.format(results_matrix[j][0],results_matrix[j][1],results_matrix[j][2]))
            

def get_matrix(file_path):
    return []

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    group = PARSER.add_argument_group()
    group.add_argument( '-f', '--file', help = 'The matrix with he input', type = str)
    group.add_argument( '-u', '--upoint', help = 'use the best', type = str)
    group.add_argument( '-r', '--radius', help = 'radius of the spheres', type = str)
    group.add_argument( '-p', '--printtoscreen', action='store_true', help = 'use the bigram')
    ARGS = PARSER.parse_args()
    matrix = get_matrix( ARGS.file)
    try:
        du = float( ARGS.upoint)
        du_is_between_zero_and_one = 0 <= du <= 1
    except:
        Exception("du is not a float")
    if du_is_between_zero_and_one:
        main( matrix, du, ARGS.printtoscreen, ARGS.radius)
    else:
        print("du is not between/or 0 and 1")