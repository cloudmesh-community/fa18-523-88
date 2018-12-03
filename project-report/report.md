# OCR Extraction Implementation with Tesseract :hand: fa18-523-88

| Joao Paulo Leite
| jleite@iu.edu
| Indiana University
| hid: fa18-523-88
| github: [:cloud:](https://github.com/cloudmesh-community/fa18-523-88/blob/master/project-report/report.md)
| code: [:cloud:](https://github.com/cloudmesh-community/fa18-523-88/tree/master/project-code)

---

Keywords: OCR, Tesseract, Python
          
---

:o: as pointed out previously on piazza, remove the word *project* or *report* from your report. simply sauy We

## Abstract

:o: The main purpose is to create a simple 
OCR extraction implementation which is able to extract 
key metadata from documents. 

The focus is to create an extraction engine that will work 
well for semi-structured and unstructured documents. As the 
volume of these documents are ever increasing, organizations 
are tasked with storing and organzing these doucments. An OCR tool 
that enables these  organizations to extract valuable information 
from these documents is the first step in being able to analyze the 
data that is currently locked within these documents.
:o: no explenation provided how this relates to buig data.

To accomplish this, Google's 
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

Gartner, a leading technology analysis firm, has stated the following:

:o: use of non ascii characters please do not just paste and coppy from word. Word produces dirty text for markdown. Previously mentioned in piazza FAQ.

> "...the amount of data stored in companies will increase by 800 percent by 
> 2018, 80 percent of which would include unstructured data that are harder 
> to tame and manage. The biggest challenges for companies will include: 
> collecting, managing, storing, searching and archiving this content
> [@hid-sp18-414-www-ecmandbigdata]."

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
from unstructured data provided by Tesseract. The extraction engine's logic works by 
indentifying potential candidates(data which follows a specific format) and the 
scoring of each candidate based on context around said candidate. At the end of this 
process, the candidate which obtained the highest score will be selected. 

For the extraction engine, there are 8 distinct phases: 

1. Image Thresholding
2. OCR Process
3. Transform HOCR Data
4. Define Candidates
5. Set Context
6. Group Context
7. Score Context
8. Output Results

### Image Thresholding

Before submitting the image into Tesseract, image clean
up is performed to create a bitonal image and to remove any noise that
may be present. This process consists of three steps; standardizing 
image DPI, smoothing the image and removing noise from the 
image[@hid-sp18-414-www-imagethresholding].

:o: spaces before brackets

Standarizing Image DPI to 300 DPI:

```python
def set_dpi(path):
    image = IMG.open(path)
    len_x, wid_y = image.size
    factor = max(1, int(1800 / len_x))
    size = factor * len_x, factor * wid_y
    # size = (1800, 1800)
    image_resized = image.resize(size, IMG.ANTIALIAS)
    temp_f = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_fn = temp_f.name
    image_resized.save(temp_fn, dpi=(300, 300))
    return temp_fn
```

Converting to Bitonal Image via Adaptive Thresholding:

```python
def remove_noise(name):
    image = cv2.imread(name, 0)
    filtered = cv2.adaptiveThreshold(image.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
    core = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, core)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, core)
    image = smooth(image)
    original_image = cv2.bitwise_or(image, closing)
    return original_image
```
Smoothing Image:

```python
def smooth(image):
    ret1, th1 = cv2.threshold(image, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3
```

### OCR Process

Google's Tesseract OCR engine is an open source engine that has the ability to
output HOCR. HOCR is an open standard of data representation for
formatted text obtained from an OCR engine. This standard includes 
text, style, layout information, recognition confidence and other info
in a XML structure. 

Create HOCR data:

:o: its easy to bring thsi to a smaller format that fits in 

```python
    def Run(self):
        DATA = pytesseract.image_to_pdf_or_hocr(image, lang=None, config='hocr', nice=0, extension='hocr')
```


### Transform HOCR Data

Once the HOCR results are generated, we must transform the results
into useable data for our extraction process. The first step is to target
the ocrx_word data from the results and parser it into separate words.
After this initial parsing is complete, we separate each individual data
point within a dictionary object with the values: value, confidence, 
left, top, right and bottom.

Parsing HOCR results with Beautiful Soup

```python
    def Run(self):
        soup = bs4.BeautifulSoup(DATA, 'html.parser')
        words = soup.find_all('span', class_='ocrx_word')
```

Creating word data structure:

:o: this prg is a non valid python prg due to indentation errors

:o: why not use variables or functions to make it more readbale

```python
def transform_hocr(self, words):
    # Convert HOCR to usable structure
    for x in range(len(words)):
        word[int(words[x]['id'].split('_')[2])] = {}
        word[int(words[x]['id'].split('_')[2])]['Value'] = words[x].get_text()
        word[int(words[x]['id'].split('_')[2])]['Confidence'] = words[x]['title'].split(';')[1].split(' ')[2]
        word[int(words[x]['id'].split('_')[2])]['Left'] = words[x]['title'].split(';')[0].split(' ')[1]
        word[int(words[x]['id'].split('_')[2])]['Top'] = words[x]['title'].split(';')[0].split(' ')[2]
        word[int(words[x]['id'].split('_')[2])]['Right'] = words[x]['title'].split(';')[0].split(' ')[3]
        word[int(words[x]['id'].split('_')[2])]['Bottom'] = words[x]['title'].split(';')[0].split(' ')[4]

```

### Define Candidates

After transforming the HOCR results, we use the generated word dictionary 
to find values that match the defined regular expression that was provided
by the user. All candidates which match the regular expression are 
stored within the candidates dictionary object with the values: value, confidence, 
left, top, right and bottom.

Finding candidates:

:o: indentation errors

```python
def find_candidates(self, RE_ATT):
    y = 1
    for z in RE_ATT:

        for x in range(len(word)):

            m = re.match(r'' + z + '', word[x + 1]['Value'], )

            if m:
                candidates[y] = {}
                candidates[y]['Value'] = word[x + 1]['Value']
                candidates[y]['Confidence'] = word[x + 1]['Confidence']
                candidates[y]['Left'] = word[x + 1]['Left']
                candidates[y]['Top'] = word[x + 1]['Top']
                candidates[y]['Right'] = word[x + 1]['Right']
                candidates[y]['Bottom'] = word[x + 1]['Bottom']
                print(candidates[y])
                y = y + 1
```

### Set Context

Using the location input define by the user, we will set the context of each
candidate based on the proximity(top, bottom, left and right) in pixels.
Each word which falls within the proper proximity is stored in the context
dictionary with the values: value, candidate ,word number, confidence,
left, top, right, bottom, line number and same line as candidate.

:o: prg unreadable, indentation errors

```python
def set_context(self, candidates, word):
    line = 1
    z = 1
    for x in range(len(candidates)):

        for y in range(len(word)):

            if (int(word[y + 1]['Bottom']) > int(candidates[x + 1]['Bottom']) - 100) and \
                    (int(word[y + 1]['Bottom']) < int(candidates[x + 1]['Bottom']) + 20) and \
                    (int(word[y + 1]['Right']) > int(candidates[x + 1]['Left']) - 700) and \
                    (int(word[y + 1]['Right']) < int(candidates[x + 1]['Left']) + 20):

                context[z] = {}
                context[z]['Value'] = word[y + 1]['Value']
                context[z]['Candidates'] = candidates[x + 1]['Value']
                context[z]['Word'] = str(y + 1)
                context[z]['Confidence'] = word[y + 1]['Confidence']
                context[z]['Left'] = word[y + 1]['Left']
                context[z]['Top'] = word[y + 1]['Top']
                context[z]['Right'] = word[y + 1]['Right']
                context[z]['Bottom'] = word[y + 1]['Bottom']

                if z == 1:
                    context[z]['Line'] = line
                elif context[z - 1]['Bottom'] == word[y + 1]['Bottom']:
                    context[z]['Line'] = line
                else:
                    line = line + 1
                    context[z]['Line'] = line

                if int(word[y + 1]['Bottom']) > int(candidates[x + 1]['Bottom']) - 15 and int(
                        word[y + 1]['Bottom']) < int(candidates[x + 1]['Bottom']) + 15:
                    context[z]['SameLine'] = "1"
                else:
                    context[z]['SameLine'] = "0"

                z = z + 1
```

### Group Context

Once the context for each candidate has been
defined, we will group the context based on proximity.
If mutliple context words are in sequence, we will group 
those so that they are arranged as a phrase.

```python
def define_groupcontext(self, context):
    # TRANSFORM CONTEXT INTO GROUPED CONTEXT
    # Context words that are on the same line and in sequence are grouped together
    z = 1
    for x in range(len(context)):

        if x == 0:
            groupcontext[z] = {}
            groupcontext[z]['Value'] = context[x + 1]['Value']
            groupcontext[z]['Word'] = context[x + 1]['Word']
            groupcontext[z]['Candidates'] = context[x + 1]['Candidates']
            groupcontext[z]['Weight'] = '0'
            groupcontext[z]['Confidence'] = context[x + 1]['Confidence']
            groupcontext[z]['Left'] = context[x + 1]['Left']
            groupcontext[z]['Top'] = context[x + 1]['Top']
            groupcontext[z]['Right'] = context[x + 1]['Right']
            groupcontext[z]['Bottom'] = context[x + 1]['Bottom']
            groupcontext[z]['SameLine'] = context[x + 1]['SameLine']

        elif int(groupcontext[z]['Word']) + 1 == int(context[x + 1]['Word']):

            groupcontext[z]['Value'] = groupcontext[z]['Value'] + ' ' + context[x + 1]['Value']
            groupcontext[z]['Word'] = context[x + 1]['Word']
            groupcontext[z]['Confidence'] = context[x + 1]['Confidence']
            groupcontext[z]['Top'] = context[x + 1]['Top']
            groupcontext[z]['Right'] = context[x + 1]['Right']
            groupcontext[z]['Bottom'] = context[x + 1]['Bottom']

        else:
            z = z + 1
            groupcontext[z] = {}
            groupcontext[z]['Value'] = context[x + 1]['Value']
            groupcontext[z]['Word'] = context[x + 1]['Word']
            groupcontext[z]['Candidates'] = context[x + 1]['Candidates']
            groupcontext[z]['Weight'] = '0'
            groupcontext[z]['Confidence'] = context[x + 1]['Confidence']
            groupcontext[z]['Left'] = context[x + 1]['Left']
            groupcontext[z]['Top'] = context[x + 1]['Top']
            groupcontext[z]['Right'] = context[x + 1]['Right']
            groupcontext[z]['Bottom'] = context[x + 1]['Bottom']
            groupcontext[z]['SameLine'] = context[x + 1]['SameLine']
```

### Score Context

After grouping the context, using the context values provided by
the user, we will score each grouping based on how strongly it matches 
the context values. We utilize a fuzzy algorithm that allows us to accommodate
for any OCR errors or misspellings. The weight given to each context word is also
judged based on the weighted value provided by the user. This gives the ability for
the user to define which context words should carry more weight in the scoring
algorithm. For grouped context that fall within the same line as the candidate, the user
can define a value to be added to the overall weight. 

Score Context:

```python
def weightcontext(self, KW_ATT):
    # Match Context and Weighting

    for z, value in KW_ATT.items():

        for x in range(len(groupcontext)):

            groupcontext[x + 1]['Weight'] = 0

            if int(groupcontext[x + 1]['Weight']) < fuzz.WRatio(groupcontext[x + 1]['Value'], z):
                groupcontext[x + 1]['Weight'] = float(fuzz.WRatio(groupcontext[x + 1]['Value'], z)) * float(
                    value[0]) / 100

                if groupcontext[x + 1]['SameLine'] == '1':
                    groupcontext[x + 1]['Weight'] = groupcontext[x + 1]['Weight'] + float(value[5])
```

### Output Result

Outputting a resulting text file with the winning candidate as well as
the entire results array. The text file name will be the same as the input 
image file.

```python
 def outputresults(self, groupcontext, fp):
    # Output Results
    for x in range(len(groupcontext)):

        if groupcontext[x + 1]['Candidates'] in results:

            if int(results[groupcontext[x + 1]['Candidates']]) < int(groupcontext[x + 1]['Weight']):
                results[groupcontext[x + 1]['Candidates']] = groupcontext[x + 1]['Weight']

        else:
            results[groupcontext[x + 1]['Candidates']] = groupcontext[x + 1]['Weight']

    if (len(results.keys()) == 0):

        f = open(fp + '.txt', 'w')
        f.write("Could not find any valid candidates")
        f.close()

    else:
        sorted_by_value = sorted(results.items(), key=lambda kv: kv[1], reverse=True)
        f = open(fp + '.txt', 'w')
        f.write("WINNING CANDIDATE (CANDIDATE , WEIGHT): " + str(sorted_by_value[0]) + "\n")
        f.write("ALL CANDIDATES: " + str(sorted_by_value))
        f.close()

```

## Example

:o: unclear, why not provide also an instalation section with requirements.txt

## Tools and Technology

The tools and technology deployed for this project are going to be covered in 
this section.

### Terresact

Python-tesseract is an optical character recognition (OCR) tool for python.
That is, it will recognize and “read” the text embedded in images. Python-tesseract 
is a wrapper for Google’s Tesseract-OCR Engine[@hid-sp18-414-www-pytesseract].

Code Example:

```python
import pytesseract
hocr = pytesseract.image_to_pdf_or_hocr('test.png', extension='hocr')
```

Install:

```bash
$ pip install pytesseract
```

### Beautiful Soup

Beautiful Soup is a library that makes it easy to scrape information from web pages.
It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching,
and modifying the parse tree[@hid-sp18-414-www-beautifulsoup].

Code Example:

```python
import bs4
soup = bs4.BeautifulSoup(DATA, 'html.parser')
words = soup.find_all('span', class_='ocrx_word')
```

Install:

```python
$ pip install beautifulsoup4
```

### FuzzyWuzzy

Fuzzy Wuzzy provides fuzzy string matching in an easy to use package.
It uses Levenshtein Distance to calculate the differences between sequences
in a simple-to-use package[@hid-sp18-414-www-fuzzywuzzy].

Code Example:

```python
from fuzzywuzzy import fuzz
fuzz.ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear")

Output:91

```
Install:
```bash
$ pip install fuzzywuzzy
```

### Python

Python is the high-level programming language that was used to develop
this project.

### Numpy

NumPy is the fundamental package for scientific computing with Python[#hid-sp18-414-www-NumPy].

Code Example:

```python
import numpy as np
core = np.ones((1, 1), np.uint8)
```

Install:

```python
$ pip install Numpy
```

### OpenCV

OpenCV (Open Source Computer Vision Library) is released under a BSD license and hence it’s
free for both academic and commercial use. It has C++, Python and Java interfaces and
supports Windows, Linux, Mac OS, iOS and Android. OpenCV was designed for computational 
efficiency and with a strong focus on real-time applications[@hid-sp18-414-www-OpenCV].

Code Example:

```python
import cv2
img = cv2.imread('messi5.jpg',0)
```

Install:

```bash
$ pip install opencv-python
```

### Python Imaging Library

The Python Imaging Library adds image processing capabilities 
to your Python interpreter. This library provides extensive file 
format support, an efficient internal representation, and fairly 
powerful image processing capabilities[@hid-sp18-414-www-Pillow].

Code Example:

```python
from PIL import Image as IMG
image = IMG.open(path)
```

Install:

```bash
$ pip install Pillow
```

### Tkinter

Tkinter is Python's a standard GUI (Graphical User Interface) package.
It is a thin object-oriented layer on top of Tcl/Tk[@hid-sp18-414-www-tkInter].

Install:

```bash
$ pip install Tkinter
```

## Conclusion

:o: missing

## Acknowledgement

The authors would like to thank the Big Data Applications and 
Analytics (I-523) course teaching staff, mainly professor 
Gregor von Laszewski for their support and guidance during 
this project.
