import tensorflow as tf 
import types 
import numpy as np 
from six.moves import xrange

#  additional optimization as loop function 
#  matching on tensorflow 1.3.1
def loop_function(tensor,num_iteration,count,word_vec,state):
    # assert isinstance(tensor.__call__,types.FunctionType)
    """
    function loop_function
        loop over  number of iteration on tensor since the tensor are not 
        iterable

        input:
            Tensor: 2D LSTM Tensor that will be iterated
            args: batch feed_dict to the tensor.__call__
                default: 0 -> wordvec_emb[:,i,:]
                         1 -> states of lstm
    """
    if(num_iteration==count-1):
        return tensor(word_vec[:,num_iteration,:],state)
    
    print( num_iteration,count,word_vec,state)
    # compute the upcoming LSTM_call
    _,states = tensor(word_vec[:,num_iteration,:],state)
    print ("New ouput and state are : ",_," ",states)
    num_iteration=num_iteration+1
    # The next following states
    print("Updating new args: ",args)
    loop_function(tensor,num_iteration,count,args)
    

class seq2seq_chatbot():
    # dimension / shape of the word vector and nums of word will be n-gram
    def __init__(self,dim_wordvec,n_words,dim_hidden,batch_size
            ,n_encode_lstm_step,n_decode_lstm_step,bias_init_vector=None,lr=0.001):
        '''
            Seq2seq chatbot 

            @param
                dim_wordvec :dimension of word vectors 
                n_words : nums of words that will be embedded 
                dim_hidden: dimension of hidden layers
                batch_size: batch size that fit into the placeholder 
                n_encode_lstm_step: step of encoding 
                n_decode_lstm_step: step of decoding 
                bias_init_vecotr: bias condition flag 
                lr: learning rate
            @ouput
                A seq2seq model
        '''
        # initializes the parameters
        self.dim_wordvec = dim_wordvec
        self.dim_hidden = dim_hidden
        self.batch_size = batch_size
        self.n_words = n_words
        self.n_encode_lstm_step = n_encode_lstm_step
        self.n_decode_lstm_step = n_decode_lstm_step
        self.lr = lr
        
        # initializes the random word vector
        with tf.device("/cpu:0"):
            self.Wemb = tf.Variable(tf.random_uniform([n_words, dim_hidden], -0.1, 0.1), name='Weight_embedd_bias')
        # Generate the lstm cell
        self.lstm1 = tf.contrib.rnn.BasicLSTMCell(dim_hidden,state_is_tuple=False)
        self.lstm2 = tf.contrib.rnn.BasicLSTMCell(dim_hidden, state_is_tuple=False)
        
        # generate randomizes words vectors 
        
        self.encode_vector_W = tf.Variable(tf.random_uniform([ dim_wordvec, dim_hidden],- 0.1, 0.1),name='weight')
        self.encode_vector_b = tf.Variable(tf.zeros([dim_hidden]), name='biase')
    
        # generate embedded weights vector
        
        self.embed_word_W = tf.Variable(tf.random_uniform([dim_hidden,n_words],-0.1 ,0.1),name='weights')
        if bias_init_vector is not None:
            self.embed_word_b = tf.Variable(bias_init_vector.astype(np.float32), name='embed_word_b')
        else:
            self.embed_word_b = tf.Variable(tf.zeros([n_words]), name='embed_word_b')

    def graph_model(self):
        with tf.name_scope("Seq2Seq"):
            word_vecotors = tf.placeholder(tf.float32, [ self.batch_size,self.n_encode_lstm_step,self.dim_wordvec])
            caption = tf.placeholder(tf.int32, [self.batch_size, self.n_decode_lstm_step+1])
            caption_mask = tf.placeholder(tf.float32, [self.batch_size, self.n_decode_lstm_step+1])

            word_vectors_flat = tf.reshape(word_vectors, [-1, self.dim_wordvec])
            wordvec_emb = tf.nn.xw_plus_b(word_vectors_flat, self.encode_vector_W, self.encode_vector_b ) # (batch_size*n_encode_lstm_step, dim_hidden)
            wordvec_emb = tf.reshape(wordvec_emb, [self.batch_size, self.n_encode_lstm_step, self.dim_hidden])

            state1 = tf.zeros([self.batch_size, self.lstm1.state_size])
            state2 = tf.zeros([self.batch_size, self.lstm2.state_size])
            padding = tf.zeros([self.batch_size, self.dim_hidden])

            probs = []
            entropies = []
            loss = 0.0
            ##############################  Encoding Stage ##################################
            for i in range(0, self.n_encode_lstm_step):
                if i > 0:
                    tf.get_variable_scope().reuse_variables()

                with tf.variable_scope("LSTM1"):
                    output1, state1 = self.lstm1(wordvec_emb[:, i, :], state1)

                with tf.variable_scope("LSTM2"):
                    output2, state2 = self.lstm2(tf.concat([padding, output1], 1), state2)

            ############################# Decoding Stage ######################################
            for i in range(0, self.n_decode_lstm_step):
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
                cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=logit_words, labels=onehot_labels)
                cross_entropy = cross_entropy * caption_mask[:, i]
                entropies.append(cross_entropy)
                probs.append(logit_words)

                current_loss = tf.reduce_sum(cross_entropy)/self.batch_size
                loss = loss + current_loss

                # tensorboard adding value 
                # tf.scalar_summary("sequence_loss",loss)
                # tf.scalar_summary("sequence_entropies",entropies)

            with tf.variable_scope(tf.get_variable_scope(), reuse=False): 
                # train_op = tf.train.RMSPropOptimizer(self.lr).minimize(loss)
                # train_op = tf.train.GradientDescentOptimizer(self.lr).minimize(loss)
                train_op = tf.train.AdamOptimizer(self.lr).minimize(loss)

            inter_value = {
                'probs': probs,
                'entropies': entropies
            }
        
        return train_op, loss, word_vectors, caption, caption_mask, inter_value

    def build_generator(self):
        with tf.name_scope("Sequence_Generator"):
            word_vectors = tf.placeholder(tf.float32, [1, self.n_encode_lstm_step, self.dim_wordvec])

            word_vectors_flat = tf.reshape(word_vectors, [-1, self.dim_wordvec])
            wordvec_emb = tf.nn.xw_plus_b(word_vectors_flat, self.encode_vector_W, self.encode_vector_b)
            wordvec_emb = tf.reshape(wordvec_emb, [1, self.n_encode_lstm_step, self.dim_hidden])
            
            state1 = tf.zeros([1, self.lstm1.output_size*2])
            state2 = tf.zeros([1, self.lstm2.output_size*2])
            padding = tf.zeros([1, self.dim_hidden])

            generated_words = []

            probs = []
            embeds = []
            for i in xrange(self.n_encode_lstm_step):
                if i > 0:
                    tf.get_variable_scope().reuse_variables()
                
                with tf.variable_scope("LSTM1"):
                    output1, state1 = self.lstm1(wordvec_emb[:, i, :], state1)
                
                with tf.variable_scope("LSTM2"):
                    output2, state2 = self.lstm2(tf.concat([padding, output1], 1), state2)

            for i in xrange(0, self.n_decode_lstm_step):
                tf.get_variable_scope().reuse_variables()

                if i == 0:
                    with tf.device('/cpu:0'):
                        current_embed = tf.nn.embedding_lookup(self.Wemb, tf.ones([1], dtype=tf.int64))

                with tf.variable_scope("LSTM1"):
                    output1, state1 = self.lstm1(padding, state1)

                with tf.variable_scope("LSTM2"):
                    output2, state2 = self.lstm2(tf.concat([current_embed, output1], 1), state2)

                logit_words = tf.nn.xw_plus_b(output2, self.embed_word_W, self.embed_word_b)
                max_prob_index = tf.argmax(logit_words, 1)[0]
                generated_words.append(max_prob_index)
                probs.append(logit_words)

                with tf.device("/cpu:0"):
                    current_embed = tf.nn.embedding_lookup(self.Wemb, max_prob_index)
                    current_embed = tf.expand_dims(current_embed, 0)

                embeds.append(current_embed)

        return word_vectors, generated_words, probs, embeds
