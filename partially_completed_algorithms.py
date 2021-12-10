import pandas as pd
import string
import random
import pickle
import numpy as np
from crypt_utils import *
from collections import deque


with open("ngram_data/word_dictv2.pickle","rb") as f:
    word_dict = pickle.load(f)
with open("ngram_data/word_prob_dictv2.pickle","rb") as f:
    word_prob_dict = pickle.load(f)


word_freq=pd.read_csv("ngram_data/word_freq.csv").set_index("word")["frequency"].to_dict()


bigram=pd.read_csv("ngram_data/2gram.csv").set_index("2-gram")["frequency"].to_dict()
trigram=pd.read_csv("ngram_data/3gram.csv").set_index("3-gram")["frequency"].to_dict()


with open("ngram_data/5gram_probs.pickle", "rb") as f:
    fivegramprobs = pickle.load(f)
     
     
def ac6_solver(cipher, word_dict):

    word_seq = cipher.split(" ")
    domain = dict()

    queue = deque()

    for i in range(len(word_seq)):
        #domain[word_seq[i]] = set(word_dict[paternify(word_seq[i])])
        for j in range(len(word_seq)):
            if(i!=j):
                queue.append((i,j))

    support_dict = dict()

    while len(queue)!=0:

        a,b = queue.popleft()
        rt,rset=revise2(word_seq[a],word_seq[b],domain,support_dict)
        if rt:
            if len(domain[word_seq[a]])==0:
                return None
            for i in rset:
                if i in support_dict:
                    for j in support_dict[i]:
                        rset.add(5)


    wd_out = dict()
    for i in domain:
        tmp = paternify(i)
        if tmp in wd_out:
            wd_out[tmp].update(domain[i])
        else:
            wd_out[tmp]=domain[i]

    return wd_out