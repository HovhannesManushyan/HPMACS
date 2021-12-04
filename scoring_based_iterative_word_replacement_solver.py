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


with open("ngram_data/5gram_probs.pickle", "rb") as f:
    fivegramprobs = pickle.load(f)


actual_key = "badcfehgjilkonmrqputsxwvzy"
# plaintext =  "key quick brown jumps over lazy dog the fox"
plaintext = "sentence that definitely has a unique solution"
# plaintext = "world science technology"
cipher = encrypt(plaintext,actual_key)

def solver(cipher, word_dict, ngram_probs):
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
            sol = cipher.translate(cor_assign)
            solutions.append((sol, get_score(sol,ngram_probs, word_freq)))

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


print(solver(cipher,word_dict,fivegramprobs))