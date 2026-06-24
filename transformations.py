from vector_math import *
from matrix_math import *
import math

def rotate_vector_about_axis(v: Vector, angle: float,axis : str ) -> Vector:

    c = math.cos(math.radians(angle))
    s = math.sin(math.radians(angle))

    r_x=Matrix([[1,0,0],[0,c,-s],[0,s,c]])
    r_y=Matrix([[c,0,s],[0,1,0],[-s,0,c]])
    r_z=Matrix([[c,-s,0],[s,c,0],[0,0,1]])
    
    axis=axis.lower()
    
    if axis =="x":
        
        return multiply_matrix_vector(v,r_x)

    elif axis=="y":
        return multiply_matrix_vector(v,r_y)

    elif axis=="z":

        return multiply_matrix_vector(v,r_z)
    else:
        raise ValueError("Invalid axis")

def rotate_vector_euler(v: Vector, gamma: float, beta: float, alpha: float) -> Vector:

    sg, cg = math.sin(math.radians(gamma)), math.cos(math.radians(gamma))
    sb, cb = math.sin(math.radians(beta)),  math.cos(math.radians(beta))
    sa, ca = math.sin(math.radians(alpha)), math.cos(math.radians(alpha))

    r_x = Matrix([[1,   0,   0],
                  [0,  cg, -sg],
                  [0,  sg,  cg]])

    r_y = Matrix([[ cb,  0,  sb],
                  [  0,  1,   0],
                  [-sb,  0,  cb]])

    r_z = Matrix([[ca, -sa,  0],
                  [sa,  ca,  0],
                  [ 0,   0,  1]])

    rotation_matrix = matrix_mul(matrix_mul(r_z, r_y), r_x)  # ZYX order

    return multiply_matrix_vector(v, rotation_matrix)

    

def scale_vector(v: Vector, sx: float, sy: float,sz:float) -> Vector:

    scale_matrix = Matrix([[sx, 0,0], [0, sy,0],[0,0,sz]])

    return multiply_matrix_vector(v, scale_matrix)



def reflect_on_planes(v:Vector,plane : str)->Vector:

    
    if plane == 'xy':

        r_xy=Matrix([[1,0,0],[0,1,0],[0,0,-1]])

        return multiply_matrix_vector(v,r_xy)
    
    elif plane == "yz":

        r_yz=Matrix([[-1,0,0],[0,1,0],[0,0,1]])

        return multiply_matrix_vector(v,r_yz)
    
    elif plane =="xz":

        r_xz=Matrix([[1,0,0],[0,-1,0],[0,0,1]]) 

        return multiply_matrix_vector(v,r_xz)
    else:
        
        print("Invalid plane")
        return 

    