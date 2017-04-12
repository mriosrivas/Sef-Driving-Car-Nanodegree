import os
import csv

samples = []
with open('./data/driving_log.csv') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        samples.append(line)

from sklearn.model_selection import train_test_split
train_samples, validation_samples = train_test_split(samples, test_size=0.2)

import cv2
import numpy as np
import sklearn

def generator(samples, batch_size=32):
    num_samples = len(samples)
    correction = 0.2
    while 1: # Loop forever so the generator never terminates
        sklearn.utils.shuffle(samples)
        for offset in range(0, num_samples, batch_size):
            batch_samples = samples[offset:offset+batch_size]

            images = []
            angles = []
            for batch_sample in batch_samples:
                name = './data/IMG/'+batch_sample[0].split('/')[-1]
                center_image = cv2.imread(name)
                center_angle = float(batch_sample[3])
                images.append(center_image)
                angles.append(center_angle)

                name_left = './data/IMG/'+batch_sample[1].split('/')[-1]
                left_image = cv2.imread(name_left)
                left_angle = center_angle + correction
                images.append(left_image)
                angles.append(left_angle)

                name_right = './data/IMG/'+batch_sample[2].split('/')[-1]
                right_image = cv2.imread(name_right)
                right_angle = center_angle - correction
                images.append(right_image)
                angles.append(right_angle)

                
		#Generating more data by flipping images and angles
                center_image_flipped = np.fliplr(center_image)
                center_angle_flipped = -center_angle
                images.append(center_image_flipped)
                angles.append(center_angle_flipped)

                left_image_flipped = np.fliplr(left_image)
                left_angle_flipped = -left_angle
                images.append(left_image_flipped)
                angles.append(left_angle_flipped)

                right_image_flipped = np.fliplr(right_image)
                right_angle_flipped = -right_angle
                images.append(right_image_flipped)
                angles.append(right_angle_flipped)


            X_train = np.array(images)
            y_train = np.array(angles)

            yield sklearn.utils.shuffle(X_train, y_train)

# compile and train the model using the generator function
train_generator = generator(train_samples, batch_size=32)
validation_generator = generator(validation_samples, batch_size=32)

ch, row, col = 3, 160, 320  # Original image format
trim_up, trim_down = 70, 24 # Trimming values to reduce each image
crop_row = row - trim_up - trim_down #Reduced row size

from keras.models import Sequential, Model
from keras.layers.core import Lambda, Flatten, Dense, Activation
from keras.layers.convolutional import Cropping2D, Convolution2D
from keras.layers.pooling import MaxPooling2D


model = Sequential()

# set up cropping2D layer
model.add(Cropping2D(cropping=((trim_up, trim_down), (0,0)), input_shape=(row, col, ch)))

# Preprocess incoming data, centered around zero with small standard deviation 
model.add(Lambda(lambda x: x/255 - 0.5, input_shape=(crop_row, col, ch), output_shape=(crop_row, col, ch)))

#Convolutional Network with 5x5 kernel and depth of 24
model.add(Convolution2D(24, 5, 5, border_mode='same', input_shape=(crop_row, col, ch)))
model.add(MaxPooling2D((2, 2)))
model.add(Activation('relu'))

#Convolutional Network with 5x5 kernel and depth of 36
model.add(Convolution2D(36, 5, 5, border_mode='same'))
model.add(MaxPooling2D((2, 2)))
model.add(Activation('relu'))

#Convolutional Network with 5x5 kernel and depth of 48
model.add(Convolution2D(48, 5, 5, border_mode='same'))
model.add(MaxPooling2D((2, 2)))
model.add(Activation('relu'))

#Convolutional Network with 3x3 kernel and depth of 64
model.add(Convolution2D(64, 3, 3, border_mode='same'))
model.add(MaxPooling2D((2, 2)))
model.add(Activation('relu'))

#Convolutional Network with 3x3 kernel and depth of 64
model.add(Convolution2D(64, 3, 3, border_mode='same'))
model.add(MaxPooling2D((2, 2)))
model.add(Activation('relu'))

#Flatten Layer 1x33x64 = 2112
model.add(Flatten())
#model.add(Activation('relu'))

#Fully Connected Layer
model.add(Dense(100))
#model.add(Activation('relu'))

#Fully Connected Layer
model.add(Dense(50))
#model.add(Activation('relu'))

#Fully Connected Layer
model.add(Dense(10))
#model.add(Activation('relu'))

#Fully Connected Layer to obtaing single neuron
model.add(Dense(1))


#Looking for mean square loss and ADAM optimizer
model.compile(loss='mse', optimizer='adam')
model.fit_generator(train_generator, samples_per_epoch=len(train_samples), validation_data=validation_generator, nb_val_samples=len(validation_samples), nb_epoch=3)


import json
import os
import h5py

# Save the model.
# If the model.json file already exists in the local file,
# warn the user to make sure if user wants to overwrite the model.
if 'model.json' in os.listdir():
	print("The file already exists")
	print("Want to overwite? y or n")
	user_input = input()

	if user_input == "y":
		# Save model as json file
		json_string = model.to_json()

		with open('model.json', 'w') as outfile:
			json.dump(json_string, outfile)

			# save weights
			model.save('./model.h5')
			print("Overwrite Successful")
	else:
		print("the model is not saved")
else:
	# Save model as json file
	json_string = model.to_json()

	with open('model.json', 'w') as outfile:
		json.dump(json_string, outfile)

		# save weights
		model.save('./model.h5')
		print("Saved")
