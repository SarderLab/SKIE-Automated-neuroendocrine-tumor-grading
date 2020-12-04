from skimage.color import separate_stains,rbd_from_rgb
from skimage.exposure import rescale_intensity
import cv2
from skimage.morphology import disk,dilation ,erosion

'''Stain deconvolution'''
''' ====================='''

from skimage.color import rgb2hed

def col_deconv(Img,bias,ki67bias,DiscSize):
    
    ihc_hrd_DAB = rgb2hed(Img)
    ihc_hrd_syn = separate_stains(Img, rbd_from_rgb)        
    
    print("Color deconvolution...")
    
    synaptophysin_1 = rescale_intensity(ihc_hrd_syn[:, :, 1], out_range=(0,1))  
    DAB_1 = rescale_intensity(ihc_hrd_DAB[:, :, 2], out_range=(0,1))
    
    
    print("Thresholding ki67...")
    
    _,thre_ki67 = cv2.threshold(DAB_1,ki67bias,255,cv2.THRESH_BINARY)
    
    print("Otsu thresholding of synaptophysin...")
    
    ret,blur_red =  cv2.threshold((synaptophysin_1),bias,255,cv2.THRESH_BINARY)
    blur_red = dilation(blur_red,disk(DiscSize)) 
    blur_red_mr = erosion(blur_red,disk(DiscSize)) 
    ki_mask_mr2 = cv2.bitwise_and((thre_ki67), (blur_red_mr))

    return blur_red_mr,ki_mask_mr2
