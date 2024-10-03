import math
import numpy as np
from dt_apriltags import Detector
import cv2 as cv

HEIGHT = 800
WIDTH = 1280
FOV_X = math.radians(70)
FOV_Y = math.radians(37)
FOCAL_LENGTH_X = WIDTH / (2.0 * math.tan(FOV_X / 2.0))
FOCAL_LENGTH_Y = HEIGHT / (2.0 * math.tan(FOV_Y / 2.0))
INTRINSIC_CAMERA_MATRIX = np.array([
    [FOCAL_LENGTH_X, 0, WIDTH / 2.0, 0],
    [0, FOCAL_LENGTH_Y, HEIGHT / 2.0, 0],
    [0, 0, 1, 0]
])


# Function to draw bounding boxes and tag IDs on the image
def draw_tags(image, detections):
    for tag in detections:
        # Get the bounding box coordinates
        (ptA, ptB, ptC, ptD) = tag.corners
        ptA = tuple(map(int, ptA))
        ptB = tuple(map(int, ptB))
        ptC = tuple(map(int, ptC))
        ptD = tuple(map(int, ptD))

        # Draw the bounding box
        cv.polylines(image, [np.array([ptA, ptB, ptC, ptD], dtype=np.int32)], isClosed=True, color=(0, 255, 0),
                      thickness=2)

        # Draw the tag ID
        tag_id = tag.tag_id
        cv.putText(image, f"ID: {tag_id}", ptA, cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


def main():
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M','J', 'P', 'G'))
    cap.set(cv.CAP_PROP_FRAME_WIDTH,1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv.CAP_PROP_FPS, 120)
    cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 3)
    cap.set(cv.CAP_PROP_EXPOSURE, 100)


    detector = Detector(searchpath=['apriltags'],
                        families='tag36h11',
                        nthreads=1,
                        quad_decimate=1.0,
                        quad_sigma=0.0,
                        refine_edges=1,
                        decode_sharpening=0.25,
                        debug=0)

    while True:
        ret, frame = cap.read()
        
        if not ret:
            print('couldn\'t get camera input')
            continue

        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        tags = detector.detect(frame,
                           estimate_tag_pose=True,
                           camera_params=[FOCAL_LENGTH_X, FOCAL_LENGTH_Y, WIDTH/2.0, HEIGHT/2.0],
                           tag_size=0.165)

        draw_tags(frame, tags)
        cv.imshow('frame', frame)
        if len(tags) != 0:
            print(tags[0].pose_t)

        # Press 'q' to exit the loop
        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()