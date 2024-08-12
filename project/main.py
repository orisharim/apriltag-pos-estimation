import math
import numpy as np

HEIGHT = 0
WIDTH = 0
FOV_X = 0
FOV_Y = 0
FOCAL_LENGTH_X = WIDTH / (2.0 * math.tan(FOV_X / 2.0))
FOCAL_LENGTH_Y = HEIGHT / (2.0 * math.tan(FOV_Y / 2.0))
INTRINSIC_CAMERA_MATRIX = np.array([
    [FOCAL_LENGTH_X, 0, WIDTH / 2.0, 0],
    [0, FOCAL_LENGTH_Y, HEIGHT / 2.0, 0],
    [0, 0, 1, 0]
])

def main():
    print('hello')
if __name__ == '__main__':
    main()

