import pandas as pd
from crypt_utils import *
import string
import random
import pickle
import numpy as np


with open("ngram_data/word_dict.pickle","rb") as f:
    word_dict = pickle.load(f)
with open("ngram_data/word_prob_dict.pickle","rb") as f:
    word_prob_dict = pickle.load(f)


word_freq=pd.read_csv("ngram_data/word_freq.csv").set_index("word")["frequency"].to_dict()
bigram=pd.read_csv("ngram_data/2gram.csv").set_index("2-gram")["frequency"].to_dict()
trigram=pd.read_csv("ngram_data/3gram.csv").set_index("3-gram")["frequency"].to_dict()


actual_key = "badcfehgjilkonmrqputsxwvzy"
plaintext = "from bucharest to zambia to zaire ozone zones make zebras run zany zigzags"
cipher = encrypt(plaintext,actual_key)



def solve(cipher,word_dict,word_prob_dict):
    key=string.ascii_lowercase
    plaintext=decrypt(cipher,key)
    best_score = word_score(plaintext,word_freq)

    for i in range(10000):
        word_seq = plaintext.split(" ")
        len_seq = np.array([len(i) for i in word_seq])
        len_seq = len_seq/sum(len_seq)
        rnd_word = np.random.choice(word_seq,p=len_seq)
        
        rnd_word_pattern = paternify(rnd_word)
        word_sub_prob=word_prob_dict[rnd_word_pattern]/np.sum(word_prob_dict[rnd_word_pattern])
        
        sub_word = np.random.choice(word_dict[rnd_word_pattern],p=word_sub_prob)
        trans = transify(rnd_word,sub_word)
        mod_key = key.translate(trans)
        mod_plaintext=decrypt(cipher,mod_key)
        if(word_score(mod_plaintext,word_freq)>best_score):
            key=mod_key
            plaintext=mod_plaintext
            best_score=word_score(mod_plaintext,word_freq)
            print(best_score,plaintext)
        
        
        
solve(cipher,word_dict,word_prob_dict)







