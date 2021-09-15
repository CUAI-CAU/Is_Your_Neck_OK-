# Advisor for VDT: A Study on the Prevention of Incorrect Sitting Posture and Eye Dryness by Using Frontal Images [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FCUAI-CAU%2FIs_Your_Neck_OK-&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

[Paper](https://drive.google.com/file/d/1RAxAUGAC_okJ7tXQWkRe5mHfNC7nVdcs/view?usp=sharing) | [Poster](https://drive.google.com/file/d/1tpvUc9PQ5YgTljxyEAmA1LQbahQdIV66/view?usp=sharing) | [Project](https://drive.google.com/file/d/1V2NKEeIwxjkrew77IdaMgwsFWY_Eqowb/view?usp=sharing) | [Presentation](https://www.youtube.com/watch?v=MIXmdktvD-4) | [Demo](https://drive.google.com/file/d/1Ffyi54A5QsdlJta3sYhBqTVU_O0GHTVq/view?usp=sharing)

**This repository contains source codes which used for "Summer Project for CUAI 4th Conference".**

Paper, Poster and Presentation are in Korean.


## Our Team
- Yoosun Kim (School of Mechanical Engineering, Chung-Ang Univ.)
- Jimin Kim (School of Computer Science & Engineering, Chung-Ang Univ.)
- Byunghyun Bae (School of Pharmaceutics, Chung-Ang Univ.)
- Hayun Lee (School of Computer Science & Engineering, Chung-Ang Univ.)

## Application

![application00](https://user-images.githubusercontent.com/87100682/131342705-6c3c2898-0d9a-4ca0-a870-6c88cfdd368e.jpg)


## CNN Model Selection to classify forward head posture

Selecting the best model, our team tested 4 cnn algorithems(ResNet, GoogLeNet, EfficientNet, ShuffleNet). And the graph of the test-accuracy showed up as the following left fig. After comparing the accuracy for each model, ResNet18 with the best performance was selected. The increasing accuracy of ResNet18 in the learning/testing process can be seen in the right fig.  

![005](https://user-images.githubusercontent.com/87100682/131344931-a3f06737-d7b5-4a8e-a973-91bb3be5627e.jpg)


## System Flow

This program is purposed to analyze the user’s degree of VDT syndrome and show several factors to make the user recognize the computer using environment.

![application01](https://user-images.githubusercontent.com/87100682/131342794-3b844fb7-f092-4f48-a0d8-3a5f4dd19f9a.jpg)

This is followed by the upward process.
In addition, this is done by injecting images to the already trained model.


## Full System Explanation

This system is composed of ***4 steps***.

### **At first**
your camera will take your record for 3 minutes and each 3 seconds, your picture will be made. In this process, your eye blink will be counted.

### **Secondly**
you will get your most crooked image and degree among your recorded pictures.
Applying Keypoint-R-CNN, the nose location and side shoulder location will be extracted. Using this information, we can find how much your shoulder is tilted and your face is biased from the center.

### **Thirdly**
the pre-trained ResNet18 will predict your recorded pictures and return the count of the number of turtle necks and vice versa. It will also return a picture with the highest possible turtle neck.

### **Finally** 
you will get your "Out Body" result by your recorded pictures.


## Code

### 1. Install Dependencies 

Before running this program, please create a virtual environment by running the code below for a better execution environment. Then, run the code below to install the necessary tools.

```python
$ conda create -n VDT_Advisor python=3.8
$ conda activate VDT_Advisor
$ pip install -r requirements.txt
```
This code was tested with `python 3.8.3`, `torch 1.9.0`  
**Please note :** Your system must have `C++` processing program.

### 2. Record User’s Posture and Count Eye Blinking

 During recording, The program will extract frames and count your eye blinking for eye dryness. Just run (It will last 3 minutes)
```python
$ python frame_extract_with_cnt_blinked.py
```
**Please note :** In order to get a good result, your shoulders must be clearly visible during recording. Also, don't let accessories like mask cover your face.

### 3. Detect User’s Asymmetry

To detect your asymmetry, run
```python
$ python detect_asymmetry.py
```
This will automatically examine your shoulder asymmetry and crooked posture.

### 4. Detect User’s Turtle Neck Syndrome (Forward Head Posture)

If you want to know how much you’re at risk for turtle neck syndrome(Forward Head Posture), please run
```python
$ python Neck_Code.py
```
This will automatically examine your turtle neck posture.

### 5. Check Result

All the examinations are complete!
By running the code below, print out your postural analysis result. Result paper will be written in Korean.
```python
$ python make_reult.py
```
**Remember** : This result doesn't tell you everything about your posture. Don’t be too disappointed even though you get a worse result than you expected.  If you keep trying, then you can get more improved **“OutBody”** in the future.


## Reference

He, Kaiming, et al. "Deep residual learning for image recognition." Proceedings of the IEEE conference on computer vision and pattern recognition. 2016.

