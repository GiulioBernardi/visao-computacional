#!/usr/bin/python
# -*- coding: utf-8 -*-

# Programa simples com camera webcam e opencv

import cv2
import os,sys, os.path
import numpy as np
import math
import cv2
import os,sys, os.path
import numpy as np
from pynput.keyboard import Key, Controller
import pynput
import time
import random

keyboard = Controller()

def image_da_webcam(img):
    """
    ->>> !!!! FECHE A JANELA COM A TECLA ESC !!!! <<<<-
        deve receber a imagem da camera e retornar uma imagems filtrada.
    """

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
    image_lower_blue = np.array([100, 200, 50])  
    image_upper_blue = np.array([116, 255, 100])

    image_lower_reed = np.array([0, 100, 100])  
    image_upper_reed = np.array([20, 255, 255])
    
    image_lower_reed2 = np.array([140, 100, 50])  
    image_upper_reed2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(img_hsv, image_lower_blue, image_upper_blue)
    mask2 = cv2.inRange(img_hsv, image_lower_reed, image_upper_reed)
    mask3 = cv2.inRange(img_hsv, image_lower_reed2, image_upper_reed2)
    
    res2 = cv2.bitwise_or(mask2,mask3)
    res = cv2.bitwise_or(mask1, res2)

    contornos, _ = cv2.findContours(res, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    cnts = sorted(contornos, key=cv2.contourArea, reverse=True)

    mask_rgb = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR) 
    contornos_img = mask_rgb.copy()

    cv2.drawContours(contornos_img, cnts, 0, [255, 0, 0], 5)
    cv2.drawContours(contornos_img, cnts, 1, [255, 0, 0], 5)
    size = 20
    color = (128,128,0)

    coords = []
    
    for cnt in cnts:
        M = cv2.moments(cnt)
        cx =0
        cy =0
        if(M['m00'] != 0):
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            area = cv2.contourArea(cnt)
            if(area >= 500):

                cv2.line(contornos_img,(cx - size,cy),(cx + size,cy),color,5)
                cv2.line(contornos_img,(cx,cy - size),(cx, cy + size),color,5)
                coords.append(cx)
                coords.append(cy)
                #print("centro de massa na possição: x:",cx, " y:", cy, "- Area: ", area)
        
            
    if(coords != 0 and len(coords) >= 3):
        cv2.line(contornos_img, (coords[0],coords[1]),(coords[2],coords[3]), [0, 255, 0], 5)
        dx = coords[0] - coords[2]
        dy = coords[1] - coords[3]
        angle = math.atan2(dy,dx)*180 /math.pi
        if(angle > 25):
            keyboard.press(pynput.keyboard.KeyCode.from_char('a'))
            time.sleep(0.2)
            keyboard.release(pynput.keyboard.KeyCode.from_char('a'))
        if(angle < -10):
            keyboard.press(pynput.keyboard.KeyCode.from_char('d'))
            time.sleep(0.2)
            keyboard.release(pynput.keyboard.KeyCode.from_char('d'))

        
        print(angle)
        
    return contornos_img

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)


if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    
    img = image_da_webcam(frame)


    cv2.imshow("preview", img)

    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()
