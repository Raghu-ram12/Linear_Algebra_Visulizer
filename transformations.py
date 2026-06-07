from vector_math import *
from matrix_math import *
import math

def rotate_vector(v: Vector,angle: float)->Vector:

    c=math.cos(math.radians(angle))
    s=math.sin(math.radians(angle))
    rotation_matrix=Matrix([[c,-s],[s,c]])
    return multiply_matrix_vector(v,rotation_matrix)

def scale_vector(v: Vector,sx:float,sy:float)->Vector:

    scale_matrix=Matrix([sx,0],[0,sy])

    return multiply_matrix_vector(v,scale_matrix) 


def sear_vector_x(v:Vector,k: float)->Vector:
    # increment x by ky ie y=y+kx
    shear_matrix=Matrix([1,k],[0,1])

    return multiply_matrix_vector(v,shear_matrix) 

def shear_vector_y(v:Vector,k:float)->Vector:
    # increment y  by kx ie x=x+ky
    shear_matrix=Matrix([1,0],[k,0]) 
    return multiply_matrix_vector(v,shear_matrix)

def reflect_on_x_axis(v:Vector)->Vector:
    pass 
def reflect_on_y_axis(v:Vector,):
    pass