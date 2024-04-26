# -*- coding: utf-8 -*-
"""Final Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1OqRgYnTITvi1s5mhqTWKQ4_bAKF-ioUw
"""

# Import necessary libraries
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras import layers, models

# Load and preprocess data
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)
test_datagen = ImageDataGenerator(rescale=1./255)


train_generator = train_datagen.flow_from_directory(
    '/home/sivabalan/Downloads/sample dataset/lungs cancer dataset',
    target_size=(299, 299),
    batch_size=32,
    class_mode='categorical'  # Change to 'categorical' if more than two classes
)
validation_generator = test_datagen.flow_from_directory(
    '/home/sivabalan/Downloads/sample dataset/lungs cancer dataset',
    target_size=(299, 299),
    batch_size=32,
    class_mode='categorical'  # Change to 'categorical' if more than two classes
)

#Create InceptionV3 model
base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(299, 299, 3))

# Freeze the convolutional layers
for layer in base_model.layers:
    layer.trainable = False

from keras.models import Sequential
from keras.layers import Convolution2D, Dropout, Dense,MaxPooling2D
from keras.layers import BatchNormalization
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras import regularizers
def lw(bottom_model,num_classes):
  top_model=bottom_model.output
  top_model=GlobalAveragePooling2D()(top_model)
  top_model=Dense(1024,activation='relu')(top_model)
  top_model=Dense(512,activation='relu')(top_model)
  top_model=Dense(128,activation='relu',kernel_regularizer=regularizers.l2(0.01))(top_model)
  top_model=Dense(num_classes,activation='softmax')(top_model)
  return top_model


from keras.models import Sequential
from keras.layers import Dense,Dropout,Activation,Flatten,GlobalAveragePooling2D
from keras.layers import Conv2D,MaxPooling2D,ZeroPadding2D
from keras.models import Model

num_classes=3
FC_Head=lw(base_model,num_classes)
model = Model(inputs=base_model.input, outputs=FC_Head)
print(model.summary())

# Compile the model
from tensorflow.keras.models import Model
model.compile(optimizer='adam', loss = 'categorical_crossentropy',metrics = ['accuracy'])

# Train the model
history=model.fit(
    train_generator,
    epochs=2,
    validation_data=validation_generator
)

#Evaluate the model
evaluation = model.evaluate(validation_generator)
print(f"Validation Accuracy: {evaluation[1]*100:.2f}%")

# Save the model# Train the model
history=model.fit(
    train_generator,
    epochs=2,
    validation_data=validation_generator
)
model.save('lung_cancer_prediction_model.h5')

import os
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input, decode_predictions
import numpy as np

# Load the trained model
model = load_model('lung_cancer_prediction_model.h5')

# Get input image path from user
image_path = input("Enter the path to the image: ")

# Check if the file exists
if not os.path.isfile(image_path):
    print(f"Error: File '{image_path}' not found.")
    exit()

# Load and preprocess the input image
img = image.load_img(image_path, target_size=(299, 299))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = tf.keras.applications.inception_v3.preprocess_input(img_array)

# Make predictions
predictions = model.predict(img_array)

# Interpret predictions
if predictions[0][0] > 0.5:
    result = "Positive: The image indicates the presence of lung cancer."
else:
    result = "Negative: The image suggests the absence of lung cancer."
#load the inception model
    model = Model(inputs=base_model.input, outputs=base_model.layers[100].output)

#Function to visualize feature maps of an intermediate layer
def visualize_feature_maps(img_path, model):
    img = image.load_img(img_path, target_size=(299, 299))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # Get activations of the chosen intermediate layer
    intermediate_layer_outputs = model.predict(x)

    # Plot the feature maps
    num_features = intermediate_layer_outputs.shape[-1]
    square_dim = int(np.ceil(np.sqrt(num_features)))
    fig, axes = plt.subplots(square_dim, square_dim, figsize=(12, 12))

    for i in range(square_dim):
        for j in range(square_dim):
            if i * square_dim + j < num_features:
                axes[i, j].imshow(intermediate_layer_outputs[0, :, :, i * square_dim + j], cmap='viridis')
                axes[i, j].axis('off')
            else:
                axes[i, j].axis('off')

    plt.show()

# Output the result
print(result)
visualize_feature_maps(image_path, model)