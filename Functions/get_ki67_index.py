# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 16:50:22 2018

@author: Darshana Govind (d8@buffalo.edu)
"""
import numpy as np
import skimage.measure as measure
from matplotlib import pyplot as plt
import math

def get_ki67_index(Blue_final,Ki_final):
    blobs_labels = measure.label(Blue_final, background=0)
    
    
    properties = measure.regionprops(blobs_labels)
    list_obj_blue = [prop.area for prop in properties]
    
    blobs_labels_ki = measure.label(Ki_final, background=0)
    properties_ki = measure.regionprops(blobs_labels_ki)
    list_obj_ki = [prop.area for prop in properties_ki]
    
    # the histogram of the data
#    n, bins, patches = plt.hist(list_obj_blue, 50, density=True, facecolor='g', alpha=0.75)

# Supplementary figure 2>>>>>
#    plt.xlabel('Distribution of area of nuclei')
#    plt.ylabel('Probability')
#    plt.title(np.median(list_obj_blue))
#    plt.plot([np.median(list_obj_blue),np.median(list_obj_blue)],[0,0.015],'r-')
#    plt.grid(True)
#    plt.show()

    if len(list_obj_blue)==0:
        BlueNO=0
    else:
        BlueNO = (sum(list_obj_blue))/(np.median(list_obj_blue))

    KNO = len(list_obj_ki)
    BlueNO = BlueNO - KNO
    if BlueNO<0 or math.isnan(BlueNO):
        BlueNO=KNO

    return BlueNO,KNO