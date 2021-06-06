import numpy as np
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.layers import Flatten

from train_function import image_generator, create_model

TRAIN_dir = '' ## Add training folder path

TEST_dir = '' ## Add test folder path

inc_path = '' ## Add pre-trainde model folder path


train_gen, validation_gen = image_generator(TRAIN_dir, TEST_dir) 

model = create_model(inc_path)

callback1 = EarlyStopping(monitor='val_acc', patience=4)

history = model.fit(train_gen, epochs=2, validation_data = validation_gen, callbacks=callback1)

model.save("model_inc.h5")



