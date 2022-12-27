import tensorflow as tf 
import vgg19_fastmal as vgg19
import utils

import os
import numpy as np
import re 
from shutil import copyfile
import math
import random

IMSIZE = 64
epochs = 10
batch_size = 32
lr = 0.01
num_labels=2
num_steps = 1




with tf.compat.v1.Session() as sess :

    images = tf.compat.v1.placeholder(tf.float32, [None, IMSIZE, IMSIZE, 3])
    labels = tf.compat.v1.placeholder(tf.float32, [None, 2])
    train_mode = tf.compat.v1.placeholder(tf.bool)

    vgg = vgg19.Vgg19(imsize=64, trainable=True) #Chargement du modèle
    vgg.build_avg_pool(images) #Rajout des couches denses

    focal_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = vgg.new_fc8, labels=labels)) #Fonction de loss
    train = tf.compat.v1.train.GradientDescentOptimizer(0.003).minimize(focal_loss) #Optimizer
    sess.run(tf.compat.v1.global_variables_initializer())

    for step in range(epochs) :

        slides = np.array(slides)
        _,l = sess.run([train, focal_loss], feed_dict={images: slides, labels : labels, train_mode: True})
