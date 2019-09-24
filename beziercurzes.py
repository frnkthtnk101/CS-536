from math import *
from numpy import arange


def control_point_calculation(k, i):
    return factorial(k) / (factorial( i ) * factorial(k - i))

def u_calculation(k, i, u):
    reverse_u = 1 - u
    pow_by = k - i
    left = pow(reverse_u,pow_by)
    right = pow(u, i)
    return left * right

def main():
    input_matrix = [
        [0,0,0],
        [1.33333,0,1.33333],
        [3.66667, 0, 1.33333],
        [5,0,0]
    ]
    du = 0.025
    radius = 0.05
    results_matrix = []
    rows = len(input_matrix)
    columns = len(input_matrix[0])

    for i in arange(0.0,1.01,du): 
        temp_columns = [0.0] * columns
        for j in range(0,rows):
            for k in range(0,columns):
                cpc = control_point_calculation(rows,j)
                u_cal = u_calculation(rows,j,i)
                temp_columns[k] += float(input_matrix[j][k]) * float(cpc) * float(u_cal)
        results_matrix.append(temp_columns)
    for j in range(len(results_matrix) - 1,0,-1):
        print(results_matrix[j])   
            

    
main()