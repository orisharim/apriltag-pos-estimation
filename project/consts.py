import math
import numpy as np
import UtilFuncs as utils

HEIGHT = 800
WIDTH = 1280
FOV_X = math.radians(70)
FOV_Y = math.radians(37)
FOCAL_LENGTH_X = WIDTH / (2.0 * math.tan(FOV_X / 2.0))
FOCAL_LENGTH_Y = HEIGHT / (2.0 * math.tan(FOV_Y / 2.0))
FOCAL_LENGTH_X =  914.00853817
FOCAL_LENGTH_Y = 912.67983772
INTRINSIC_CAMERA_MATRIX = np.array([[914.00853817,0,694.05095984, 0],
 [  0,912.67983772 ,420.86995412, 0],
 [  0,           0,           1,        0]])

SIDE_LENGTH = 0.1651
FIELD_HEIGHT = 8.21055
FIELD_WIDTH = 16.54175

TAGS = {1: (593.68, 9.68, 53.38, 120, 0, 0), #x, z, y, yaw pitch roll
        2: (637.21, 34.79, 53.38, 120, 0, 0),
        3: (652.73, 196.17, 57.13, 180, 0, 0),
        4: (652.73, 218.42, 57.13, 180, 0 ,0),
        5: (578.77, 323.00, 53.38, 270, 0, 0),
        6: (72.5, 323.00, 53.38, 270, 0, 0),
        7: (-1.50, 218.42, 57.13, 0, 0, 0),
        8: (-1.50, 196.17, 57.13, 0, 0, 0),
        9: (14.02, 34.79, 53.38, 60, 0, 0),
        10: (57.54, 9.68, 53.38, 60, 0, 0),
        11: (468.69, 146.19, 52.00, 300, 0, 0),
        12: (468.69, 177.10, 52.00, 60, 0, 0),
        13: (441.74, 161.62, 52.00, 180, 0, 0),
        14: (209.48, 161.62, 52.00, 0, 0, 0),
        15: (182.73, 177.10, 52.00, 120, 0, 0),
        16: (182.73, 146.19, 52.00, 240, 0 ,0)
        }

APRIL_TAG_POINTS_MATRIX = np.array([[SIDE_LENGTH / 2, 0, 0, 0],
                              [0, SIDE_LENGTH / 2, 0, 0],
                              [0, 0, SIDE_LENGTH / 2, 0],
                              [1, 1, 1, 1]])

def get_inv_tag_matrix(tag_id):
        return np.linalg.inv(
                        np.array([[1, 0, 0, utils.inches_to_meter(TAGS[tag_id][0])],
                                  [0, 1, 0, utils.inches_to_meter(TAGS[tag_id][1])],
                                  [0, 0, 1, utils.inches_to_meter(TAGS[tag_id][2])],
                                  [0, 0, 0, 1]]) 
                        @ utils.get_affine_rotation_matrix(math.radians(TAGS[tag_id][3]),
                                                           math.radians(TAGS[tag_id][4]),
                                                           math.radians(TAGS[tag_id][5]))
                        @ APRIL_TAG_POINTS_MATRIX
        )


TAGS_INVERSE = {tag_id: get_inv_tag_matrix(tag_id) for tag_id in TAGS.keys()}



                
        
        

        