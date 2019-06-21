# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 12:51:11 2019

@author: d8
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 10:42:33 2019

@author: d8
"""
from xml.dom import minidom
import numpy as np
import openslide
from skimage.draw import polygon
import cv2

#source2 = openslide.open_slide("/hdd/d8/Images/HE/22.svs")
#xmlpath = '22.xml'

def getMaskFromXml(source,xmlpath):
    [l,m] = source.level_dimensions[0]
    xml = minidom.parse(xmlpath)
    mask = np.zeros((m,l),'uint8');
    regions_ = xml.getElementsByTagName("Region")
    regions, region_labels = [], []
    for region in regions_:
        vertices = region.getElementsByTagName("Vertex")
        attribute = region.getElementsByTagName("Attribute")
        if len(attribute) > 0:
            r_label = attribute[0].attributes['Value'].value
        else:
            r_label = region.getAttribute('Text')
        region_labels.append(r_label)
        
        # Store x, y coordinates into a 2D array in format [x1, y1], [x2, y2], ...
        coords = np.zeros((len(vertices), 2))
        
        for i, vertex in enumerate(vertices):
            coords[i][0] = vertex.attributes['X'].value
            coords[i][1] = vertex.attributes['Y'].value
        regions.append(coords)
        [rr,cc] = polygon(np.array([i[1] for i in coords]),np.array([i[0] for i in coords]),mask.shape)
        mask[rr,cc] = 255
    print(source.level_dimensions[1])
    mask = cv2.resize(mask, dsize=source.level_dimensions[1], interpolation=cv2.INTER_CUBIC)
    return mask
    

