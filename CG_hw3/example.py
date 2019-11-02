#!/usr/bin/python
# /*  Name:    Merlin Cherian
#  *  Class:   CS 536 (Computer Graphics)
#  *
#  *
#  */
import numpy as np
import argparse
from decimal import *
coordinate3 = []
indexFaceSet = []
positions = []
normalVectors = []


def blending_fun(u):
    arr = np.array([pow(1-u, 3), 3*u*pow(1-u, 2), 3*pow(u, 2)*(1-u), pow(u, 3)])
    return arr


def compute_points(f):
    input = open(f)
    x, y, z = list(), list(), list(),
    for l in input:
        row = l.split(" ")
        x.append(row[0])
        y.append(row[1])
        z.append(row[2].strip('\n'))
    Bx = np.array(x, dtype=np.float64).reshape(4,4)
    By = np.array(y, dtype=np.float64).reshape(4,4)
    Bz = np.array(z, dtype=np.float64).reshape(4,4)
    global positions
    positions = np.loadtxt(f)

    # GENERATE MESH
    x_coords = gen_coord_points(Bx)
    y_coords = gen_coord_points(By)
    z_coords = gen_coord_points(Bz)

    verts = np.array(list(zip(x_coords, y_coords, z_coords)))
    vertices = []
    for k in range(len(verts)):
        points = []
        for j in verts:
            column = []
            for i in j:
                column.append(i)
            points.append(column)
        vertices.append(points)

    global coordinate3
    coordinate3 = vertices

    # GENERATE TRIANGLE COORDINATES
    triangle_coordinates = gen_triangle_set(vertices)
    global indexFaceSet
    indexFaceSet = triangle_coordinates

    # GENERATE NORMALS
    normals = []
    du_list = gen_values(u)
    dv_list = gen_values(v)
    for a in range(len(du_list)):
        for b in range(len(dv_list)):
            s_vec = gen_s_tan_vector(Bx, By, Bz, du_list[a], dv_list[b])
            t_vec = gen_t_tan_vector(Bx, By, Bz, du_list[a], dv_list[b])
            normals.append(gen_normals(s_vec, t_vec).tolist())
    global normalVectors
    normalVectors = np.around(normals, 6)


def gen_t_tan_vector(Gx, Gy, Gz, u, v):
    U = np.array([pow(u, 3), pow(u, 2), u, 1])
    Vt = np.array([3 * pow(v, 2), 2 * v, 1, 0])
    M = np.array(([-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]))
    t_tan_vector = np.array([U.dot(M).dot(Gx).dot(np.transpose(Vt.dot(M))), U.dot(M).dot(Gy).dot(np.transpose(Vt.dot(M))), U.dot(M).dot(Gz).dot(np.transpose(Vt.dot(M)))])
    return t_tan_vector


def gen_s_tan_vector(Gx, Gy, Gz, u, v):
    V = np.array([pow(v, 3), pow(v, 2), v, 1])
    Ut = np.array([3 * pow(u, 2), 2 * u, 1, 0])
    M = np.array(([-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]))
    s_tan_vector = np.array([Ut.dot(M).dot(Gx).dot(np.transpose(V.dot(M))), Ut.dot(M).dot(Gy).dot(np.transpose(V.dot(M))), Ut.dot(M).dot(Gz).dot(np.transpose(V.dot(M)))])
    return s_tan_vector


def gen_normals(s, t):
    s = np.array(s)
    t = np.array(t)
    return np.cross(s, t)


def gen_coord_points(points):
    du_list = gen_values(u)
    dv_list = gen_values(v)
    vals = []
    for a in range(len(du_list)):
        for b in range(len(dv_list)):
            bu = blending_fun(du_list[a])
            bv = blending_fun(dv_list[b])
            temp = []
            for i in range(0, 4):
                for j in range(0, 4):
                    val = bu[i] * bv[j] * points[i][j]
                    temp.append(val)

            vals.append(sum(temp))
    return vals


