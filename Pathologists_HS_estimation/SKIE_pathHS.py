import openslide
import numpy as np
import matplotlib.pyplot as plt
from getMaskFromXml import getMaskFromXml
import cv2
from skimage import transform
from col_deconv_main import col_deconv
from getWindows import getWindows
from highRes_stainSep import getnucthre
from get_ki67_index import get_ki67_index
from scipy.misc import imresize
from get_xy_rev import get_xy_rev
from getbias import getbias
import math

''' User defined values'''
'''===================='''
slide_nos_recalculate = [44,45,46,47,48,49]

'''Fixed values'''                                                                
'''=========='''
w = 250
K = 3

'''Variables'''
'''========='''

Thre = 0.1
DiscSize = 6
nuc_ero_disc = 4

for i in slide_nos_recalculate:
    
    slide_no =i#5
    print(slide_no)
    
    '''Fixed values'''                                                                
    '''=========='''
    w = 250
    K = 3
        
    '''Get pointer for WSI'''
    ''' ====================='''
    source=openslide.open_slide("/hdd/d8/Images/HE/"+str(slide_no)+".svs")
    source2 = openslide.open_slide("/hdd/d8/Images/Syn/"+str(slide_no)+".svs")
    xmlpath = ("/hdd/d8/Images/synxml_KJ/"+str(slide_no)+".xml")
    
    print("Opening WSIs in mid resolution...")
    syn = np.array(source2.read_region((0,0),1,source2.level_dimensions[1]),dtype = "uint8")
    heimg = np.array(source.read_region((0,0),1,source.level_dimensions[1]),dtype = "uint8")

    print("Removing alpha channel...")
    syn1 = syn[:,:,0:3]
    he1 = heimg[:,:,0:3]

    print("Registering images...")
    x,y = get_xy_rev(slide_no)
    tform = transform.estimate_transform('similarity', np.asarray(x),np.asarray(y))
    im2 = transform.warp(he1, inverse_map=tform.inverse) 

    print("Ki-67 and synaptophysin detection in mid resolution...")
    ihc_rgb = syn1
    [rbias,kbias] = getbias(slide_no)
    blur_red_mr,ki_mask_mr = col_deconv(ihc_rgb,rbias,kbias,DiscSize)       
    TissueMask_Main = getMaskFromXml(source,xmlpath)

    _, contours,_ = cv2.findContours(TissueMask_Main.copy(), 1, 2)
    moments = [cv2.moments(cnt) for cnt in contours]
    centroids = [(int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])) for M in moments]
#    
    arrB = []
    arrK = []
    ID_stack = []
    hotspot_count = 0
    for eachCenter in centroids:
        hotspot_count+=1
        print(hotspot_count)
        crop_imghe,crop_imgsyn = getWindows(source2,source,int(eachCenter[0]),int(eachCenter[1]),tform,w)
        crop_imghe = crop_imghe[:,:,0:3]
        
        mid_imghe = syn1[int(eachCenter[1]-(w/2)):int(eachCenter[1]+(w/2)),int(eachCenter[0]-(w/2)):int(eachCenter[0]+(w/2)),0:3]
        cen = eachCenter
        R =  blur_red_mr[int(cen[1]-(w/2)):int(cen[1]+(w/2)),int(cen[0]-(w/2)):int(cen[0]+(w/2))]
        
        cen = eachCenter

        Ki_final =  ki_mask_mr[int(cen[1]-(w/2)):int(cen[1]+(w/2)),int(cen[0]-(w/2)):int(cen[0]+(w/2))]
        syn_final = np.array(imresize(R,crop_imghe.shape,interp = 'nearest'))
        Ki_final = np.array(imresize(Ki_final,crop_imghe.shape,interp = 'nearest'))
    
        _,syn_final =  cv2.threshold((syn_final),Thre,255,cv2.THRESH_BINARY)#val2+0.06
        _,Ki_final =  cv2.threshold((Ki_final),Thre,255,cv2.THRESH_BINARY)#val2+0.06

        Blue_final2= getnucthre(crop_imghe[:,:,0:3],K,slide_no,nuc_ero_disc)
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
 
        f2 =plt.figure()
        plt.imshow(crop_imgsyn[:,:,0:3])
        plt.contour(syn_final,[0.5],colors = 'b')
        plt.contour(Ki_final,[0.5],linewidths = 4, colors = 'g')
        plt.title("%d : B: (%.3f) ; K: (%.3f); IDX : (%.3f); Grade :(%d)" % (slide_no, math.floor(BlueNO), KiNO, (KiNO/BlueNO), Grade))
        plt.show() 
        f2.savefig((str(slide_no)+"_"+str(hotspot_count)+".png"),format='png', dpi=300)
        
  