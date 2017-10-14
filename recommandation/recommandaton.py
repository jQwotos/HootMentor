import numpy as np 
import pandas as pd
import tflearn


import os 
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

class recommander():
    def __init__(self,skills_cols,weights,cols_names):
        self.weights = np.array(weights)
        self.skill_cols = pd.DataFrame(np.array(skill_cols).reshape((-1,1)))

    def build_network(self,summary_writer,train_x,train_y ,n_epoch=1000,batch_size=10,show_metric=True,scope="recommandation/"):
        with tf.name_scope(scope):
            # m is list of jobs and n is numbers of skills
            x=tf.placholder(tf.float32,shape=[None,train_x.shape[1]])
            y=tf.placholder(tf.float32,shape=[None,train_y.shape[0]])
            # mxn * n
            W=tf.Variable(tf.zeros([train_x.shape[1],train_y.shape[0]]),name="weights")
            b=tf.Variable(tf.zeros([train_y.shape[0]]),name="bias")
            losses=tf.losses.mean_squared_error(y,tf.matmul(x,W)+b,name="sq_error")
        