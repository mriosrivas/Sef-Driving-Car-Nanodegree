
# **Behavioral Cloning** 

## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Behavioral Cloning Project**

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build, a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report


[//]: # (Image References)

[image1]: ./examples/architecture.png "Model Visualization"
[image2]: ./examples/udacity_data.jpg "Udacity Data"
[image3]: ./examples/left_recovery.jpg "Recovery Image"
[image4]: ./examples/right_recovery.jpg "Recovery Image"
[image5]: ./examples/original.jpg "Original Image"
[image6]: ./examples/mirrored.jpg "Mirrored Image"
[image7]: ./examples/not_crop.jpg "Original Image"
[image8]: ./examples/crop.jpg "Cropped Image"

## Rubric PointsSoftmatrix
### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/432/view) individually and describe how I addressed each point in my implementation.  

---
### Files Submitted & Code Quality

#### 1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
* model.h5 containing a trained convolution neural network 
* writeup_report.md or writeup_report.pdf summarizing the results

#### 2. Submission includes functional code
Using the Udacity provided simulator and my drive.py file, the car can be driven autonomously around the track by executing 
```sh
python drive.py model.h5
```

#### 3. Submission code is usable and readable

The model.py file contains the code for training and saving the convolution neural network. The file shows the pipeline I used for training and validating the model, and it contains comments to explain how the code works.

### Model Architecture and Training Strategy

#### 1. An appropriate model architecture has been employed

My model consist of an implementation of the NVidia CNN Architecture (model.py lines 85-133).

The model uses RELU layers on all Convolutional Networks to indroduce nonlinearity. Data is normalized using a Keras Lambda Layer (line 89)

Since this is a regression problem no Softmatrix is used.

#### 2. Attempts to reduce overfitting in the model

The model contains maxpooling layers after each convolutional network in order to reduce overfitting (model.py lines 85-133). 

The model was trained and validated on different data sets. These data setes were chosen to be randmoly selected. All data was implemented by using generator functions to reduce computer overhead (lines 17-71). 

The model was tested by running it through the simulator and ensuring that the vehicle could stay on the track.

#### 3. Model parameter tuning

The model used an adam optimizer, so the learning rate was not tuned manually (model.py line 137).

#### 4. Appropriate training data

Training data consists of three parts:

1. Data given by Udacity.
2. Data collected using the simulator.
3. Data selection.

By just using all of Udacity data (left, right and center images) I couldn't prevent the car from going outside the track, so I also captured some extra data on turns that helped the car to stay on track. There is also a classification on which data to use. In this case only 40% of the images that had a steering value of zero were kept, since more data was redundant.


### Model Architecture and Training Strategy

#### 1. Solution Design Approach

The way I was able to solve this problems was by first implementing the NVidia CNN Architecture. On my first attempt I introduced RELU layers on both the Convolutional Networks and on the Fully Connected Layers. The results of this implementation seemed to work, but eventually the car went outside the track.

I thought that the car may be going outside the track because the Fully Connected Layers didn't need to have a nonlinear output. The results improved a lot, but the car was still going outside the track.

After that, by getting some extra data (specially on turns) I was able to get a fully working self diving implementation.

Due to the amout of data, I used an AWS instance to run my model. Function generators provided to be very useful when data is big on size and quantity.

After finishing this project, I realized that data selection is a very important topic, and if a good data set is feeded to our model, it can be more robust than one with poor data selection.

#### 2. Final Model Architecture

This architecture is based on the following parts:

1. Convolutional Network with 5x5 kernel and depth of 24
2. Convolutional Network with 5x5 kernel and depth of 36
3. Convolutional Network with 5x5 kernel and depth of 48
4. Convolutional Network with 3x3 kernel and depth of 64
5. Convolutional Network with 3x3 kernel and depth of 64
6. Flatten Layer
7. Fully Connected Layer of 100
8. Fully Connected Layer of 50
9. Fully Connected Layer of 10
10. Fully Connected Layer of a single neuron

Here is a visualization of the architecture.

![alt text][image1]

#### 3. Creation of the Training Set & Training Process

I had some problems using the simulator, so it was hard for me to drive the car. So instead of driving and recording a complete lap, I used the Udacity data set as my starting point. Below is an image of this data set:

![alt text][image2]

I recorded the car driving from the left and right sides and moving towards the center so I could teach the car how to recover from this kind of circumstances. Below there are some images:

![alt text][image3]
![alt text][image4]

To augment the data set, I also flipped images and angles as it was suggested on the project lecture. This data set was like driving on a different road since everything was mirrored.

![alt text][image5]
![alt text][image6]


After the collection process, I had around 7000 images. From this number of images I discarded around 3500 that had a steering angle of zero.

I then preprocessed the data by cropping and reducing the original size of 160x320 to 66x320 to take from the image things like trees, sky and the car itself. Below there is an original and a cropped image:


![alt text][image7]
![alt text][image8]


The data was also randomly shuffled with 20% of the data into a validation set. 

For the model a number of 3 epochs was used with a batch size of 32. An Adam optimizer and mean square error optimization for the regression model was also implemented.

