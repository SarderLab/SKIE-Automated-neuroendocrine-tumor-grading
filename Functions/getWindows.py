# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 15:38:21 2018

@author: Darshana Govind (d8@buffalo.edu)
"""
import numpy as np
def getWindows(source_syn,source_he,pointx,pointy,tform,w):

    centroids = [pointx,pointy]
    xy_w_o2 = tform.inverse(centroids)[0]
        
    startxhe = int(max((xy_w_o2[0]-(w/2))*4,0))
    startyhe = int(max((xy_w_o2[1]-(w/2))*4,0))
    startxsyn = int(max((centroids[0]-(w/2))*4,0))
    startysyn = int(max((centroids[1]-(w/2))*4,0))
    endx = int(min(w*4,source_syn.dimensions[0]-xy_w_o2[0]))
    endy = int(min(w*4,source_syn.dimensions[1]-xy_w_o2[1]))
#    
   
    crop_imghe = np.array(source_he.read_region(((startxhe),(startyhe)),0,((endx),(endy))),dtype = "uint8")
    crop_imgsyn = np.array(source_syn.read_region(((startxsyn),(startysyn)),0,((endx),(endy))),dtype = "uint8")
    return crop_imghe,crop_imgsyn