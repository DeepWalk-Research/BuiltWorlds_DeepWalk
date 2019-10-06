import cv2
import json
import numpy as np


def init_model():#TODO: actually initialize model
    pass

def steady_state(video_name):
    init_model()
    vidcap = cv2.VideoCapture(video_name)
    success,image = vidcap.read()
    curr_state = False
    scoops = 0
    state_buffer = []
    frame_list = []
    scoop_list = []
    len_buffer  = 10
    num_trans = 5
    i = 0
    while success:
        # Process image
        pred = eval(image)
        state = parse_json(pred, curr_state)
        state_buffer.append(state)
        if len(state_buffer) == len_buffer:
            curr_state, iterate = logic(curr_state,state_buffer,num_trans)
            state_buffer = []
            scoops += iterate
        frame_list.append(i)
        scoop_list.append(scoops)
        success,image = vidcap.read()
        i += 1
    return scoop_list

def eval(image): #TODO: Make this work
    return tfnet.return_predict(image)

def parse_json(predi, default):
    od,conv = obj_detected(pred) 
    if (od == "full"):
        return True
    elif od == "empty":
        return False
    return default

def logic(curr_state, state_buffer, num_trans):
    if curr_state == False:
        num_true = len(list(filter(lambda x: x == True, state_buffer)))
        if num_true >= num_trans:
            return True, 1
        return False, 0
    if curr_state == True:
       num_false =  len(list(filter(lambda x: x == False, state_buffer)))
       if num_false >= num_trans:
           return False, 0
    return True, 0

def obj_detected(yolo_dict):
    conv = 0
    od = ''
    for pred in yolo_dict:
        if od == '':
            od = pred['label']
            conv = pred['confidence']
            continue
        elif conv < pred['confidence']:
            conv = pred['confidence']
            od = pred['label']
    return od, conv
