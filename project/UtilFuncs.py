import numpy as np

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