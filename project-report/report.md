# TBD

:o: wrong format
# OCR Extraction Implementation with Tesseract :hand:

| Joao Paulo Leite
| jleite@iu.edu
| Indiana University
| hid: 
| github: [:cloud:]()
| code: [:cloud:]()

---

Keywords: OCR, Tesseract, Python
          
---

## Abstract

The main purpose of this project is to create a simple 
OCR extraction implementation which is able to extract 
key metadata from documents. To accomplish this, Google's 
Tesseract OCR Engine is leveraged to provide full-page OCR 
data. The goal is to have a configurable extraction engine 
that allows users to pin-point the meta-data to be extracted 
and output said meta-data.

## Introduction

Optical Character Recognition (OCR) technology first appeared 
in the 1940's and grew alongside the rise of the digital computer.
It was not until the late 1950's when OCR machines became 
commercially available and today this technology presents itself 
in both hardware devices as well as software offerings 
[@hid-sp18-414-www-eikvilocr].OCR is the first step in enabling 
the extraction of actionable data by transforming print on an 
image(document) to machine encoded text. The analysis of the output 
provided by OCR engines allows for this key data to be used for 
downstream processes and reporting. Documents fall into three categories: 
structured documents, semi-structured documents and unstructured documents. 

> Gartner, a leading technology analysis firm, has stated the following, 
> “…the amount of data stored in companies will increase by 800 percent by 
> 2018, 80 percent of which would include unstructured data that are harder 
> to tame and manage. The biggest challenges for companies will include: 
> collecting, managing, storing, searching and archiving this content
> [@hid-sp18-414-www-ecmandbigdata].” 

As unstructured documents continues to grow, big data systems are being 
introduced as a solution to analyze and organize this data. As a precursor, 
an OCR extraction solution can extract actionable data from documents and 
provide structure to unstructured content. 

## Overview of Optical Character Recognition

The main principle in Optical Character Recognition (OCR) is to 
automatically recognize character patterns. This is accomplished by teaching 
the system each class of pattern that can occur and providing a set of 
examples for each pattern. At the time of recognition, the system 
performs a comparison between the unknown character provided and 
the previously provided examples, assigned the appropriate class to 
the closest match[@hid-sp18-414-www-eikvilocr]. This system is 
designed to solely transform text on a document into machine encoded 
text and additional systems must be built to further extract relevant information
from the document, that is to say, the process of OCR is the first step 
in transforming structured, semi-structured and unstructured documents 
into valuable and relevant information.


## Context Based Extraction Engine


This project utilizes Google's Open Source Tesseract OCR engine to provide
HOCR output that is leveraged to begin the process of extracting information 
from unstructured data provided by Tesseract. The extraction engine's logic works 
in two distinct phases, the identification of potential candidates( data which follows 
a specific format) and the scoring of each candidate based on context around said 
candidate. At the end of this process, the candidate which obtained the highest 
score will be selected. 

### Image Thresholding

Before submitting the image into Tesseract, image clean
up is performed to create a bitonal image and to remove any noise that
may be present. This process consists of three steps; standardizing 
image DPI, smoothing the image and removing noise from the 
image[@hid-sp18-414-www-imagethresholding].

Standarizing Image DPI to 300 DPI:

> def set_dpi(path):
>
>   image = IMG.open(path)
>   len_x, wid_y = image.size
>   factor = max(1, int(1800 / len_x))
>   size = factor * len_x, factor * wid_y
>   image_resized = image.resize(size, IMG.ANTIALIAS)
>   temp_f = tempfile.NamedTemporaryFile()
>   temp_fn = temp_f.name
>   image_resized.save(temp_fn, dpi=(300, 300))
>
>   return temp_fn


Converting to Bitonal Image via Adaptive Thresholding:

> def remove_noise(name):
>   
>   image = cv2.imread(name, 0)
>   filtered = cv2.adaptiveThreshold(image.astype(np.uint8), 255, 
>   cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
>   core = np.ones((1, 1), np.uint8)
>   opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, core)
>   closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, core)
>   image = smooth(image)
>   original_image = cv2.bitwise_or(image, closing)
>   
>   return original_image

Smoothing Image:

> def smooth(image):
>
>   ret1, th1 = cv2.threshold(image, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
>   ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
>   blur = cv2.GaussianBlur(th2, (1, 1), 0)
>   ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
>   
>   return th3
