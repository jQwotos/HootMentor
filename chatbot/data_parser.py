import pickle 
import numpy as np 
import codecs 
import config
import os 
import re
import types

def pre_build_word_vocab(word_count_threshold=5,all_words_path=config.all_words_path): 
    """
        pre-processing the data into word vector
        args-> (int, string)
        
        word_count_threshold: bucket size for vectorizes
        all_words_path: path to file contain all of the words
    """

    # if the words haven't tokenizes
    if not os.path.exists(all_words_path):
        parse_all_words (all_words_path,config.filters)
    corpus = open(all_words_path, 'r').read().split('\n')[:-1]
    captions = np.asarray(corpus, dtype=np.object)

    captions = map(lambda x: x.replace('.', ''), captions)
    captions = map(lambda x: x.replace(',', ''), captions)
    captions = map(lambda x: x.replace('"', ''), captions)
    captions = map(lambda x: x.replace('\n', ''), captions)
    captions = map(lambda x: x.replace('?', ''), captions)
    captions = map(lambda x: x.replace('!', ''), captions)
    captions = map(lambda x: x.replace('\\', ''), captions)
    captions = map(lambda x: x.replace('/', ''), captions)

    print('preprocessing word counts and creating vocab based on word count threshold %d' % (word_count_threshold))
    word_counts = {}
    nsents = 0
    for sent in captions:
        nsents += 1
        for w in sent.lower().split(' '):
           word_counts[w] = word_counts.get(w, 0) + 1
    vocab = [w for w in word_counts if word_counts[w] >= word_count_threshold]
    print('filtered words from %d to %d' % (len(word_counts), len(vocab)))

    ixtoword = {}
    ixtoword[0] = '<pad>'
    ixtoword[1] = '<bos>'
    ixtoword[2] = '<eos>'
    ixtoword[3] = '<unk>'

    wordtoix = {}
    wordtoix['<pad>'] = 0
    wordtoix['<bos>'] = 1
    wordtoix['<eos>'] = 2
    wordtoix['<unk>'] = 3

    for idx, w in enumerate(vocab):
        wordtoix[w] = idx+4
        ixtoword[idx+4] = w

    word_counts['<pad>'] = nsents
    word_counts['<bos>'] = nsents
    word_counts['<eos>'] = nsents
    word_counts['<unk>'] = nsents

    bias_init_vector = np.array([1.0 * word_counts[ixtoword[i]] for i in ixtoword])
    bias_init_vector /= np.sum(bias_init_vector) # normalize to frequencies
    bias_init_vector = np.log(bias_init_vector)
    bias_init_vector -= np.max(bias_init_vector) # shift to nice numeric range

    return wordtoix, ixtoword, bias_init_vector


def parse_all_words(destination_path,filters,text_path='./data/movie_lines.txt'):
    """
        parse all of the text into destination_path from texts(text_path)
            (destination , filter_applied_on_each_line , text_path)
            
        destination: the final destiation of the words 
        filter: splitting uneed filter from the string 
        text_path: text that will be encoding from 
    """
    lines= open(text_path,'r',encoding='utf-8',errors='ignore').read().split('\n')[:-1]
    assert isinstance(filters,str)
    with codecs.open(destination_path,"w",encoding='utf-8',errors='ignore') as f:
        for line in lines:
            # apply filter if needed 
            if(filters):
                line = line.split(filters)
            utterance = line[-1]
            f.write(utterance+'\n')

def default_filter(words):
    '''
        default filter that applied on sepcific datasets 
        words: words that will be applied
    '''
    words = ["".join(word.split("'")) for word in words]
    # words = ["".join(word.split("'")) for word in words]    
    data = ' '.join(words)
    return data 

def refine(data,filters = default_filter):
    '''
        refine the vocabulary into a fixed concurrent sequnence
        
        data: The data that will be refine with

        filters: filter function to join up the intened form  
    '''
    # find all of the path that are matching the pattern
    words = re.findall("[a-zA-Z'-]+", data)
    # assert the filters is a function 
    assert isinstance(filters,types.FunctionType)
    data =filters(words)
    return data

# Testing the data parser  
# if __name__ == '__main__':
#     parse_all_words(config.all_words_path,filters='+++$+++')
    
    