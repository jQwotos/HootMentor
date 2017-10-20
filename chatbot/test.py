#intended for suitable testing 
from gensim.models import KeyedVectors
import data_parser
import config

from model import seq2seq_chatbot
import tensorflow as tf
import numpy as np

import re
import os
import sys
import time


#=====================================================
# Global Parameters
#=====================================================
default_model_path = './saver/Seq2Seq/model-77'
testing_data_path = './tmp/sample_input.txt' if len(sys.argv) <= 2 else sys.argv[2]
output_path = './tmp/sample_output_S2S.txt' if len(sys.argv) <= 3 else sys.argv[3]

word_count_threshold = config.WC_threshold

#=====================================================
# Train Parameters
#=====================================================
dim_wordvec = 300
dim_hidden = 1000

n_encode_lstm_step = 22 + 1 # one random normal as the first timestep
n_decode_lstm_step = 22

batch_size = 1

def test(model=default_model_path):
    testing_data = open(testing_data_path,'r').read().split("\n")

    word_vector = KeyedVectors.load_word2vec_format('./word_vector.bin', binary=True)
    
    # loading embedding vector map
    _, ixtoword, bias_init_vector = data_parser.pre_build_word_vocab(word_count_threshold=word_count_threshold)
    
    model = seq2seq_chatbot(
            dim_wordvec=dim_wordvec,
            n_words=len(ixtoword),
            dim_hidden=dim_hidden,
            batch_size=batch_size,
            n_encode_lstm_step=n_encode_lstm_step,
            n_decode_lstm_step=n_decode_lstm_step,
            bias_init_vector=bias_init_vector)
    # word_vectors, caption_tf, probs, _ =
    model.build_generator()
    

if __name__ == '__main__':
    if len(sys.argv) >1:
        test(model= sys.argv[1])
    else:
        test()
    