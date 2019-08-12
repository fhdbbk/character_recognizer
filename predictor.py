import numpy as np
import cv2
import os
import tensorflow as tf
from architecture import Lenet


def normalize_images(x):
    x = (x - 128) / 256.0
    return x


class Predictor:
    def __init__(self):
        self.x = tf.placeholder(tf.float32, (None, 32, 32, 1))
        self.y = tf.placeholder(tf.int32, (None))
        self.one_hot_y = tf.one_hot(self.y, 10)
        self.logits = Lenet().model(self.x)
        self.sess = self.load_model()

    def load_model(self):
        saver = tf.train.Saver()
        sessn = tf.Session()
        saver.restore(sessn, tf.train.latest_checkpoint('../models'))
        print("Loaded the graph...")
        return sessn

    def get_maxprob_idx(self, probs):
        max_prob_idx = None
        max_prob = -1
        for i in range(len(probs)):
            if probs[i] > max_prob:
                max_prob = probs[i]
                max_prob_idx = i
        return max_prob_idx

    def predict(self, image):
        #image = cv2.imread(image_file, 0)

        image = cv2.resize(image, (32, 32))
        image = normalize_images(image)
        image_vector = np.reshape(image, (1, 32, 32, 1))
        pred = tf.nn.softmax(self.logits)
        print("Shape of Image: {}".format(image.shape))
        classification = self.sess.run(pred, feed_dict={self.x: image_vector})
        print("Result of classification: {}".format(classification))
        print("Performed the classification")
        probs = classification[0]
        idx = np.argmax(probs)
        print("Predicted number = {}".format(idx))
        return idx

    def close_session(self):
        self.sess.close()
        print("Tensorflow session closed")

if __name__ == '__main__':
    predictor = Predictor()
    image_file = 'temp/img1.png'
    predictor.predict(image_file)




