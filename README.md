# SKIE: Automated neuroendocrine tumor grading

This repository contains the source codes for the publication,"Automated hotspot selection and Ki-67 index quantitation from whole slide images of gastrointestinal neuroendocrine tumors", submitted to Modern Pathology journal on ##/July/2019. All algorithms were developed and written by [Darshana Govind](https://github.com/DarshanaGovind).

# Image data

Whole slide images (WSIs) of three adjacent tissue sections stained with hemotoxylin and eosin (H&E), Ki-67 alone, and double immunohistochemical staining (synaptophysin-Ki-67-hemotoxylin) from 50 gastrointestinal neuroendocrine tumor (GI-NET) biopsies are available at: (https://buffalo.app.box.com/folder/79962857765)

# Requirements

Openslide (1.1.1) (https://openslide.org/)<br/>
NumPy (1.14.2) (https://www.numpy.org/) <br/>
Skimage (0.13.1) (https://scikit-image.org/docs/dev/api/skimage.html) <br/>
scipy (1.0.1) (https://www.scipy.org/) (<br/>
OpenCV Python (3.4.2) (https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html)<br/>
csv (1.0) (https://docs.python.org/2/library/csv.html) <br/>

# Contents

"SKIE_main0619.py" reproduces the automated hot-spot selection and Ki-67 index results presented in the paper.  

Functions:
This directory contains the functions necessary to run "SKIE_main0619.py".

PathologistHS-analysis
This directory contains "SKIE_pathHS.py" which extracts the pathologist-chosen hot-spots from the annotated xml files and computes the Ki-67 index from the hot-spots. This directory also contains "getMaskFromXml.py" which is the function to automatically extract hot-spots of pre-determined size from xml files.

# Usage

Create two distinct folders containing the H&E stained WSIs and the double immunostained WSIs in .svs format and specify their paths in "SKIE_main0619.py". The variable 'no_hotspots' decides the number of hot-spots to be extracted, which is five, in this study.

You can run the code by typing in the command line:<br/>
'python SKIE_main0619.py' 

For image registration, the ten landmark points to be selected on the two images to be registered have already been saved for the 50 WSIs, which can be retrieved via the function "get_xy_rev.py". In order to select you own set of points, comment out line 51 and add lines 53-65 which enables the user to select the landmark points, through an interactive window.

Once the algorithm detects the highest hot-spot, SKIE displays the hot-spot and waits for the user input ('y/n?') for quality control purposes. If the hot-spot is of adequate quality, type 'y' and SKIE displays the next hot-spot until the selected number of hot-spots. 





