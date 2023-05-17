# Python environment with a requirements.txt

The `requirements.txt` file should list all Python libraries that your notebooks
depend on, and they will be installed using:

```
pip install -r requirements.txt
```
---


## How to run?

You have 2 options:
1. python main.py webcam ROI_number
2. python main.py video ROI_number PATH_of_video

\
Notice that:
* You need to choose 'webcam' or 'video'
* ROI_number must be in range of [1-5]
* PATH_of_video must be the full path of a file
\


### Example:
\
<img src="https://user-images.githubusercontent.com/79280930/127553271-2fa20129-371e-41b5-ac8d-39bd3400b70b.png">

*******************************************************************
# HR-from-RGB
# Integration between open source codes
# Einat Lasry & Yaniv Shnur, Under the direction of Hagit Hel Or, Haifa University 08/2021

The purpose of the project is to extract a pulse from RGB videos.
There are a lot of open-source codes that extract a pulse from videos.
Our goal was to find some such codes, compare performance, and finally use them to generate a "winning" code with good results.

# Background
Heart Rate (HR) is one of the most important Physiological parameter and a vital indicator of people‘s physiological state.
A non-contact based system to measure Heart Rate: real-time application using camera.
Principal: Extract heart rate information from facial skin color variation caused by blood circulation.

# The process of finding the pulse from a RGB video:
![FlowChart](https://github.com/EinatLasry/HR-from-RGB/assets/82314695/a9a521b6-20e0-4ce8-84ef-d82a9194056c)

# Approaches:
After locating the face using a face-detection algorithm, each code uses a different ROI on the face of the person.
We have noticed that there are pros and cons to each approach.

Face in Rectangle:
Pros: All facial areas are reflected in the HR calculation.
Cons: Included noise in the HR calculation (background, hair, mouth, eyes, glasses, etc.)

Face Segmentation:
Pros: Removing the background outside, using several areas on the face.
Cons: Included in the HR calculation eyes, mouth and other areas from which we do not want to infer information about HR.
In addition, the forehead is not included in the calculation.

Use of a specific facial area (forehead, left or right cheek):
Pros: Everything included in the ROI is relevant to the HR calculation.
Cons: There are relevant areas that are not included in the calculation.
In addition, if that person has a pony for example, calculating the forehead will not work for him.

# Solution:
For each video, we extracted HR from 5 different ROI's:
* ROI1 - Left Cheek – YELLOW
* ROI2 - Right Cheek – GREEN
* ROI3 - Forehead – BLUE
* ROI4 - Face in Rectangle – WHITE
* ROI5 - Face Segmentation – CYAN
* 
![ROIS_EINAT](https://github.com/EinatLasry/HR-from-RGB/assets/82314695/60858dad-32c1-4acb-b442-0cb6e30a22f7)

Next, we tested on a large number of challenging videos ("training"),
how we will get the best results, by weighting the different results for that video.
In the first step we calculated the errors of each ROI,
and we concluded which ROI should be given greater weight.

The weight vectors are:
* Vector_1 = 0.06*ROI1 + 0.08*ROI2 + 0.06*ROI3 + 0.4*ROI4 + 0.4*ROI5
* Vector_2 = 0.2*ROI1 + 0.2*ROI2 + 0.2*ROI3 + 0.2*ROI2 + 0.2*ROI5
* Vector_3 = 0.05*ROI1 + 0.2*ROI2 + 0.05*ROI3 + 0.35*ROI4 + 0.35*ROI5
* Vector_4 = 0.1*ROI1 + 0.2*ROI2 + 0.1*ROI3 + 0.3*ROI4 + 0.3*ROI5
* Vector_5 = 0.15*ROI1 + 0.2*ROI2 + 0.15*ROI3 + 0.25*ROI4 + 0.25*ROI5
* Vector_6 = 0.18*ROI1 + 0.2*ROI2 + 0.18*ROI3 + 0.22*ROI4 + 0.22*ROI5

# Results
You can see in the table the results of our code (with the weight-vector selected) compared to the results of the competition.
https://arxiv.org/pdf/2003.11756.pdf

We were surprised that it is precisely the equal weight vector that brings the best results.
It can be concluded that in a test on large and varied data, there were advantages and disadvantages to each method,
and therefore their combination resulted in a better result from each method individually.
Our recommendation for the continuation of the project:
run an algorithm to identify interfering factors (e.g. pony, beard, glasses) and then re-examine the weight vectors.

![image](https://github.com/EinatLasry/HR-from-RGB/assets/82314695/2c1c0665-f103-4613-818c-ca45812f0c7d)
![image](https://github.com/EinatLasry/HR-from-RGB/assets/82314695/c877cef4-e480-419a-a1ec-3aaa139b7f95)
![image](https://github.com/EinatLasry/HR-from-RGB/assets/82314695/c2e8b207-7f54-4dcc-8f1b-b3590a734530)

# Source codes:
FILL
