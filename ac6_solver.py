import pandas as pd
import string
import random
import pickle
import numpy as np
from crypt_utils import *
from collections import deque, defaultdict
import copy

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
    domains = {}
    supports = {}
    queue = deque()

    # Initialize domains and supports
    for word in word_seq:
        pattern = paternify(word)
        if pattern in word_dict:
            domains[word] = set(word_dict[pattern])
        else:
            return None  # No possible substitutions for this word

    # Initialize supports and queue
    for xi in word_seq:
        supports[xi] = {}
        for a in domains[xi]:
            supports[xi][a] = {}
            for xj in word_seq:
                if xi != xj:
                    supports[xi][a][xj] = set()
                    for b in domains[xj]:
                        if is_arc_consistent(xi, a, xj, b):
                            supports[xi][a][xj].add(b)
                    if not supports[xi][a][xj]:
                        # No support for (xi, a) with xj
                        queue.append((xi, a, xj))

    # AC-6 Algorithm
    while queue:
        xi, a, xj = queue.popleft()
        # Remove a from the domain of xi
        domains[xi].discard(a)
        if not domains[xi]:
            return None  # Domain wipeout
        for xk in word_seq:
            if xk != xi:
                for c in domains[xk]:
                    if (xi not in supports[xk][c]) or (a in supports[xk][c][xi]):
                        supports[xk][c][xi].discard(a)
                        if not supports[xk][c][xi]:
                            queue.append((xk, c, xi))

    # Prepare the output domain
    wd_out = {}
    for word in domains:
        pattern = paternify(word)
        if pattern in wd_out:
            wd_out[pattern].update(domains[word])
        else:
            wd_out[pattern] = domains[word]
    return wd_out

def is_arc_consistent(xi, a, xj, b):
    # Check if assignment a for xi is consistent with assignment b for xj
    return isconsistent({}, xi, a) and isconsistent({}, xj, b) and check_consistency(a, b, gen_ordered_dict(xi, xj))

def solver(cipher, word_dict, ngram_probs):
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
            print(sol)
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


    if len(solutions) == 0:
        return -float("inf")
    else:
        return max([i[1] for i in solutions])

if __name__ == "__main__":
    actual_key = "badcfehgjilkonmrqputsxwvzy"
    plaintext = "sentence that definitely has a unique solution"
    cipher = encrypt(plaintext, actual_key)

    res_domain = ac6_solver(cipher, word_dict)
    if res_domain is not None:
        print(solver(cipher, res_domain, fivegramprobs))
    else:
        print(-float("inf"))
