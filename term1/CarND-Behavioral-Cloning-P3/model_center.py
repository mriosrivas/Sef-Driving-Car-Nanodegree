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
    while 1: # Loop forever so the generator never terminates
        sklearn.utils.shuffle(samples)
        for offset in range(0, num_samples, batch_size):
            batch_samples = samples[offset:offset+batch_size]

            images = []
            angles = []
            for batch_sample in batch_samples:
                name = './data/IMG/'+batch_sample[0].split('/')[-1]
                center_image = cv2.imread(name)
#                assert float(batch_sample[3])
                center_angle = float(batch_sample[3])
                images.append(center_image)
                angles.append(center_angle)

            # trim image to only see section with road
            X_train = np.array(images)
            y_train = np.array(angles)
            yield sklearn.utils.shuffle(X_train, y_train)

# compile and train the model using the generator function
train_generator = generator(train_samples, batch_size=32)
validation_generator = generator(validation_samples, batch_size=32)

ch, row, col = 3, 160, 320  # Original image format
trim_up, trim_down = 70, 24 
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

#Convolutional Network with 5x5 kernel
model.add(Convolution2D(24, 5, 5, border_mode='same', input_shape=(crop_row, col, ch)))
model.add(MaxPooling2D((2, 2)))
model.add(Activation('relu'))

#Convolutional Network with 5x5 kernel
model.add(Convolution2D(36, 5, 5, border_mode='same'))
model.add(MaxPooling2D((2, 2)))
model.add(Activation('relu'))

#Convolutional Network with 5x5 kernel
model.add(Convolution2D(48, 5, 5, border_mode='same'))
model.add(MaxPooling2D((2, 2)))
model.add(Activation('relu'))

#Convolutional Network with 3x3 kernel
model.add(Convolution2D(64, 3, 3, border_mode='same'))
model.add(MaxPooling2D((2, 2)))
model.add(Activation('relu'))

#Convolutional Network with 3x3 kernel
model.add(Convolution2D(64, 3, 3, border_mode='same'))
model.add(MaxPooling2D((2, 2)))
model.add(Activation('relu'))

#Flatten Layer 1x33x64 = 2112
#model.add(Flatten(input_shape=(33, 64, 1)))
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

#Fully Connected Layer
model.add(Dense(1))


model.compile(loss='mse', optimizer='adam')
model.fit_generator(train_generator, samples_per_epoch=len(train_samples), validation_data=validation_generator, nb_val_samples=len(validation_samples), nb_epoch=3)


# parses flags and calls the `main` function above
#if __name__ == '__main__':
#    tf.app.run()


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
