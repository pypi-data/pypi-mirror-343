import numpy as np 
import math 

# Define rotation matrices for each axis
def rot_x(angle):
    angle = math.radians(angle)
    return np.array([[1, 0, 0, 0],
                     [0, math.cos(angle), -math.sin(angle), 0],
                     [0, math.sin(angle), math.cos(angle), 0],
                     [0, 0, 0, 1]])#.type(np.float64)

def rot_y(angle):
    angle = math.radians(angle)
    return np.array([[math.cos(angle), 0, math.sin(angle), 0],
                     [0, 1, 0, 0],
                     [-math.sin(angle), 0, math.cos(angle), 0],
                     [0, 0, 0, 1]])#.astype(np.float64)

def rot_z(angle):
    angle = math.radians(angle)
    return np.array([[math.cos(angle), -math.sin(angle), 0, 0],
                    [math.sin(angle), math.cos(angle), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])#.astype(np.float64)