def gen_triangle_set(vertices): 
    triangle_coords = []
    for j in range(0, int(num_u) - 1):  
        for i in range(0, int(num_v) - 1):
            tri0 = list((fire(i, j, vertices), fire(i, j+1, vertices), fire(i + 1, j+1, vertices), -1))
            tri1 = list((fire(i, j, vertices), fire(i+1, j + 1, vertices), fire(i+1, j, vertices), -1))
            triangle_coords.append(tri0)
            triangle_coords.append(tri1)
    return triangle_coords


def fire(x, y, grid):
    cheese = (num_v*y)+x
    return cheese


def gen_values(val):
    values = np.arange(0.0, 1.01, val)
    return values


#WITH NORMALS
def smooth_shaded():
    print("#Inventor V2.0 ascii"
          "\n"
          "\n"
          "ShapeHints {"
          "\n"
          "vertexOrdering        COUNTERCLOCKWISE"
          "\n"
          "}\n\n"
          "Separator {\n"
          "Coordinate3 { 	"
          "\npoint [ ")

    for i in range(len(coordinate3)):
        print (' '.join(map(repr, coordinate3[0][i])) + ",")

    print("]\n"
          "} \nNormalBinding {\n"
          "value        PER_VERTEX_INDEXED\n"
          "}\n"
          "Normal {\n"
          "     vector [")

    for i in range(len(normalVectors)):
        print( str(normalVectors[i][0]) + " " + str(normalVectors[i][1]) + " " + str(normalVectors[i][2]) + ",")

    print("]\n"
          "} \nIndexedFaceSet {\n"
          "coordIndex [")

    for i in range(len(indexFaceSet)):
        print (', '.join(map(repr, indexFaceSet[i])) + ",")

    print(
        "]\n}\n}\nSeparator {\nLightModel {\n"
        "model PHONG\n"
        "}\n"
        "Material {	\n      diffuseColor 1.0 1.0 1.0}\nTransform {\n        translation\n")

    for i in range(0, len(positions)):
        print(' '.join(map(repr, positions[i])))
        if i != len(positions) - 1:
            print("\n"
                  "}Sphere {	radius " + radius + " }}\nSeparator {LightModel {model PHONG}Material {	diffuseColor 1.0 1.0 1.0}\nTransform {translation\n")
        else:
            print("\n"
                  "}Sphere {	radius " + radius + " }}")


#NO NORMALS
def flat_shaded():
    print("#Inventor V2.0 ascii"
          "\n"
          "\n"
          "ShapeHints {"
          "\n"
          "vertexOrdering        COUNTERCLOCKWISE"
          "\n"
          "}\n\n"
          "Separator {\n"
          "Coordinate3 { 	"
          "\npoint [ ")

    for i in range(len(coordinate3)):
        print (' '.join(map(repr, coordinate3[0][i])) + ",")

    print("]\n"
          "} \nIndexedFaceSet {\n"
          "coordIndex [")
    for i in range(len(indexFaceSet)):
        print (' '.join(map(repr, indexFaceSet[i])) + ",")

    print(
        "]\n}\n}\nSeparator {\nLightModel {\n"
        "model PHONG\n"
        "}\n"
        "Material {	\n      diffuseColor 1.0 1.0 1.0}\nTransform {\n        translation\n")

    for i in range(0, len(positions)):
        print(' '.join(map(repr, positions[i])))
        if i != len(positions) - 1:
            print("\n"
                  "}Sphere {	radius " + radius + " }}\nSeparator {LightModel {model PHONG}Material {	diffuseColor 1.0 1.0 1.0}\nTransform {translation\n")
        else:
            print("\n"
                  "}Sphere {	radius " + radius + " }}")


def main():
    global num_u
    num_u = 11
    global num_v
    num_v = 11
    global radius
    radius = str(0.1)
    THREEPLACES = Decimal(10) ** -3
    global u, v
    u = float(Decimal(1.0/(num_u-1.0)).quantize(THREEPLACES))
    v = float(Decimal(1.0/(num_v-1.0)).quantize(THREEPLACES))
    compute_points('patchPoints.txt')
    '''
    flat_shaded()
    smooth_shaded()
    '''


if __name__ == '__main__':
    main()

