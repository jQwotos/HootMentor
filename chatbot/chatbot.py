# supress warning 
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import nltk
from nltk.stem.lancaster import LancasterStemmer 
stemmer = LancasterStemmer()

import numpy as np 
import tflearn 
import tensorflow as tf
import random

from model import ChatBotModel
import config


class Batch:
    def __init__(self):
        self.encoderSeq=[]
        self.decoderSeqs = []
        self.targetSeqs = []
        self.weights = []


def DNN_network(train_x,train_y,n_epoch=1000,batch_size=10,show_metric=True):
    tf.reset_default_graph()
    # Build neural network
    net = tflearn.input_data(shape=[None, len(train_x[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
    net = tflearn.regression(net)

    # Define model and setup tensorboard
    model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
    # Start training (apply gradient descent algorithm)
    model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("./DNN/model.ckpt")

