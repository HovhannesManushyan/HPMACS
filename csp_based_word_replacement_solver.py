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
     

# hard cipher emv qsjdl apmwn isoru mxfp kbyz cmh tgf
actual_key = "badcfehgjilkonmrqputsxwvzy"
# plaintext =  "quick brown jumps over lazy fox dog the"
# plaintext = "sentence that definitely has a unique solution"
plaintext = "world and most important depth technology science"
# plaintext = "fly can fly mosqito can mosqito"
cipher = encrypt(plaintext,actual_key)


def ac3_solver(cipher, word_dict):

    key = string.ascii_lowercase
    word_seq = cipher.split(" ")
    domain = dict()

    queue = deque()

    for i in range(len(word_seq)):
        domain[word_seq[i]] = set(word_dict[paternify(word_seq[i])])
        for j in range(len(word_seq)):
            if(i!=j):
                queue.append((i,j))

    

    while len(queue)!=0:

        a,b = queue.popleft()        
        if revise(word_seq[a],word_seq[b],domain):
            if len(domain[word_seq[a]])==0:
                return None
            for i in range(len(word_seq)):
                if(i!=a):
                    queue.append((a,i))

    wd_out = dict()
    for i in domain:
        tmp = paternify(i)
        if tmp in wd_out:
            wd_out[tmp].update(domain[i])
        else:
            wd_out[tmp]=domain[i]
    return wd_out

res_domain=ac3_solver(cipher,word_dict)
    

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
            solutions.append((sol, get_score(sol,ngram_probs,word_freq)))
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
    print(sorted(solutions,key=lambda x: x[1])[-1])
    if len(solutions) == 0:
        return -float("inf")
    else:
        return max([i[1] for i in solutions])


if __name__=="__main__":
    print(solver(cipher,res_domain,fivegramprobs))


