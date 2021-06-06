import numpy as np
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.layers import Flatten



def image_generator(train_data, test_data, target= (150,150), batch = 64):

    train_datagen = ImageDataGenerator(rescale=1./255., 
                                   validation_split=0.2,
                                   rotation_range=10,  # randomly rotate images in the range (degrees, 0 to 180)
                                   width_shift_range=0.1, # randomly shift images horizontally (fraction of total width)
                                   height_shift_range=0.1) # randomly shift images vertically (fraction of total height)

    validation_datagen = ImageDataGenerator(validation_split = 0.2,
                                        rescale=1./255.) 

    train_gen = train_datagen.flow_from_directory(train_data, 
                                              target_size = target,
                                              batch_size= batch,
                                              subset ='training',
                                              seed = 321,
                                              color_mode='rgb',
                                              class_mode='categorical')

    validation_gen = validation_datagen.flow_from_directory(train_data,
                                                        target_size = target,
                                                        class_mode='categorical',
                                                        seed = 321,
                                                        color_mode='rgb',
                                                        batch_size= batch,                                                       
                                                        subset='validation')   

    test_datagen = ImageDataGenerator(rescale=1./255.)

    test_gen = test_datagen.flow_from_directory(test_data,
                                            target_size = target,
                                            batch_size=batch)

    return train_gen, validation_gen


def create_model(pre_trained_model_path ): 

    inc_conv = tf.keras.models.load_model(pre_trained_model_path)
    inc_conv.trainable=False

    model = Sequential()
    model.add(inc_conv)
    model.add(Flatten())
    model.add(Dense(units = 128, activation = 'relu'))
    #inc.add(Dropout(rate = 0.5))
    model.add(Dense(units = 128, activation = 'relu'))
    model.add(Dense(units = 6, activation = 'softmax')) 


    model.compile(optimizer= 'adam',loss='categorical_crossentropy',metrics=['acc'])
    return model 



