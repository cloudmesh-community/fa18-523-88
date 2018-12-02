# OCR Technology Overview :hand: fa18-523-88

| Joao Paulo Leite
| jleite@iu.edu
| Indiana University
| hid: fa18-523-88
| github: [:cloud:]()
| code: [:cloud:]()

---

Keywords: fa18-523-88,  OCR, Optical Character Recognition, Computer Vision
          
---

## Abstract
Optical Character Recognition (OCR) technology first appeared in the 1940's 
and grew alongside the rise of the digital computer. It was not until the late 
1950's when OCR machines became commercially available and today this technology 
presents itself in both hardware devices as well as software offerings. At a 
high level, an OCR system consists of locating and segmenting each character, 
running the segmented character thru a pre-processor for normalization and noise 
reduction and extracting critical features to assist in the classification of each 
character. Once each character has been classified, the characters are regrouped and 
contextual information can be applied to assist in word construction and to detect 
potential character mis-classifcations. While OCR technology has continued to evolve 
over the years into the realms of handwriting recognition, known as Intelligent 
Character Recognition (ICR), the main issue with these systems have been around degraded 
characters, which are incorrectly fragmented or joined, which causes issues during 
the segmentation process. OCR technology has far-reaching applications and is typically 
the first step when attempting to provide automation to document-centric processes such 
as image classification and data entry/indexing. 

## Introduction

The main principle in Optical Character Recognition (OCR) is to automatically recognize 
character patterns. This is done by teaching the system each class of pattern that can 
occur and providing a set of examples for each pattern. At the time of recognition, the 
system performs a comparison between the unknown character provided and the previously 
provided examples, assigned the appropriate class to the closest match. This system is 
designed to solely transform text on a document into machine encoded text and additional 
systems must be built to further extract relevant information from the document, that is 
to say, the process of OCR is the first step in transforming structured,semi-structured 
and unstructured documents into valuable and relevant information.


## Optical Character Recognition

As stated in the name Optical Character Recognition, the characters that are typically trained 
are letter, numbers and special symbols. Each differing character is defined as its own class, 
and the system builds an understanding of each class utilizing examples of characters provided. 
The steps that will be performed are threshold processing, character segmentation, character 
preprocessing, feature extraction, classifcation and post processing. 

### Threshold Processing

At it's core, the OCR process expects to process a black character which is presented against 
a white background. While images coming into an OCR system could have already undergone this 
transfromation from color image into a black and white image via a scanner, it is beneficial to 
perform this thersholding step before passing the image into the OCR engine to provide the high 
level image quality to the OCR engines. The mechanism behind this conversion is to analyse each 
pixel on the page to determine if it should be assigned as a black or white pixel. For color images 
that are on the RGB scale, this thresholding can be set at a fixed level so that any faintly colored
pixels can be dropped as white while truly dark colored pixels are converted to black. In the case 
of grayscaled images, the same threshold can be set with the difference being the level of greyness
presented in each pixel. Once this proccess is complete, the newly created black and white images will 
be used for the remainder of the process moving forward[@hid-sp18-414-www-imagethresholding].

### Character Segmentation

Character segmentation is a critical step in the process which represents breaking the image down 
into logical segments. While the system can be designed to segment the image into words, typically 
OCR is most successful if it is segmented to the lowest common denominator, the character. Each character 
is defined as a contiguously connected set of pixels and a break in the connection constitutes the 
beginning of a new character. While this may sound like a straightforward process, problems can occur 
when characters are fragmented or touching. Character distortions due to image quality issues or serifed
font fonts are the main culprits behind fragmented or touching characters, while noise such as marks, 
handwriting and dots can also contribute to challenges when attempting to segment characters. To alleviate 
this issue, before the characters are presented to the feature extraction phase in the process, the 
characters are run thru the preprocessing phase in an attempt to correct some of the issues that may 
have manifested themselves[@hid-sp18-414-www-eikvilocr].

### Character Preprocessing

Character Preprocessing is a vital step that occurs before the extraction/classification, with the goal 
being to provide the best quality character to subsequent steps. A certain amount of character defects can 
be introduced during the scan process as well as the thresholding step, which can later cause poor character 
level recognition rates.

