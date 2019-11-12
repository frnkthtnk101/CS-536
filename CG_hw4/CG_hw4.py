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
    def __init__(self,
    a_scalar_input, b_scalar_input, c_scalar_input,r_input, t_input, u_input, v_input, face_input):
        self.a_scalar = a_scalar_input
        self.b_scalar = b_scalar_input
        self.c_scalar = c_scalar_input
        self.r_s1 = r_input
        self.t_s2 = t_input
        self.u_point = u_input
        self.v_point = v_input
        self.face_type = face_input
        self.u_points = np.array(0,1.01, 1 / u_input)
        self.v_points = np.array(0,1.01, 1 / v_input)
        self.u_points_len = len(self.u_points)
        self.v_points_len = len(self.v_points)

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

def sgn(angle):
    if(angle == 0): return 0
    if(angle > 0): return 1
    if(angle < 0): return -1

auxiliary_function_c = lambda w, m : sgn(np.cos(w)) * np.power(np.absolute(np.cos(w)),m)
auxiliary_function_s = lambda w, m : sgn(np.sin(w)) * np.power(np.absolute(np.sin(w)),m)
x_function = lambda u, v, r, t, a : a * auxiliary_function_c(v, r) * auxiliary_function_c(u, t)
y_function = lambda u, v, r, t, b : b * auxiliary_function_c(v,r) * auxiliary_function_s(u, t)
z_function = lambda v, r, c: c * auxiliary_function_s(v,r)

def main(given_args_params):
    points = []
    normalized_points = []
    #gen points
    for u_point in given_args_params.u_points:
        for v_point in given_args_params.v_points:
            points.append(
                [
                x_function(u_point, v_point, given_args_params.r_s1, given_args_params.t_s2, given_args_params.a_scalar),
                y_function(u_point, v_point, given_args_params.r_s1, given_args_params.t_s2, given_args_params.b_scalar),
                z_function( v_point, given_args_params.r_s1, given_args_params.c_scalar),
                ]
            )
            normalized_points.append(
                [
                x_function(u_point, v_point, 2 - given_args_params.r_s1, 2 - given_args_params.t_s2, 1 / given_args_params.a_scalar),
                y_function(u_point, v_point, 2 - given_args_params.r_s1, 2 - given_args_params.t_s2, 1 / given_args_params.b_scalar),
                z_function( v_point, 2 - given_args_params.r_s1, 1 / given_args_params.c_scalar),
                ]
            )


    

if __name__ == '__main__':
    '''
    parses arguements
    '''
    PARSER = argparse.ArgumentParser()
    ARG_GROUP = PARSER.add_argument_group()
    ARG_GROUP.add_argument('-u', '--u_iteration', help='How many times to iterate over the first Bernstein polynomial', type=str)
    ARG_GROUP.add_argument('-v', '--v_iteration', help='How many times to iterate over the second Bernstein polynomial', type=str)
    ARG_GROUP.add_argument('-A', '--a_scalar', type=str)
    ARG_GROUP.add_argument('-B', '--b_scalar', type=str)
    ARG_GROUP.add_argument('-C', '--c_scalar', type=str)
    ARG_GROUP.add_argument('-r', '--s1', type=str)
    ARG_GROUP.add_argument('-t', '--s2', type=str)
    ARG_GROUP.add_argument('-F', '--flat', action = 'store_true')
    ARG_GROUP.add_argument('-S', '--smooth', action = 'store_true')
    ARGS = PARSER.parse_args()
    use_smoothing = ARGS.flat is False
    if(use_smoothing) :
        face = surface_options.smooth
    else:
        face = surface_options.flat
    inputs = given_args(
        a_scalar_input = parse_input(ARGS.a_scalar, 1, True),
        b_scalar_input = parse_input(ARGS.b_scalar, 1, True),
        c_scalar_input = parse_input(ARGS.c_scalar, 1, True),
        r_input = parse_input(ARGS.s1, 1, True),
        t_input = parse_input(ARGS.s2, 1, True),
        u_input = parse_input(ARGS.u_iteration, 19, True),
        v_input = parse_input(ARGS.v_iteration, 19, True),
        face_input = face
    )
    main(inputs)