from rl_model import PolicyGradient_chatbot 
import sys 
from gensim.models import KeyedVectors
import tensorflow as tf 
import config 
import data_utils as data_parser
import os 

tf_config = tf.ConfigProto()
tf_config.intra_op_parallelism_threads = 44
tf_config.inter_op_parallelism_threads = 44

# ===========================================
# Global Params
# ===========================================
default_model_path = './saver/model/RL/model-56-3000'

dim_wordvec = 300
dim_hidden = 1000

n_encode_lstm_step = 22 + 1 # one random normal as the first timestep
n_decode_lstm_step = 22

batch_size = 1



word_vector = KeyedVectors.load_word2vec_format('saver/word_vector.bin', binary=True)
word_count_threshold = config.WC_threshold

_, ixtoword, bias_init_vector = data_parser.pre_build_word_vocab(word_count_threshold=word_count_threshold)


# model 
model = PolicyGradient_chatbot(
            dim_wordvec=dim_wordvec,
            n_words=len(ixtoword),
            dim_hidden=dim_hidden,
            batch_size=batch_size,
            n_encode_lstm_step=n_encode_lstm_step,
            n_decode_lstm_step=n_decode_lstm_step,
            bias_init_vector=bias_init_vector)

word_vectors, caption_tf, feats = model.build_generator()

sess =tf.Session(config=tf_config)

saver =tf.train.Saver()
saver = tf.train.import_meta_graph(os.path.join(default_model_path+".meta"))


def refine(data):
    words = re.findall("[a-zA-Z'-]+", data)
    words = ["".join(word.split("'")) for word in words]
    # words = ["".join(word.split("-")) for word in words]
    data = ' '.join(words)
    return data

print("\n ================ Using ", default_model_path,"===========\n")
saver.restore(sess,default_model_path)
