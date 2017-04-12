
## Writeup Project 4, Advanced Lane Lines

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./images/image_01.png "Undistorted"
[image2]: ./images/image_02.png "Road Transformed"
[image3]: ./output_images/filtered_image.png "Binary Example"
[image4]: ./images/image_04.png "Road Transformed"
[image5]: ./images/image_05.png "Fit Visual"
[image6]: ./output_images/poly_fit.png "Output"
[image7]: ./output_images/final.png "Output"

[video1]: ./project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one. 

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

To obtain the camera matrix and distortion coefficients I did the following steps (please che `CarND_Project4_CameraCalibration.ipynb`):

1. Prepare all the `object` points. In this case, the chessboard consisted by an 9x6x0 array of points.
2. Determine the `image` points on the chessboard on each image given by using the function `cv2.findChessboardCorners()`.
3. Calculate the `camera matrix` and `distortion coefficients`by using the function `cv2.calibrateCamera()` to the `object` and `image` points.
4. Test the results with `cv2.undistort` function. 

The results of this procedure can be seen on this image:  

![alt text][image1]

The camera matrix and distortion coefficients were saved into a `pickle` file for later use on the pipeline.

### Pipeline (single images)
You can check the pipeline implementation for single images on `CarND_Project4_Pipeline(Single_Images).ipynb`

#### 1. Provide an example of a distortion-corrected image.
To apply a distortion correction on each image, I used the `pickle` data from the previous step were `camera matrix` and `distortion coefficients` were calculated.

![alt text][image2]
#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.
To generate a thresholded binary image Ifirst converted the original image into an HLS image. After that, I applied a Sobel Filter in the "x" direction to find vertical lines on the S-Channel. Another HLS copy of the original image was used to find a thresholded S-Channel pixels.

I cobined both image filters. The results of this is:

![alt text][image3]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The folling image shows the region of interest that I used to make a perspective transform.
![alt text][image4]

In this case I created a function called `perspective_transform` that takes an image, `source points` and `destination points`and returns `perspective transformed image`.

The source and destination points were selected by looking at the image:

[[1090, 0], [1090, 720], [273, 720], [273, 0]])

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 727, 450      | 1090, 0       | 
| 1150, 720     | 1090, 720     |
| 273, 720      | 273, 720      |
| 597, 450      | 273, 0        |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image5]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?
To find a polynomial fit for the lane-line pixels I did the following steps:

1. Create a histogram of the bottom half image pixels and find the left and right initial positions of the lane lines.
2. Use the sliding windows method described on the lectures to "follow" each lane line to obtain a certain amout of pixels that will be used for fitting a curve.
3. Fit a second order polynomial with all the pixels from step 2 for each lane line.
4. Generate a linear space for each lane line, with the x values modeled with the second order polynomial.

The result of this implementation looks like this:

![alt text][image6]


#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

To find the radius of curvature I had to change from pixel space to real space. The number of meters per pixel in y dimension is 30/720 and in the x dimension is 3.7/700.

With this change, I found a new polynomial fit and linear space for each line as in section 5.
Later I used the formula given in the [Advance Lane Finding](http://www.intmath.com/applications-differentiation/8-radius-curvature.php) to calculate the curvature of each lane line and average them.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

The final results are shown on the next image. A polygon is generated between both lane lines using `cv2.fillPoly`.

![alt text][image7]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)

The whole implementation can be seen on `CarND_Project4_Pipeline(Videos).ipynb`

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

I had a two main problems that I want to mention:

1. Right lane lines were not correctly fitted by polynomial: The main problem here was that my upper thresholds for the sobel filter were too high, and also I had to reduce the bounding box lenght because there were other pixels taken on the image to fit the polynomial.

2. Area between lanes (green shaded area) dissapear from time to time: The issue here was that some polynomials were not correctly calculated (even if I tried to solve it as before), so the area between lanes was very messy. To solve this problem I checked present and past frames and measure the distance between left and right lanes on both frames, if the distance changed too much from frame to frame I discarded the calculations from the present frame and used the previous calculations.

My pipeline will likely fail if for example a car is very near to a lane line or if a slope is to high. Another problem that I might encounter is if there is no lane line, in that case my pipeline will fail too. One of the things that I would like to test, to make my pipeline more robust, is the size of the windows used to make the polynomial fit. If I can make it variable, depending on the type of curve, it will be more robust on finding a good polynomial with less chance to take undesirable pixels.



```python

```
