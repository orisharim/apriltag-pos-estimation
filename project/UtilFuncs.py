import numpy as np
import consts
import math

def inches_to_meter(inches):
    return inches * 0.0254

def matrix_3x3_to_affine_matrix(matrix):
    return np.array([
        [matrix[0][0], matrix[0][1], matrix[0][2], 0],
        [matrix[1][0], matrix[1][1], matrix[1][2], 0],
        [matrix[2][0], matrix[2][1], matrix[2][2], 0],
        [0, 0, 0, 1]
    ])

def get_affine_rotation_matrix(yaw=0.0, pitch=0.0, roll=0.0) -> np.ndarray:
    c1 = np.cos(pitch)
    s1 = np.sin(pitch)
    c2 = np.cos(yaw)
    s2 = np.sin(yaw)
    c3 = np.cos(roll)
    s3 = np.sin(roll)
    return np.array([[c2 * c3, -c2 * s3, s2, 0],
                     [c1 * s3 + c3 * s1 * s2, c1 * c3 - s1 * s2 * s3, -c2 * s1, 0],
                     [s1 * s3 - c1 * c3 * s2, c3 * s1 + c1 * s2 * s3, c1 * c2, 0],
                     [0, 0, 0, 1]])
    
#stolen functions from nadav. edit code later
def extrinsic_matrix_to_camera_position(extrinsic_matrix: np.ndarray) -> np.ndarray:
    """
    :param extrinsic_matrix: 4*4 extrinsic camera matrix
    :return: 3d vector representing the cameras position in global coordinates
    """
    rotation_matrix = np.delete(np.delete(extrinsic_matrix, 3, 0), 3, 1)
    inverse_rotation = np.linalg.inv(rotation_matrix)
    return -(inverse_rotation @ extrinsic_matrix[:3, 3])


def extrinsic_matrix_to_rotation(extrinsic_matrix: np.ndarray) -> list[float]:
    """
    :param extrinsic_matrix: 4*4 extrinsic camera matrix
    :return: the rotation around each axis
    """
    z = np.array([0, 0, 1])
    rotation_matrix = np.delete(np.delete(extrinsic_matrix, 3, 0), 3, 1)
    r_z = rotation_matrix @ z
    yaw = np.arccos(np.dot(np.array([z[0], z[2]]), np.array([r_z[0], r_z[2]]))) * np.sign(r_z[0])

    pitch = math.atan2(-extrinsic_matrix[2, 0],
                   (int(np.sign(extrinsic_matrix[1, 0])) | int(np.sign(extrinsic_matrix[0, 0])))
                       * math.sqrt(extrinsic_matrix[1, 0]**2 + extrinsic_matrix[0, 0]**2))
    # yaw = math.atan2(extrinsic_matrix[2, 1], extrinsic_matrix[2, 2])
    roll = math.atan2(extrinsic_matrix[1, 0], extrinsic_matrix[0, 0])

    return [math.degrees(yaw), math.degrees(pitch), math.degrees(roll)]
    # return [yaw, pitch, roll]

