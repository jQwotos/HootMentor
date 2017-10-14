from config import *
import sys 
import os 
import time 
import math 
import tensorflow as tf
from tensorflow.python.platform import gfile
import numpy as np
import gst_rnn_model
import grl_rnn_model
import data_utils
import config
import pickle
import os.path


# batchsize x inputsize 

def prepare_data(config):
    pass 


def create_rl_model(session,config,forward_only,name_scope):
    with tf.variable_scope(name_or_scope=name_scope):
        rl_model=grl_rnn_model (config,name_scope,forward=forward_only)

        # post trainning progression show
        ckpt = tf.train.get_checkpoint_state(os.path.join(config.train_dir, "checkpoints"))
        if ckpt and tf.train.checkpoint_exists(ckpt.model_checkpoint_path):
            print("Read %s model from %s" % (name_scope, ckpt.model_checkpoint_path))
            rl_model.saver.restore(session, ckpt.model_checkpoint_path)
        else:
            print("Creating %s model with fresh parameters" % name_scope)
            global_variables = [gv for gv in tf.global_variables() if name_scope in gv.name]
            session.run(tf.variables_initializer(global_variables))
            print("Created %s model with fresh parameters" % name_scope)
        return rl_model

def train():
    vocab, rev_vocab, dev_set, train_set = prepare_data(grl_config)
    for b_set in train_set:
        print("b_set length: ", len(b_set))

    with tf.Session() as sess:
        st_model = create_st_model(sess, gst_config, True, gst_config.name_model)
        bk_model = create_st_model(sess, gbk_config, True, gbk_config.name_model)
        cc_model = create_st_model(sess, gcc_config, True, gcc_config.name_model)
        rl_model = create_rl_model(sess, grl_config, False, grl_config.name_model)

        train_bucket_sizes = [len(train_set[b]) for b in range(len(grl_config.buckets))]
        train_total_size = float(sum(train_bucket_sizes))
        train_buckets_scale = [sum(train_bucket_sizes[:i + 1]) / train_total_size
                               for i in range(len(train_bucket_sizes))]

        step_time, loss = 0.0, 0.0
        current_step = 0
        previous_losses = []
        step_loss_summary = tf.Summary()
        # merge = tf.merge_all_summaries()
        rl_writer = tf.summary.FileWriter(grl_config.tensorboard_dir, sess.graph)
        while True:
            random_number_01 = np.random.random_sample()
            bucket_id = min([i for i in range(len(train_buckets_scale)) if train_buckets_scale[i] > random_number_01])

            # Get a batch and make a step.
            start_time = time.time()
            encoder_inputs, decoder_inputs, target_weights, batch_source_encoder, _ = \
                rl_model.get_batch(train_set,bucket_id)

            updata, norm, step_loss = rl_model.step_rl(sess, st_model=st_model, bk_model=bk_model, encoder_inputs=encoder_inputs,
                                               decoder_inputs=decoder_inputs, target_weights=target_weights,
                                               batch_source_encoder=batch_source_encoder, bucket_id=bucket_id)

            step_time += (time.time() - start_time) / grl_config.steps_per_checkpoint
            loss += step_loss / grl_config.steps_per_checkpoint
            current_step += 1

            # Once in a while, we save checkpoint, print statistics, and run evals.
            if current_step % grl_config.steps_per_checkpoint == 0:

                bucket_value = step_loss_summary.value.add()
                bucket_value.tag = grl_config.name_loss
                bucket_value.simple_value = float(loss)
                rl_writer.add_summary(step_loss_summary, int(sess.run(rl_model.global_step)))

                # Print statistics for the previous epoch.
                perplexity = math.exp(loss) if loss < 300 else float('inf')
                print ("global step %d learning rate %.4f step-time %.2f perplexity "
                       "%.2f" % (rl_model.global_step.eval(), rl_model.learning_rate.eval(),
                                 step_time, perplexity))
                # Decrease learning rate if no improvement was seen over last 3 times.
                if len(previous_losses) > 2 and loss > max(previous_losses[-3:]):
                    sess.run(rl_model.learning_rate_decay_op)
                previous_losses.append(loss)
                # Save checkpoint and zero timer and loss.
                gen_ckpt_dir = os.path.abspath(os.path.join(grl_config.train_dir, "checkpoints"))
                if not os.path.exists(gen_ckpt_dir):
                    os.makedirs(gen_ckpt_dir)
                checkpoint_path = os.path.join(gen_ckpt_dir, "chitchat.model")
                rl_model.saver.save(sess, checkpoint_path, global_step=rl_model.global_step)
                step_time, loss = 0.0, 0.0
                # Run evals on development set and print their perplexity.
                # for bucket_id in range(len(gen_config.buckets)):
                #   encoder_inputs, decoder_inputs, target_weights = model.get_batch(
                #       dev_set, bucket_id)
                #   _, eval_loss, _ = model.step(sess, encoder_inputs, decoder_inputs,
                #                                target_weights, bucket_id, True)
                #   eval_ppx = math.exp(eval_loss) if eval_loss < 300 else float('inf')
                #   print("  eval: bucket %d perplexity %.2f" % (bucket_id, eval_ppx))
                sys.stdout.flush()
        pass