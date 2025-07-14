# Copyright 2019 The MediaPipe Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import mediapipe as mp
import numpy as np
import cv2 as cv

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def calc_angle(a: list, b: list, c: list) -> float:
    """Takes given points (arrays) from mediapipe pose solution
       and returns a relevant angle"""
    
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle


def pullup(image, landmarks, counter, phase) -> tuple[float, str]:
    """This function, if specified is called automaticaly by mp_stream function.\n 
    It tracks and returns count and phase for given exercise and outputs\n
    those values onto video stream"""

    try:
        shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        angle = calc_angle(shoulder, elbow, wrist)
        angle = round(angle, 2)
        
        if angle > 167:
            phase = 'UP'
        if angle < 70 and phase == 'UP':
            phase = 'DOWN'
            counter += 1    
        
        cv.putText(image, phase, (150, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (100,255,100), 3)
        cv.putText(image, str(counter), (50, 300), 0, 2, (248,183,7), 3)
        return counter, phase 
    except:
        pass    


def pushup(image, landmarks, counter, phase) -> tuple[float, str]:
    """This function, if specified is called automaticaly by mp_stream function.\n 
    It tracks and returns count and phase for given exercise and outputs\n
    those values onto video stream"""
    
    try:
        shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        angle = calc_angle(shoulder, elbow, wrist)
        angle = round(angle, 2)
        
        if angle > 167 and phase == 'UP':
            phase = 'DOWN'
            counter += 1    
        if angle < 43:
            phase = 'UP'
        
        cv.putText(image, phase, (300, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (100,255,100), 3)
        cv.putText(image, str(counter), (50, 300), 0, 2, (248,183,7), 3)
        return counter, phase 
    except:
        pass


def squat(image, landmarks, counter, phase) -> tuple[float, str]:
    """This function, if specified is called automaticaly by mp_stream function.\n 
    It tracks and returns count and phase for given exercise and outputs\n
    those values onto video stream"""
    
    try:
        shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        angle = calc_angle(shoulder, elbow, wrist)
        angle = round(angle, 2)
        
        if angle > 167 and phase == 'UP':
            phase = 'DOWN'
            counter += 1    
        if angle < 60:
            phase = 'UP'
        
        cv.putText(image, phase, (150, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (100,255,100), 3)
        cv.putText(image, str(counter), (50, 300), 0, 2, (248,183,7), 3)
        return counter, phase 
    except:
        pass
