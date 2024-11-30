import math
import numpy as np
from dt_apriltags import Detection
from dt_apriltags import Detector
import cv2 as cv
import parameters
import utils as utils
import field_displayer

robot_pos = [0, 0, 0]
robot_rot = [0, 0, 0]

# Draw bounding boxes and tag IDs on the image
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
                      thickness=3)

        # Draw the tag ID
        tag_id = tag.tag_id
        cv.putText(image, f"ID: {tag_id}", ptA, cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


    

# Calculate robot position and rotation based on a single april tag detection
def estimate_robot_state(tag: Detection):
    tag_id = tag.tag_id
        
    #calculate tag center point translation camera oriented
    tag_translation = utils.matrix_3x3_to_affine_matrix(tag.pose_R)
    tag_translation[0][3] = tag.pose_t[2][0]
    tag_translation[1][3] = tag.pose_t[1][0] 
    tag_translation[2][3] = tag.pose_t[0][0]
    
    #calcuate a matrix that represents the translation of 4 points on the tag
    tag_points_translation = tag_translation @ parameters.TRANSFORMATION_TO_POINTS_ON_TAG_MATRIX
    
    extrinsic_matrix = tag_points_translation @ parameters.TAGS_INVERSE[tag_id]
    #stolen functions from nadav. edit code later
    pos_estimation = utils.extrinsic_matrix_to_camera_position(extrinsic_matrix)
    rot_estimation = utils.extrinsic_matrix_to_rotation(extrinsic_matrix)
    return (pos_estimation, rot_estimation)

def main():
    global robot_pos, robot_rot
    
    #setup camera
    cap = cv.VideoCapture(2)
    cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M','J', 'P', 'G'))
    cap.set(cv.CAP_PROP_FRAME_WIDTH,1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv.CAP_PROP_FPS, 120)
    cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 3)
    cap.set(cv.CAP_PROP_EXPOSURE, 100)
    
    #setup april tag detector
    detector = Detector(searchpath=['apriltags'],
                        families='tag36h11',
                        nthreads=1,
                        quad_decimate=1.0,
                        quad_sigma=0.0,
                        refine_edges=1,
                        decode_sharpening=0.25,
                        debug=0)
    
    field_displayer.start()
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print('couldn\'t get camera input')
            continue

        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        tags = detector.detect(frame,
                           estimate_tag_pose=True,
                           camera_params=[parameters.FOCAL_LENGTH_X, parameters.FOCAL_LENGTH_Y, parameters.SCREEN_WIDTH/2.0, parameters.SCREEN_HEIGHT/2.0],
                           tag_size=parameters.SIDE_LENGTH)
        
        draw_tags(frame, tags)
        cv.imshow('frame', frame)
        if len(tags) != 0:
            # print(tags[0].pose_t)
            pos_estimation, rot_estimation = estimate_robot_state(tags[0])
            print(f'pos: {pos_estimation} \n rot:{rot_estimation}\n')
            robot_pos = pos_estimation
            robot_rot = rot_estimation
            field_displayer.update_state(robot_pos, robot_rot)

            
        cv.waitKey(1)

    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()


def estimate_robot_pos():
    print('a')
