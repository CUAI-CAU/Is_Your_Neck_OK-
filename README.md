# Advisor for VDT: A Study on the Prevention of Incorrect Sitting Posture and Eye Dryness by Using Frontal Images

[Paper]() | [Poster]() | [Project]() | [Presentation]() | [Demo](https://drive.google.com/file/d/1Ffyi54A5QsdlJta3sYhBqTVU_O0GHTVq/view?usp=sharing)


**This repository contains source codes which used for "Summer Project for CUAI 4th Conference".**

Paper, Poster and Presentation are in Korean.

## Our Team
- Yoosun Kim (School of Mechanical Engineering, Chung-Ang Univ.)
- Jimin Kim (School of Computer Science & Engineering, Chung-Ang Univ.)
- Byunghyun Bae (School of Pharmaceutics, Chung-Ang Univ.)
- Hayun Lee (School of Computer Science & Engineering, Chung-Ang Univ.)

## Applications

## System

## Code

### 1. Install Dependencies 

Before running this program, please run the code below to install the necessary tools.
```python
python -m pip install -r requirements.txt
```
This code was tested with python 3.x.x, torch 1.xx   
**Please note :** Your system must have C++ processing program.


### 2. Record User’s Posture and Count Eye Blinking

 During recording, The program will extract frames and count your eye blinking for eye dryness. Just run
```python
python frame_extract_with_cnt_blinked.py
```
**Please note :** In order to get a good result, your shoulders must be clearly visible during recording. Otherwise, you may get a wrong analysis result about your posture.    


### 3. Detect User’s Asymmetry

To detect your asymmetry, run
```python
python detect_asymmetry.py
```
This will automatically examine your shoulder asymmetry and crooked posture.  


### 4. Detect User’s Turtle Neck Syndrome

If you want to know how much you’re at risk for turtle neck syndrome, please run
```python
python Neck_Code.py
```
This will automatically examine your turtle neck posture.  


### 5. Check Result

All the examinations are complete! 
By running the code below, print out your postural analysis result. 
```python
python make_reult.py
```
**Remember** : This result doesn't tell you everything about your posture. Don’t be too disappointed even though you get a worse result than you expected.  If you keep trying, then you can get more improved **“OutBody”** in the future.



## Reference

