from highRes_stainSep import getnucthre
import openslide
import numpy as np
import matplotlib.pyplot as plt
from skimage import transform
from col_deconv_main import col_deconv
from getWindows import getWindows
from get_ki67_index import get_ki67_index
import cv2
from scipy.misc import imresize
from get_xy_rev import get_xy_rev
from skimage.measure import label,regionprops
from getbias import getbias
import skimage
import csv

''' User defined values'''
'''===================='''
Thre = 0.01
for sli in range(1,51,1):
    
    slide_no =sli
    print(slide_no)
    
    '''Variables'''
    '''=========='''
    w = 250 # tile size 
    K = 3 #kmeans k = 3
    
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
    x,y = get_xy_rev(slide_no)
    
    tform = transform.estimate_transform('similarity', np.asarray(x),np.asarray(y))
    im2 = skimage.img_as_ubyte(transform.warp(he1, inverse_map=tform.inverse))   
    
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
    
    ki67_positive_cells = len(X_ki67spot)    
  
    X_ki67spot.append([0])
    X_ki67spot.append([int(source2.level_dimensions[1][1])])
    
    Y_ki67spot.append([0])
    Y_ki67spot.append([int(source2.level_dimensions[1][0])])
    
    bin_x =int(source2.level_dimensions[1][0]/w)
    bin_y = int(source2.level_dimensions[1][1]/w)
    hist, xbins, ybins, _ = plt.hist2d(np.asarray(Y_ki67spot)[:,0],np.asarray(X_ki67spot)[:,0],[bin_x,bin_y])
    xcenters = (xbins[:-1] + xbins[1:]) * 0.5
    ycenters = (ybins[:-1] + ybins[1:]) * 0.5
    Elem_indx = []
    for i in np.ndindex(hist.shape):
        Elem_indx.append([i[0],i[1],hist[i]]) 
        
    indx_histovalues = sorted(Elem_indx, reverse = True,key=lambda a_entry: a_entry[2])
    indx_histovalues = np.asarray(indx_histovalues)

    hotspot_count = 0
    arrB = np.array([])
    arrK = np.array([])
    Slide_info = []
    
    a_count = 0
    blue_count_sum = 0
    for ui in indx_histovalues:
        cen = [int(ycenters[int(ui[1])]),int(xcenters[int(ui[0])])]
    
        R =  blur_red_mr[int(cen[0]-(w/2)):int(cen[0]+(w/2)),int(cen[1]-(w/2)):int(cen[1]+(w/2))]
    
        if R.any():

            crop_imghe,crop_imgsyn = getWindows(source2,source,int(xcenters[int(ui[0])]),int(ycenters[int(ui[1])]),tform)
            a_count+=1
            print(a_count)
            cen = [int(ycenters[int(ui[1])]),int(xcenters[int(ui[0])])]

            Ki_final1 =  ki_mask_mr[int(cen[0]-(w/2)):int(cen[0]+(w/2)),int(cen[1]-(w/2)):int(cen[1]+(w/2))]
            syn_final = np.array(imresize(R,crop_imghe.shape,interp = 'nearest'))
            Ki_final = np.array(imresize(Ki_final1,crop_imghe.shape,interp = 'nearest'))
            _,syn_final =  cv2.threshold((syn_final),Thre,255,cv2.THRESH_BINARY)
            Blue_final2= getnucthre(crop_imghe[:,:,0:3],K,slide_no)          
            Blue_final = cv2.bitwise_and(cv2.convertScaleAbs(Blue_final2),cv2.convertScaleAbs(syn_final))
            BlueNO,KiNO = get_ki67_index(Blue_final,Ki_final)

            if BlueNO==0 or KiNO==0:
                IDX = 0
            else:
                IDX = KiNO/BlueNO
        
            if IDX<0.025:
                Grade =1
            elif IDX<0.2:
                Grade =2
            else:
                Grade =3
            
          
            blue_count_sum = blue_count_sum + BlueNO
            if BlueNO==0:
                ID_X = [a_count,KiNO,BlueNO,0]
            else:
                ID_X = [a_count,KiNO,BlueNO,KiNO/BlueNO]
            Slide_info.append(ID_X)
            
    EXfilename = "WSI_excel_blocks/WSI_optHS_"+str(slide_no)
    myFile = open(EXfilename+'.csv', 'w')  
    with myFile:
        
        writer = csv.writer(myFile)
        writer.writerows(Slide_info)
