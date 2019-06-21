# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 15:55:14 2018

@author: d8
"""
from skimage.color import rgb2grey
import numpy as np
import cv2

nuc_ero_disc = 4
def getnucthre(image,K, slide_no):
   
     
    Z = image.reshape((-1,3))
    Z = np.float32(Z)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((image.shape))
    res3 = rgb2grey(res2)
    
    Min_value = min(np.unique(res3))
    ind = np.where(res3 == Min_value)
    
    lab2 = res2[int(ind[0][0]),int(ind[1][0])]

    lab2 = np.array(lab2)
    lower = lab2-1
    upper = lab2+1
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")
    kernel_b = np.ones((nuc_ero_disc,nuc_ero_disc),np.uint8)
    mask = cv2.inRange(res2, lower, upper)
    Blue_final = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_b)

    return Blue_final
