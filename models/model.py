import tensorflow as tf
import cv2

class Model():
    def __init__(self):
        self.model=tf.keras.models.load_model(r'water_pred_02.h5')

    def image_to_feature_vector(self,image_get, size=(128, 128)):
      # Load the image using OpenCV
      # image = cv2.imread(image_path)
      # Resize the image to the specified size
      image = cv2.resize(image_get, size)

      self.image=image.reshape((1,128,128,3))

    def image_prediction(self,image):
      pred=self.model.predict(image)
      pred=pred.flatten()
      if pred<=0.5:
        return 0
      else:
        return 1