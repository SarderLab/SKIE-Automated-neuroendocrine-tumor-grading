# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 10:44:45 2019

@author: d8
"""

import openslide
import numpy as np
import matplotlib.pyplot as plt
from skimage import transform
from col_deconv_main import col_deconv
from getWindows import getWindows
from highRes_stainSep import getnucthre
from get_ki67_index import get_ki67_index
import cv2
from scipy.misc import imresize
from get_xy_rev import get_xy_rev
from skimage.measure import label,regionprops
from getbias import getbias
import time

''' User defined values'''
'''===================='''

slide_no =2
print(slide_no)
no_hotposts = 5 # User-defined number of hot-spots

'''Variables'''
'''=========='''

Thre = 0.01

'''Fixed variables'''
'''=========='''
w = 250 #hot-spot window size
K = 3 #k-means cluster number

'''Get pointer for WSI'''
''' ====================='''

source=openslide.open_slide("/home/d8/DG_ki67/Images/HE/"+str(slide_no)+".svs")
source2 = openslide.open_slide("/home/d8/DG_ki67/Images/Syn/"+str(slide_no)+".svs")

print("Opening WSIs in mid resolution...")
syn = np.array(source2.read_region((0,0),1,source2.level_dimensions[1]),dtype = "uint8")
heimg = np.array(source.read_region((0,0),1,source.level_dimensions[1]),dtype = "uint8")

print("Removing alpha channel...")
syn1 = syn[:,:,0:3]
he1 = heimg[:,:,0:3]

print("Registering images...")
x,y = get_xy_rev(slide_no) # Comment out line 55 and add lines 57 to 69 if you need to pick new registration points

#plt.figure()
#plt.imshow(he1)
#print("Please click 10 points from H&E image")
#x = plt.ginput(10)
#print("clicked", np.asarray(x))
#plt.show()
#
#plt.figure()
#plt.imshow(syn1)
#print("Please click 10 points from synaptophysin image")
#y = plt.ginput(10)
#print("clicked", np.asarray(y))
#plt.show()

tform = transform.estimate_transform('similarity', np.asarray(x),np.asarray(y))
im2 = transform.warp(he1, inverse_map=tform.inverse) 

print("Ki-67 and synaptophysin detection in mid resolution...")
ihc_rgb = syn1
[rbias,kbias] = getbias(slide_no)
blur_red_mr,ki_mask_mr = col_deconv(ihc_rgb,rbias,kbias)

print("Find location of ki-67 positive nuclei within tumor regions")
label_image1 = label(ki_mask_mr)

coords1 = []
X_ki67spot = []
Y_ki67spot = []
for region1 in regionprops(label_image1):
    centroid1 = region1.centroid
    X_ki = [int(centroid1[0])]
    Y_ki = [int(centroid1[1])]
    X_ki67spot.append(X_ki)
    Y_ki67spot.append(Y_ki)

# For display purposes select 1st and last pixel of WSI
X_ki67spot.append([0])
X_ki67spot.append([int(source2.level_dimensions[1][1])])

Y_ki67spot.append([0])
Y_ki67spot.append([int(source2.level_dimensions[1][0])])

bin_x =int(source2.level_dimensions[1][0]/w)
bin_y = int(source2.level_dimensions[1][1]/w)
#print(bin_x,bin_y)
hist, xbins, ybins, _ = plt.hist2d(np.asarray(Y_ki67spot)[:,0],np.asarray(X_ki67spot)[:,0],[bin_x,bin_y])
xcenters = (xbins[:-1] + xbins[1:]) * 0.5
ycenters = (ybins[:-1] + ybins[1:]) * 0.5
Elem_indx = []
for i in np.ndindex(hist.shape):
    Elem_indx.append([i[0],i[1],hist[i]]) 
    
indx_histovalues = sorted(Elem_indx, reverse = True,key=lambda a_entry: a_entry[2])
indx_histovalues = np.asarray(indx_histovalues)

plt.figure()
plt.hist2d(np.asarray(Y_ki67spot)[:,0],np.asarray(X_ki67spot)[:,0],[bin_x,bin_y])
plt.imshow(syn1)
plt.plot(Y_ki67spot,X_ki67spot,'o',markersize = 6, color = 'k')
plt.plot(Y_ki67spot,X_ki67spot,'o',markersize = 4, color = 'w')
plt.colorbar()
plt.show()

hotspot_count = 0
arrB = np.array([])
arrK = np.array([])
ID_stack = []

while hotspot_count <no_hotposts:
    for ui in indx_histovalues:
        crop_imghe,crop_imgsyn = getWindows(source2,source,int(xcenters[int(ui[0])]),int(ycenters[int(ui[1])]),tform)
        f2 =plt.figure()
        plt.imshow(crop_imgsyn)
        plt.show() 
        
        user_input1 = raw_input('y/n?')#input('y/n?')#raw_input('y/n?') - choose one or the other based on the python version
        print(user_input1)
        
        if user_input1=='y':
            start = time.time()
            crop_imghe,crop_imgsyn = getWindows(source2,source,int(xcenters[int(ui[0])]),int(ycenters[int(ui[1])]),tform)
            hotspot_count+=1
            print(hotspot_count)
            cen = [int(ycenters[int(ui[1])]),int(xcenters[int(ui[0])])]

            mid_imgsyn = syn1[int(cen[0]-(w/2)):int(cen[0]+(w/2)),int(cen[1]-(w/2)):int(cen[1]+(w/2)),0:3]
            R =  blur_red_mr[int(cen[0]-(w/2)):int(cen[0]+(w/2)),int(cen[1]-(w/2)):int(cen[1]+(w/2))]

            Ki_final1 =  ki_mask_mr[int(cen[0]-(w/2)):int(cen[0]+(w/2)),int(cen[1]-(w/2)):int(cen[1]+(w/2))]
            syn_final = np.array(imresize(R,crop_imghe.shape,interp = 'nearest'))
            Ki_final = np.array(imresize(Ki_final1,crop_imghe.shape,interp = 'nearest'))

            _,syn_final =  cv2.threshold((syn_final),Thre,255,cv2.THRESH_BINARY)
            _,Ki_final =  cv2.threshold((Ki_final),Thre,255,cv2.THRESH_BINARY)

            Blue_final2= getnucthre(crop_imghe[:,:,0:3],K,slide_no)
            
            Blue_final = cv2.bitwise_and(cv2.convertScaleAbs(Blue_final2),cv2.convertScaleAbs(syn_final))

            BlueNO,KiNO = get_ki67_index(Blue_final,Ki_final)
            arrB = np.hstack((arrB, BlueNO))
            arrK = np.hstack((arrK, KiNO))
            
            IDX = KiNO/BlueNO   
            
            if IDX<0.025:
                Grade =1
            elif IDX<0.2:
                Grade =2
                
            else:
                Grade =3
           
            end = time.time()
            print(end - start)
            fig2, axes = plt.subplots(2, 2, figsize=(7, 6), sharex=True, sharey=True)
            ax = axes.ravel()
            
            ax[0].imshow(crop_imgsyn[:,:,0:3])
            ax[0].set_title("Double stain image")
            
            ax[1].imshow(crop_imghe[:,:,0:3])
            ax[1].set_title("H&E")
            
            ax[2].imshow(crop_imghe[:,:,0:3])
            ax[2].contour(Blue_final,[0.5],colors = 'r')
            ax[2].set_title("Non proliferating nuclei")
            
            ax[3].imshow(crop_imgsyn[:,:,0:3])
            ax[3].contour(syn_final,[0.5],colors = 'b')
            ax[3].contour(Ki_final,[0.5],linewidths = 4,colors = 'g')
            ax[3].contour(Blue_final,[0.5],colors = 'r')

            ax[3].set_title("%d : B: (%.3f) ; K: (%.3f); IDX : (%.3f); Grade :(%d)" % (slide_no, BlueNO, KiNO, (KiNO/BlueNO), Grade))

            ID_stack.append(IDX) 
            if hotspot_count>=no_hotposts:
                break
        else:
            continue
