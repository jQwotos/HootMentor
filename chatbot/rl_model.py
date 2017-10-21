import tensorflow as tf 
import numpy as np 
from model import seq2seq_chatbot

class PolicyGradient_chatbot(seq2seq_chatbot):
    def __init__(self, dim_wordvec, n_words, dim_hidden, batch_size
        , n_encode_lstm_step, n_decode_lstm_step, bias_init_vector=None, lr=0.0001):
        # inheritance from seq2seq_chatbot
        super(dim_wordvec,n_words,dim_hidden,batch_size,n_encode_lstm_step,n_decode_lstm_step,bias_init_vector,lr)
    
    def graph_model(self):
        # feed_dict
        word_vectors = tf.placeholder(tf.float32, [self.batch_size,self.n_encode_lstm_step,self.dim_wordvec])
        
        caption = tf.placeholder(tf.int32,[self.batch_size,self.n_decode_lstm_step+1])
        caption_mask = tf.placeholder(tf.float32,[self.batch_size,self.n_decode_lstm_step+1])

        word_vectors_flat = tf.reshape(word_vectors, [-1, self.dim_wordvec])
        wordvec_emb = tf.nn.xw_plus_b(word_vectors_flat, self.encode_vector_W, self.encode_vector_b ) # (batch_size*n_encode_lstm_step, dim_hidden)
        wordvec_emb = tf.reshape(wordvec_emb, [self.batch_size, self.n_encode_lstm_step, self.dim_hidden])

        reward = tf.placeholder(tf.float32, [self.batch_size, self.n_decode_lstm_step])

        state1 = tf.zeros([self.batch_size, self.lstm1.state_size])
        state2 = tf.zeros([self.batch_size, self.lstm2.state_size])
        padding = tf.zeros([self.batch_size, self.dim_hidden])


        entropies = []
        loss = 0.
        # policy gradient loss 
        pg_loss = 0. 
        ########### Encoding states ######################
        for i in range ( self.n_encode_lstm_step):
            if i>0:
                tf.get_variable_scope().reuse_variables()
            
            with tf.variable_scope("LSTM1"):
                output1,state1 =self.lstm1(wordvec_emb[:,i,:],state1)

            with tf.variable_scope("LSTM2"):
                output2, state2 = self.lstm2(tf.concat([padding, output1], 1), state2)
        ########### Decoding states ######################
        for i in range(self.n_decode_lstm_step):
            with tf.device("/cpu:0"):
                current_embed = tf.nn.embedding_lookup(self.Wemb, caption[:, i])

            tf.get_variable_scope().reuse_variables()

            with tf.variable_scope("LSTM1"):
                output1, state1 = self.lstm1(padding, state1)

            with tf.variable_scope("LSTM2"):
                output2, state2 = self.lstm2(tf.concat([current_embed, output1], 1), state2)
                        labels = tf.expand_dims(caption[:, i+1], 1)
            indices = tf.expand_dims(tf.range(0, self.batch_size, 1), 1)
            concated = tf.concat([indices, labels], 1)
            onehot_labels = tf.sparse_to_dense(concated, tf.stack([self.batch_size, self.n_words]), 1.0, 0.0)

            logit_words = tf.nn.xw_plus_b(output2, self.embed_word_W, self.embed_word_b)
            # probs.append(logit_words)

            cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=logit_words, labels=onehot_labels)
            cross_entropy = cross_entropy * caption_mask[:, i]
            entropies.append(cross_entropy)
            pg_cross_entropy = cross_entropy * reward[:, i]

            # current_loss = tf.reduce_sum(cross_entropy) / self.batch_size
            # loss = loss + current_loss

            pg_current_loss = tf.reduce_sum(pg_cross_entropy) / self.batch_size
            pg_loss = pg_loss + pg_current_loss

        with tf.variable_scope(tf.get_variable_scope(), reuse=False):
            #options of optimization s 

            # train_op = tf.train.RMSPropOptimizer(self.lr).minimize(loss)
            # train_op = tf.train.GradientDescentOptimizer(self.lr).minimize(loss)
            train_op = tf.train.AdamOptimizer(self.lr).minimize(pg_loss)
            # pg_train_op = tf.train.AdamOptimizer(self.lr).minimize(pg_loss)

        # train_ops = {
        #     'normal': train_op, # normal training
        #     'pg': pg_train_op   # policy gradient training
        # }

        # losses = {
        #     'normal': loss, # normal loss
        #     'pg': pg_loss   # policy gradient loss
        # }

        input_tensors = {
            'word_vectors': word_vectors,
            'caption': caption,
            'caption_mask': caption_mask,
            'reward': reward
        }

        feats = {
            'entropies': entropies
            # 'probs': probs,
            # 'states': states
        }

        return train_op, pg_loss, input_tensors, feats

    def reward_sys(self):
        pass