To combat these defects, a preprocessor is employed to attempt to correct these issues and a common 
technique is called smoothing. Smoothing serves to both fill in gaps within a character (fragmentation 
correction) as well as thin the width of lines within a character (touching correction). When properly 
applied, smoothing is successful in filling in pits within a character and removing bumps from a character, 
which will increase the likelihood of recognition in the following steps[@hid-sp18-414-www-eikvilocr]. 
Removing noise and normalization of the character are also considered tasks, which will be resolved by the 
preprocessor. The removal of specks, thin lines and other inconsistency are resolved thru the analysis of the 
height, size and density of a grouping of pixels. If the characteristics of a particular grouping is not 
consistent with the characteristics found for a typical character, the grouping is deemed noised and removed 
as such. The normalization of characters is applied to provide a uniformly sized and oriented character, fixing 
issues around scaling, slanting and rotation of characters. 

### Feature Extraction

The simplest extraction technique, template matching, foregoes feature analysis and will only compare the 
inputted character against a known set of characters provided for each class. The distance between the inputted 
character and the set of known characters is computed for each class. Once that comparison is completed, the 
class with lowest distance is assigned as the class for the inputted character. While this method is simple, 
the simplicity does not afford any flexibility around noise or font variations, which have not been assigned. 

Because of rigidity of the template matching technique, feature based techniques were developed to extract 
significant features from a character. Some common feature extraction methods are zoning, distance profiling 
and directional distribution analysis[@hid-sp18-414-www-featureextraction].

#### Zoning
Zoning is a technique that frames the character in a set of overlapping or non-overlapping zones. The pixel 
density in each zone must be calculated by taking the number of black pixels in the zone divided by the total 
number of pixels presented in the zone.

#### Distance Profiling
Distance profiling is a technique that frames the character in a bounding box. The distance from the bounding 
box to the outer edge of the character is calculated for each of the four side (top, bottom, left and right).

#### Directional Distribution
Directional distribution analysis is a technique that assigned a center point to the character. Once the center 
point is assigned, the weight is calculated by taking the number of black pixels found in each direction divided 
by the total number of pixels found in the character.

Because these techniques are independent, there are possibilities to combine multiple features to increase the 
accuracy of recognition. 

### Classification

The classification step is the culmination of all the previous steps to obtain the desired result of assigning 
a character to the correct class. One such classification method that could be used is K- Nearest Neighbor.The K-Nearest 
Neighbor (k-NN) provides a method to classify characters based on the closest features extracted in the training examples. 
Typically regarded as a simple machine learning algorithm, k-NN calculates the Euclidean distance between features 
value of the inputted character against the features value of the characters provided by the training examples. Once 
the distance is calculated, the results are arranged in order and the input character is assigned the character class 
that corresponds to the majority of its nearest neighbors[@hid-sp18-414-www-featureextraction].


### Post Processing

#### Grouping
Once all the individual characters have been successfully classified, the system can begin to group those set of characters 
into the next level of association. Grouping characters into logical strings of words, numbers or tokens is an easy task of 
considering the location of each individual character and evaluating the pixel distance (white space) to the next individual 
character. With machine printed text, the assumption is that distances between words are far greater than distances between 
characters within a word. 

#### Error-Detection

Because individual character recognition will never be 100 percent accurate, we can utilize the context around our newly formed 
words from the grouping phase to increase the accuracy and detect errors around the recognition. This secondary evaluation process 
will be based on the systems understanding of the underlying language for which the text is written in.

#### Language Syntax
One form to evaluate the accuracy is to use the syntax of the language and rule out specific combinations of characters appearing in 
sequence. As an example, if the recognition for the three-letter word "cut" came back as "cwt", the system would understand that the 
syntax of a C followed by a W and a W followed by a T is highly improbable in the English language and flag this a potential error
[@hid-sp18-414-www-eikvilocr]. 

#### Dictionaries
Another evaluation method that can assist with the accuracy is a dictionary lookup. Following the logic of the example above, after 
understanding that we have mistakenly extracted "cwt", we can apply dictionaries to assist in correcting the error that was 
caused by the individual character recognition engine. Because "w" and "u" share some common characteristics, the original 
classification can be utilized to not only provide the highest matching character but also consider which matching characters 
provides the highest probability of forming a word that matches an entry in the dictionary[@hid-sp18-414-www-eikvilocr]. 

### Conclusion
