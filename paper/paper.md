# OCR Technology Overview :hand: fa18-523-88

| Joao Paulo Leite
| jleite@iu.edu
| Indiana University
| hid: fa18-523-88
| github: [:cloud:](https://github.com/cloudmesh-community/fa18-523-88/blob/master/paper/paper.md)

---

Keywords: fa18-523-88,  OCR, Optical Character Recognition, Computer Vision
          
---

## Abstract

Optical Character Recognition (OCR) technology first appeared in the 1940's and grew alongside the 
rise of the digital computer. It was not until the late 1950's when OCR machines became commercially 
available and today this technology presents itself in both hardware devices as well as software offerings. 
Optical Character Recognition (OCR) was created as a way to transform text from a document into machine 
encode text. At a high level, an OCR system works by locating and segmenting each character, running 
the segmented character through a pre-processor for normalization and noise reduction, and extracting 
critical features to assist in the classification of each character. Once each character has been 
classified, the characters are regrouped and contextual information is applied to assist in word construction 
and to detect potential character misclassifications. While OCR technology has continued to evolve over 
the years into the realms of handwriting recognition, known as Intelligent Character Recognition (ICR), 
the main problem with these systems have been around degraded characters, which are incorrectly fragmented 
or joined characters, which causes issues during the segmentation process. OCR technology has far-reaching 
applications and is typically the first step when attempting to provide automation to document-centric 
processes such as image classification and data entry/indexing. 

## Introduction

The main principle in Optical Character Recognition (OCR) is to automatically recognize character patterns. 
This is accomplished by showing the system each class of pattern that can occur and providing a training set 
for each pattern. At the time of recognition, the system uses the previously provided examples to classify the 
new character to the closest match. Typical, OCR system are designed to solely transform text on a document into 
machine-encoded text and additional systems must be built to further extract relevant information from the document. 
That is to say, the process of OCR is the first step in transforming structured, semi-structured and unstructured 
documents into valuable and relevant information.


## Optical Character Recognition

As stated in the name Optical Character Recognition, the characters that are typically trained are letters, numbers 
and special symbols. Each differing character is defined as its own class, and the system builds an understanding of 
each class utilizing examples of characters provided. The steps that are typically performed by an OCR system are 
threshold processing, character segmentation, character preprocessing, feature extraction, classification and post 
processing. 

### Threshold Processing

At its core, the OCR process expects to process a black character presented against a white background. While images 
coming into an OCR system could have already undergone this transformation from color image into a black and white image 
via a scanner, it is beneficial to perform this step before passing the image into the OCR engine to provide the highest 
level quality to the OCR engines. The mechanism behind this conversion analyzes each pixel to determine if it should be 
assigned as a black or white pixel. For color images, this thresholding can be set at a fixed level so that any faintly 
colored pixels can be dropped as white while truly dark colored pixels are converted to black. In the case of 
grayscale images, the same threshold can be set with the difference being the shades of gray presented in each 
pixel. Once this process is complete, the newly created black and white images are used for the remainder of the 
process[@fa18-523-88-www-imagethresholding].

### Character Segmentation

Character segmentation is a critical step in the process which represents breaking the image down into logical segments. 
While the system can be designed to segment the image into words, typically OCR is most successful if it is segmented to 
the lowest common denominator, the character. Each character is defined as a contiguously connected set of pixels and a 
break in the connection constitutes the beginning of a new character. While this may sound like a straightforward process, 
problems can occur when characters are fragmented or touching. Character distortions due to image quality issues or ‘serifed’ 
fonts are the main culprits behind fragmented or touching characters, while noise such as marks, handwriting and dots can 
also contribute to challenges when attempting to segment characters. To alleviate this issue, before the characters are 
presented to the feature extraction phase in the process, the characters are run through the preprocessing phase in an 
attempt to correct some of the issues that may have manifested themselves[@fa18-523-88-www-eikvilocr].

### Character Preprocessing

Character Preprocessing is a vital step used to clean up common defects introduced during the previous scanning or thresholding 
steps. The goal of preprocessing is to remove the faults that can later cause poor character recognition in the subsequent steps.

To combat these defects, the preprocessor employs a common technique called smoothing. Smoothing serves to both fill in gaps 
within a character (fragmentation correction) as well as thin the width of lines within a character (touching correction). 
When properly applied, smoothing is successful in filling in pits and removing bumps from characters, which will increase the 
likelihood of recognition in the following steps[@fa18-523-88-www-eikvilocr]. The preprocessor also invokes tasks for
noise removal and character normalization. The noise removal task removes of specks, thin lines and other inconsistencies 
through the analysis of height, size and density of a grouping of pixels. If the characteristics of a particular grouping 
is not consistent with the characteristics found for a typical character, the grouping is deemed noise and removed as such. 
The normalization of characters is applied to provide a uniformly sized and oriented character, fixing issues around scaling,
slanting and rotation of characters. With the character preprocessing completed, OCR is ready for feature extraction.


### Feature Extraction

The most simplistic extraction technique is known as template matching. The technique does not use feature analysis and 
will only compare the input character against a known set of characters provided for each class at a pixel level. The distance
between the inputted character and the set of known characters is calculated for each class. Once that comparison is completed,
the class with lowest distance is assigned as the class for the input character. However, the set-back of this method is that 
it does not afford any flexibility around noise or font variations that have not yet been assigned[@fa18-523-88-www-eikvilocr].

Because of rigidity of the template matching technique, feature based techniques were later developed to extract significant 
features from a character. Some common feature extraction methods are zoning, distance profiling, and directional distribution 
analysis[@fa18-523-88-www-imagethresholding].

#### Zoning

Zoning is a technique that frames the character in a set of overlapping or non-overlapping zones. The pixel density in each 
zone must be calculated by taking the number of black pixels in the zone divided by the total number of pixels presented in 
the zone. The resulting ratio for each zone becomes the feature that describes the character.

#### Distance Profiling

Distance profiling is a technique that frames the character in a bounding box. The distance from the bounding box to the outer 
edge of the character is calculated for each of the four side (top, bottom, left and right). The resulting calculated distance 
becomes the feature that describes the character.

#### Directional Distribution
Directional distribution analysis is a technique that assigned a center point to the character. Once the center point is 
assigned, the weight is calculated by taking the number of black pixels found in each direction divided by the total number 
of pixels found in the character. The resulting ratio for each direction becomes the feature that describes the character.

Because these techniques are independent, there are possibilities to combine multiple features to increase the 
accuracy of recognition. 

### Classification

The classification step is the culmination of all the previous steps to obtain the desired result of assigning 
a character to the correct class. One such classification method that could be used is K- Nearest Neighbor.The K-Nearest 
Neighbor (KNN) provides a method to classify characters based on the closest features extracted in the training set. Typically 
regarded as a simple machine learning algorithm, KNN calculates the Euclidean distance between features value of the input 
character against the features value of the characters in the training set. Once the distance is calculated, the results 
are arranged in order and the input character is assigned the character class that corresponds to the majority of its 
nearest neighbors[@fa18-523-88-www-imagethresholding].

### Post Processing

#### Grouping

Once all the individual characters have been successfully classified, the system can begin to group those set of characters 
into the next level of association. Grouping characters into logical strings of words, numbers or tokens is an easy task of 
considering the location of each individual character and evaluating the pixel distance (white space) to the next individual 
character. With machine printed text, the assumption is that distances between words are far greater than distances between 
characters within a word. Once grouping is complete, the system is able to leverage the newly formed words to provide error 
detection and logical character correction.

#### Error-Detection

Because individual character recognition will never be 100 percent accurate, we can utilize the context around our newly formed 
words from the grouping phase to increase the accuracy and detect errors around the recognition. This secondary evaluation process 
will be based on the systems understanding of the underlying language for which the text is written in.

#### Language Syntax

One form to evaluate the accuracy is to use the syntax of the language and rule out specific combinations of characters appearing in 
sequence. As an example, if the recognition for the three-letter word "cut" came back as "cwt", the system would understand that the 
syntax of a C followed by a W and a W followed by a T is highly improbable in the English language and flag this a potential error
[@hid-fa18-88-www-eikvilocr]. 

#### Dictionaries

Another evaluation method that can assist with the accuracy is a dictionary lookup. Following the logic of the example above, after 
understanding that we have mistakenly extracted "cwt", we can apply dictionaries to assist in correcting the error that was 
caused by the individual character recognition engine. Because "w" and "u" share some common characteristics, the original 
classification can be utilized to not only provide the highest matching character but also consider which matching characters 
provides the highest probability of forming a word that matches an entry in the dictionary[@hid-fa18-88-www-eikvilocr]. 

### Conclusion

As the evolution of Optical Character Recognition systems continue to evolve, new techniques may be developed to increase the
accuracy of such systems. With that said, the overall structure and process of these new systems will follow what has been outlined and 
discussed in this paper. This is especially true in the more challenging arena of handwritten recognition, where systems based on 
neural networks have begun to emerge in recent years.
