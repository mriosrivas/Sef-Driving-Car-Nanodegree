
## CarND Vehicle Detection
---

**Vehicle Detection Project**

The goals / steps of this project are the following:

* Perform a Histogram of Oriented Gradients (HOG) feature extraction on a labeled training set of images and train a classifier Linear SVM classifier
* Optionally, you can also apply a color transform and append binned color features, as well as histograms of color, to your HOG feature vector. 
* Note: for those first two steps don't forget to normalize your features and randomize a selection for training and testing.
* Implement a sliding-window technique and use your trained classifier to search for vehicles in images.
* Run your pipeline on a video stream (start with the test_video.mp4 and later implement on full project_video.mp4) and create a heat map of recurring detections frame by frame to reject outliers and follow detected vehicles.
* Estimate a bounding box for vehicles detected.

[//]: # (Image References)
[image1]: ./output_images/car_notcar.png
[image2a]: ./output_images/hog0.png
[image2b]: ./output_images/hog1.png
[image2c]: ./output_images/hog2.png
[image3]: ./output_images/windows.png
[image4]: ./output_images/cars.png
[image5]: ./output_images/heat_maps.png
[image6]: ./output_images/result.png
[video1]: ./result.mp4


### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  


### Histogram of Oriented Gradients (HOG)

#### 1. Explain how (and identify where in your code) you extracted HOG features from the training images.

The code for this implementation can be seen in sections **Features Definition** and **Features Extraction** on `CarND-Vehicle-Detection-Images.ipynb` 

I started by reading in all the `vehicle` and `non-vehicle` images.  Here is an example of one of each of the `vehicle` and `non-vehicle` classes:

![alt text][image1]

I checked different color spaces and different `skimage.hog()` parameters (`orientations`, `pixels_per_cell`, and `cells_per_block`).  I grabbed random images from each of the two classes and displayed them to get a feel for what the `skimage.hog()` output looks like.

Best results were achieved using `YUV` color space and HOG parameters of `orientations=9`, `pixels_per_cell=(8, 8)` and `cells_per_block=(2, 2)`:


![alt text][image2a]
![alt text][image2b]
![alt text][image2c]

#### 2. Explain how you settled on your final choice of HOG parameters.

HOG parameters were chosen by trial and error. At the beggining it was very difficult to select the right color space. After seen different results, I used `YUV` color space because it gave me best results in identifying the white car in the video. I also used the Udacity videos as reference to select other parameters such as `orientation`, `pixels_per_cell` and `cells_per_block` .

#### 3. Describe how (and identify where in your code) you trained a classifier using your selected HOG features (and color features if you used them).

I trained a linear SVM from two different data sets. One is the smallset (vehicles and non-vehicles) and the other was the labeled data set for vehicles and non-vehicles (check section **Data Set** on `CarND-Vehicle-Detection-Images.ipynb`).
I used around 2000 JPEG images of 64x64. I scaled and shuffled my data set, then divided in 80% for trainning and 20% for testing (check section **Trainning and Fitting** on `CarND-Vehicle-Detection-Images.ipynb`)

Results from my SVM are as follows:

`
Feature vector length: 17676
10.5 Seconds to train SVC...
Test Accuracy of SVC =  0.9828`

### Sliding Window Search

#### 1. Describe how (and identify where in your code) you implemented a sliding window search.  How did you decide what scales to search and how much to overlap windows?

I implemented a window search as explained on the Udacity videos (check **Slinding Window Method** on `CarND-Vehicle-Detection-Images.ipynb`). After that, I created a Sliding Window Search as shown on section **Search single image features using sliding window technique** on `CarND-Vehicle-Detection-Images.ipynb`. The key idea on this implementation is to generate a series of windows that goes around the picture. Each window compares the region it sees with the SVM implementation, and if it predicts that its a car, then a bounding box is generated.

The different scales selected were chosen by trial and error, these are as follows:

| box size      | x_init, x_final        | y_init, y_final      | 
|:-------------:|:-------------:|:-------------:| 
| 96, 96        | 200, 1280      | 400, 500       | 
| 144, 144      | 200, 1280     | 400, 600     |
| 192, 192      | 150, 1280      | 430, 630      |
| 192, 192      | 0, 1280      | 460, 660        |

Original overlap was chosen to be 0.75 but after some tests 0.90 was selected. (This change also increased the time to calculate each frame on the video). The picture below show the result of using this parameters:

![alt text][image3]

#### 2. Show some examples of test images to demonstrate how your pipeline is working.  What did you do to optimize the performance of your classifier?

Ultimately I searched on four scales using YUV 3-channel HOG features plus spatially binned color and histograms of color in the feature vector, which provided a good result. Some result images are shown below:  

![alt text][image4]
---

### Video Implementation

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (somewhat wobbly or unstable bounding boxes are ok as long as you are identifying the vehicles most of the time with minimal false positives.)
Here's a [link to my video result](./result.mp4)


#### 2. Describe how (and identify where in your code) you implemented some kind of filter for false positives and some method for combining overlapping bounding boxes.

I recorded the positions of positive detections in each frame of the video.  From the positive detections I created a heatmap and then thresholded that map to more that 2 finds so I could identify vehicle positions.  I then used `scipy.ndimage.measurements.label()` to identify individual blobs in the heatmap.  I then assumed each blob corresponded to a vehicle.  I constructed bounding boxes to cover the area of each blob detected check **Heat map detection** on  `CarND-Vehicle-Detection-Video.ipynb`.

Here's an example result showing the heatmap from a series of frames of video, the result of `scipy.ndimage.measurements.label()` and the bounding boxes then overlaid on the last frame of video:

### Here are six frames and their corresponding heatmaps:

![alt text][image5]

### Here is the output of `scipy.ndimage.measurements.label()` on the integrated heatmap from all ten frames:
![alt text][image6]



---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

When I implemented this project I had to succed in different problems such as:
1. **Find correct parameters for HOG transform.** This was very time consuming and I had to check and recheck many times. After many attepms I realized that YUV color space was the one that suited better my needs.
2. **Data sets.** I found that if I used just the small data sets provided I couldn't detect the white car on the video, and if I used the big data set provided I got too many false detects. My aproach was to join a small part of the big data set with the small data set. The results for this change were much better.
3. **Windowing size and position.** I started by just using 2 windows, but it didn't find cars as I would expected, so I increase the number of windows to 4. After that, my computing time increased, so I started my slinding window on different x values were cars never appear.
4. **Video implementation.** I ran into how to implement this on the video given, so I decided to take all the frames of the video, analize every 10 frames and calculate the average hot windows for that amount of frames. With this approach, my implementation was too slow, so in order to achive better perfomance I saved my bounding boxes on a pickle file for later use. That saved me a lot of time.

My pipeline would not work on real time, and that is one key limitation. It can be much better if I could apply some cache technique to save time computation. Another approach that I may use, since I am an electronic engieneer, is to develop some hardware accleration to calculate on a parallel basis each window. 


