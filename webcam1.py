#!/usr/bin/python
# -*- coding: utf-8 -*-

# Programa simples com camera webcam e opencv

import cv2
import os,sys, os.path
import numpy as np


def image_da_webcam(imgage):
    """
    ->>> !!!! FECHE A JANELA COM A TECLA ESC !!!! <<<<-
        deve receber a imagem da camera e retornar uma imagems filtrada.
    """
    img = cv2.imread('circulo.png')

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    image_lower_blue = np.array([50, 50, 50])  
    image_upper_blue = np.array([90, 255, 249])

    image_lower_reed = np.array([0, 55, 50])  
    image_upper_reed = np.array([16, 240, 231])

    mask1 = cv2.inRange(img_hsv, image_lower_blue, image_upper_blue)
    mask2 = cv2.inRange(img_hsv, image_lower_reed, image_upper_reed)

    mask = mask1 + mask2

    res = cv2.bitwise_and(img_hsv,img_hsv, mask= mask)


    contornos, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB) 
    contornos_img = mask_rgb.copy()

    cv2.drawContours(contornos_img, contornos, -1, [255, 0, 0], 5);


    size = 20
    color = (128,128,0)

    # lista_de_contorno = cv2.contourArea(cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE))
    # print("areas dos contornos", lista_de_contorno)

    coords = []

    for cnt in contornos:
        M = cv2.moments(cnt)
        
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        area = cv2.contourArea(cnt)
        if(area >= 22854.0):

            cv2.line(contornos_img,(cx - size,cy),(cx + size,cy),color,5)
            cv2.line(contornos_img,(cx,cy - size),(cx, cy + size),color,5)
            coords.append(cx)
            coords.append(cy)
            print("centro de massa na possição: x:",cx, " y:", cy, "- Area: ", area)

    print(coords)
    cv2.line(contornos_img, (coords[0],coords[1]),(coords[2],coords[3]), [0, 255, 0], 5)


    imgage = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    return imgage

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
