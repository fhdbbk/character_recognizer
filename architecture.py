import tensorflow as tf
from tensorflow.contrib.layers import flatten


class Lenet:
    def model(self, x):
        # Arguments used for tf.truncated_normal, randomly defines variables for the weights and biases for each layer
        mu = 0
        sigma = 0.1

        # SOLUTION: Layer 1: Convolutional. Input = 32x32x1. Output = 32x32x16.
        conv1_W = tf.Variable(tf.truncated_normal(shape=(5, 5, 1, 16),
                              mean=mu, stddev=sigma))
        conv1_b = tf.Variable(tf.zeros(16))
        conv1   = tf.nn.conv2d(x, conv1_W, strides=[1, 1, 1, 1], padding='SAME') + conv1_b

        # SOLUTION: Activation.
        conv1 = tf.nn.relu(conv1)

        # SOLUTION: Pooling. Input = 32x32x16. Output = 16x16x16.
        conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

        #conv1 = tf.layers.batch_normalization(conv1) 

        # SOLUTION: Layer 2: Convolutional. Output = 16x16x32.
        conv2_W = tf.Variable(tf.truncated_normal(shape=(5, 5, 16, 32), mean = mu, stddev = sigma))
        conv2_b = tf.Variable(tf.zeros(32))
        conv2   = tf.nn.conv2d(conv1, conv2_W, strides=[1, 1, 1, 1], padding='SAME') + conv2_b

        # SOLUTION: Activation.
        conv2 = tf.nn.relu(conv2)

        # SOLUTION: Pooling. Input = 16x16x32. Output = 8x8x32.
        conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

        #conv2 = tf.nn.dropout(conv2, keep_prob=0.75)

        # SOLUTION: Flatten. Input = 8x8x32. Output = 2048.
        fc0   = flatten(conv2)

        # SOLUTION: Layer 3: Fully Connected. Input = 2048. Output = 1024.
        fc1_W = tf.Variable(tf.truncated_normal(shape=(2048, 1024), mean = mu, stddev = sigma))
        fc1_b = tf.Variable(tf.zeros(1024))
        fc1   = tf.matmul(fc0, fc1_W) + fc1_b

        # SOLUTION: Activation.
        fc1    = tf.nn.relu(fc1)

        fc1    = tf.nn.dropout(fc1, keep_prob=0.75)

        # SOLUTION: Layer 4: Fully Connected. Input = 1024. Output = 512.
        fc2_W  = tf.Variable(tf.truncated_normal(shape=(1024, 128), mean = mu, stddev = sigma))
        fc2_b  = tf.Variable(tf.zeros(128))
        fc2    = tf.matmul(fc1, fc2_W) + fc2_b

        # SOLUTION: Activation.
        fc2    = tf.nn.relu(fc2)

        fc2    = tf.nn.dropout(fc2, keep_prob=0.6)

        # SOLUTION: Layer 5: Fully Connected. Input = 512. Output = 10.
        fc3_W  = tf.Variable(tf.truncated_normal(shape=(128, 10), mean = mu, stddev = sigma))
        fc3_b  = tf.Variable(tf.zeros(10))
        logits = tf.matmul(fc2, fc3_W) + fc3_b
        return logits