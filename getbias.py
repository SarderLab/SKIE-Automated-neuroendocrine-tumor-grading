# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 16:32:18 2019

@author: d8
"""

def getbias(slide_no):
    if slide_no == 1:
        rbias = 0.6
        kbias = 0.65
    if slide_no == 8:
        rbias = 0.5
        kbias = 0.7
    if slide_no == 8 or slide_no == 10:
        rbias = 0.5
        kbias = 0.7
    if slide_no == 27 or slide_no == 41:
        rbias = 0.56
        kbias = 0.65
    else:
        rbias = 0.5
        kbias = 0.65
    return [rbias,kbias]