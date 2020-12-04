import numpy as np
from numpy import linalg
from skimage.util import dtype
from skimage.color import rgb2grey
from skimage.exposure import rescale_intensity
import cv2
from skimage.morphology import disk,dilation ,erosion

'''Stain deconvolution'''
''' ====================='''
color_vector = np.array([[0.644, 0.710, 0.285],
                         [0.0326, 0.873, 0.487],
                         [0.270, 0.562, 0.781]])

converted = linalg.inv(color_vector)

def col_deconv(Img,bias,ki67bias,DiscSize):
    Img = dtype.img_as_float(Img, force_copy=True)
    Img += 2
    stains = np.dot(np.reshape(-np.log(Img), (-1, 3)), converted)
    ihc_hrd = np.reshape(stains, Img.shape)
    print("Color deconvolution...")
    
    synaptophysin_1 = rescale_intensity(ihc_hrd[:, :, 1], out_range=(0,1))
    synaptophysin_final = rgb2grey(np.dstack((np.zeros_like(synaptophysin_1), synaptophysin_1, synaptophysin_1)))
    
    DAB_1 = rescale_intensity(ihc_hrd[:, :, 2], out_range=(0,1))
    DAB_final = rgb2grey(np.dstack((np.zeros_like(DAB_1), DAB_1, DAB_1)))
    
    
    print("Thresholding ki67...")
    
    _,thre_ki67 = cv2.threshold(DAB_final,ki67bias,255,cv2.THRESH_BINARY)
    
    print("Otsu thresholding of synaptophysin...")
    
    ret,blur_red =  cv2.threshold((synaptophysin_final),bias,255,cv2.THRESH_BINARY)
    blur_red = dilation(blur_red,disk(DiscSize)) 
    blur_red_mr = erosion(blur_red,disk(DiscSize)) 
    ki_mask_mr2 = cv2.bitwise_and((thre_ki67), (blur_red_mr))

    return blur_red_mr,ki_mask_mr2
