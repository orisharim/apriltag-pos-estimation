
import math
import numpy as np
from dt_apriltags import Detection
from dt_apriltags import Detector
import cv2 as cv
import parameters
import utils as utils
import copy
import threading 

field_img = cv.imread('SampleImages2024/field.png')
meters_to_pixels_x = (parameters.SCREEN_WIDTH) / (parameters.FIELD_WIDTH)
meters_to_pixels_y = (parameters.SCREEN_HEIGHT) / (parameters.FIELD_HEIGHT) 

    
def start():
    global field_img, meters_to_pixels_x, meters_to_pixels_y
    field_img = cv.resize(field_img, (parameters.SCREEN_WIDTH, parameters.SCREEN_HEIGHT))
    field_img = cv.flip(field_img, 0)
    # __draw_tags_on_field(field_img)
    update_state([0,0,0], [0,0,0])
    
def update_state(pos, rot):
    global field_img, meters_to_pixels_x, meters_to_pixels_y
    current_img = copy.deepcopy(field_img)
    current_img = __draw_robot(current_img, pos[0], pos[1], rot[0])
    cv.imshow('field', current_img)
    
    
def __draw_robot(screen, point_x, point_y, yaw):
    center = __pos_to_pixels(point_x, point_y)
    
    p1 =  __pos_to_pixels(-0.5 * parameters.ROBOT_CHASSIS_HEIGHT + point_x,
                          -0.5 * parameters.ROBOT_CHASSIS_WIDTH + point_y)
    
    p2 = __pos_to_pixels(-0.5 *  parameters.ROBOT_CHASSIS_HEIGHT + point_x,
                         0.5  *  parameters.ROBOT_CHASSIS_WIDTH + point_y)
    
    p3 = __pos_to_pixels(0.5  *  parameters.ROBOT_CHASSIS_HEIGHT + point_x,
                         0.5  *  parameters.ROBOT_CHASSIS_WIDTH + point_y)
    
    p4 = __pos_to_pixels(0.5  *  parameters.ROBOT_CHASSIS_HEIGHT + point_x,
                         -0.5 *  parameters.ROBOT_CHASSIS_WIDTH + point_y)
    
    rotation_matrix = cv.getRotationMatrix2D((center[0], center[1]), yaw, 1)
    p1 = rotation_matrix @ p1
    p2 = rotation_matrix @ p2
    p3 = rotation_matrix @ p3
    p4 = rotation_matrix @ p4
    
    #turn from affine 2d vectors to normal 2d vectors
    p1 = (int(p1[0]), int(p1[1]))
    p2 = (int(p2[0]), int(p2[1]))
    p3 = (int(p3[0]), int(p3[1]))
    p4 = (int(p4[0]), int(p4[1]))
    
    screen =  cv.line(screen, p1, p2, (0,0,255), 3)
    screen =  cv.line(screen, p2, p3, (0,0,255), 3)
    screen =  cv.line(screen, p3, p4, (0,255,255), 3)
    screen =  cv.line(screen, p4, p1, (0,0,255), 3)
    return screen
    
def __pos_to_pixels(point_x, point_y):
    global meters_to_pixels_x, meters_to_pixels_y
    return ((point_x * meters_to_pixels_x),
            ((parameters.FIELD_HEIGHT - point_y) * meters_to_pixels_y),
            1)       
     
def __draw_tags_on_field(field_img):
    for i in parameters.TAGS.keys():
         __draw_robot(field_img, utils.inches_to_meter(parameters.TAGS[i][0]), utils.inches_to_meter(parameters.TAGS[i][1]), parameters.TAGS[i][3])
    return field_img
    
            