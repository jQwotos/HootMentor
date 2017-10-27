# path to training data
training_data_path = 'data/conversations_lenmax22_formersents2_with_former'
filters = "+++$+++"

# path to all_words
all_words_path = './data/all_words.txt'

# training parameters 

train_model_path = 'saver/model/RL/'
train_model_name = 'model-RL'

save_model_path= 'ouput/'

start_epoch = 56
start_batch = 0
batch_size = 25

# for RL training
training_type = 'pg' # 'normal' for seq2seq training, 'pg' for policy gradient
reversed_model_path = 'saver/model/reversed'
reversed_model_name = 'mode-Reversed'

# data reader shuffle index list
load_list = False
index_list_file = 'data/shuffle_index_list'
cur_train_index = start_batch * batch_size

# word count threshold
WC_threshold = 20
reversed_WC_threshold = 6


# dialog simulation turns
MAX_TURNS = 10

dull_set = ["I don't know what you're talking about.", "I don't know.", "You don't know.", "You know what I mean.", "I know what you mean.", "You know what I'm saying.", "You don't know anything."]
