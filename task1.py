# -*- coding: utf-8 -*-
"""Task1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hyRBpJ7tPhM58okWwI4xDfZLliEwkR0d

**Dataset Uploading **
"""

!pip install opendatasets

import opendatasets as od
import pandas

od.download(
    "https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset")

"""**Importing main libraries , tensorflow and keras  **"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

"""**Define Dataset path and other essentials parameters**"""

dataset_path = "/content/plantvillage-dataset"
img_size = 256
batch_size = 32
epochs = 10

"""**Traning and Validation Data Gneerator**"""

train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2)

train_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='binary',
    subset='training')

validation_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='binary',
    subset='validation')

"""**CNN Model layers **"""

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_size, img_size, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

"""**Compling the model and train it using the previous train and validate data generators**"""

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size,
    epochs=5)

"""**Testing the model using image sample giving it's path**"""

test_image_path = "/content/g.jpg"
test_image = tf.keras.preprocessing.image.load_img(
    test_image_path, target_size=(img_size, img_size))
test_image = tf.keras.preprocessing.image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis=0)
result = model.predict(test_image)

if result[0] > 0.01:
    print("The plant in the image is diseased.")
else:
    print("The plant in the image is healthy.")