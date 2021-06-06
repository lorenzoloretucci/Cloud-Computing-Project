import keras
import numpy as np
import tensorflow as tf
import boto3

class Inception_Model():
   def __init__(self):
      self.s3 = boto3.resource('s3')
      self.retrieve_modification_date()
      self.s3.Bucket('clc-project-mlmodels').download_file("best_model_2_inc.h5",'best_model_2_inc.h5')
      self.model = keras.models.load_model("best_model_2_inc.h5",compile=True)
      self.class_names = ['buildings', 'forest', 'glacier', 'mountain', 'sea', 'street']
      load_model_to_mem = self.return_prediction("/home/ec2-user/image_to_model.jpg") ## loads model to main memory

   def return_prediction(self,image_name):
      img = tf.keras.preprocessing.image.load_img(image_name,target_size=(150, 150))
      img = tf.keras.preprocessing.image.img_to_array(img)
      img = tf.expand_dims(img, 0)/255.0
      prediction = self.model.predict(img)
      predicted_class = np.argmax(prediction, axis = 1)
      return self.class_names[predicted_class[0]]

   def retrieve_modification_date(self):
      obj = self.s3.Object("clc-project-mlmodels","best_model_2_inc.h5")
      self.model_update_time = obj.last_modified
