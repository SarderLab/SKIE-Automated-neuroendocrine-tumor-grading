# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 16:50:22 2018

@author: d8
"""
import numpy as np
from numpy import linalg
from skimage.util import dtype
from skimage.color import rgb2grey
from skimage.exposure import rescale_intensity
import cv2
from skimage.morphology import disk,dilation ,erosion

'''Stain deconvolution'''
''' ====================='''
DiscSize = 6
rgb_from_hrd = np.array([[0.644, 0.710, 0.285],
                         [0.0326, 0.873, 0.487],
                         [0.270, 0.562, 0.781]])

hrd_from_rgb = linalg.inv(rgb_from_hrd)

def separate_stains(rgb, color_deconv_vector):
    rgb = dtype.img_as_float(rgb, force_copy=True)
    rgb += 2
    stains = np.dot(np.reshape(-np.log(rgb), (-1, 3)), color_deconv_vector)
    return np.reshape(stains, rgb.shape)

def stainspace_to_2d_array(ihc_xyz, channel):
    rescale = rescale_intensity(ihc_xyz[:, :, channel], out_range=(0,1))
    stain_array = np.dstack((np.zeros_like(rescale), rescale, rescale))
    grey_array = rgb2grey(stain_array)
    return grey_array

def col_deconv(ihc_rgb,bias,ki67bias):
    ihc_hrd = separate_stains(ihc_rgb, hrd_from_rgb)
    print("Color deconvolution...")
    
    permred_Gray_Array = stainspace_to_2d_array(ihc_hrd, 1)
    DAB_Grey_Array = stainspace_to_2d_array(ihc_hrd, 2)
    
    print("Thresholding ki67...")
    
    _,thre_ki67 = cv2.threshold(DAB_Grey_Array,ki67bias,255,cv2.THRESH_BINARY)
    
    print("Otsu thresholding of synaptophysin...")
    
    ret,blur_red =  cv2.threshold((permred_Gray_Array),bias,255,cv2.THRESH_BINARY)
    blur_red = dilation(blur_red,disk(DiscSize)) 
    blur_red_mr = erosion(blur_red,disk(DiscSize)) 
    ki_mask_mr2 = cv2.bitwise_and((thre_ki67), (blur_red_mr))

    return blur_red_mr,ki_mask_mr2
