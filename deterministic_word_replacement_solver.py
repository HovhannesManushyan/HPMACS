import pandas as pd
import string
import random
import pickle
import numpy as np
from crypt_utils import *

with open("ngram_data/word_dict.pickle","rb") as f:
    word_dict = pickle.load(f)
with open("ngram_data/word_prob_dict.pickle","rb") as f:
    word_prob_dict = pickle.load(f)
    
word_freq=pd.read_csv("ngram_data/word_freq.csv").set_index("word")["frequency"].to_dict()

bigram=pd.read_csv("ngram_data/2gram.csv").set_index("2-gram")["frequency"].to_dict()
trigram=pd.read_csv("ngram_data/3gram.csv").set_index("3-gram")["frequency"].to_dict()

actual_key = "badcfehgjilkonmrqputsxwvzy"
plaintext = "sentence that definitely has a unique solution"
cipher = encrypt(plaintext,actual_key)

def solver(cipher, word_dict):
    key = string.ascii_lowercase
    word_seq = cipher.split(" ")
    
    solutions = []
    partial_solutions=[]
    
    que = []
    que.append((0,{}))
    while len(que)!=0:
        
        index, assignment = que.pop()
        if index >= len(word_seq):
            cor_assign = assignment_trans(assignment)
            solutions.append(cipher.translate(cor_assign))
            print(cipher.translate(cor_assign))

        else:
            values = word_dict[paternify(word_seq[index])]
            was_assign = False
            for sub_word in values:
                if isconsistent(assignment,word_seq[index],sub_word):
                    cassignment = dict()
                    cassignment.update(assignment)
                    cassignment.update(get_assignment(word_seq[index],sub_word))
                    que.append((index+1,cassignment))
                    was_assign=True
            if was_assign==False:
                cor_assign = assignment_trans(assignment)
                partial_solutions.append(cipher.translate(cor_assign))
    
    return (solutions,partial_solutions)

solver(cipher,word_dict)