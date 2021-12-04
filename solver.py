import pandas as pd
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


with open("ngram_data/5gram_probs.pickle", "rb") as f:
    fivegramprobs = pickle.load(f)


def encrypt(plaintext,key):
    trans = plaintext.maketrans(key,string.ascii_lowercase)
    cipher = plaintext.translate(trans)
    return cipher

def decrypt(ciphertext,key):
    trans = ciphertext.maketrans(string.ascii_lowercase,key)
    cipher = ciphertext.translate(trans)
    return cipher

def paternify(instr):
    ht = dict()
    pattern = ""
    cnt = 97
    for i in instr:
        if i in ht:
            pattern = pattern + ht[i]
        else:
            pattern = pattern + chr(cnt)
            ht[i]=chr(cnt)
            cnt = cnt + 1
    return pattern

def bigram_score(instring,bigram):
    prob = None
    for i,j in zip(instring, instring[1:]):
        if i+j in bigram:
            if prob==None:
                prob = np.log(bigram[i+j])
            else:
                prob=prob + np.log(bigram[i+j])
        
    return prob

def trigram_score(instring,trigram):
    prob = None
    for i,j,z in zip(instring, instring[1:],instring[2:]):
        if i+j+z in trigram:
            if prob==None:
                prob = np.log(trigram[i+j+z])
            else:
                prob=prob + np.log(trigram[i+j+z])
        
    return prob

def word_score(instring,word_freq):
    oov_score = np.log(10**(-10))
    words = instring.split(" ")
    prob = 0
    for i in words:
        if i in word_freq:
            prob += np.log(word_freq[i])
        else:
            prob += oov_score
            
    return prob

def transify(str1,str2):
    trans = dict()
    
    fxu = list(set(str1)-set(str2))
    fxl = list(set(str2)-set(str1))
    
    for i,j in zip(str1,str2):
        if ord(i) not in trans:
            trans[ord(i)]=ord(j)
    
    for i,j in zip(fxu,fxl):
        trans[ord(j)]=ord(i)

    return trans

def isconsistent(assignment,pattern, word):

    for i,j in zip(pattern,word):
        if ord(i) in assignment:
            if assignment[ord(i)]!=ord(j):
                return False
        elif ord(j) in assignment.values(): # avoids the case when letter is assigned to a different value
            return False
            
    return True

def get_assignment(word1,word2):
    trans = dict()
    for i,j in zip(word1,word2):
        if i not in trans:
            trans[ord(i)]=ord(j)
    return trans


def assignment_trans(assignment):
    
    vl = set(assignment.values())
    ks = set(assignment.keys())
    
    fxu = list(ks - vl)
    fxl = list(vl - ks)
    
    for i,j in zip(fxu,fxl):
        assignment[j]=i

    return assignment


def get_score(charseq, ngram_probs, word_frequency):
    totprob = 0
    words = charseq.split(" ")
    sz = len(list(ngram_probs.keys())[0])
    eps = np.log(1e-9)

    for i in words:
        if i in word_frequency:
            totprob += np.log(word_frequency[i])
        else:
            totprob += eps

    for i in range(len(charseq)-sz+1):
        cprob = ngram_probs.get(charseq[i:i+sz],0)
        if cprob == 0:
            totprob += eps
        else:
            totprob += np.log(cprob)

    return totprob


def get_scorev2(charseq, ngram_probs,):
    totprob = 0
    words = charseq.split(" ")
    sz = len(list(ngram_probs.keys())[0])
    eps = np.log(1e-9)

    for i in range(len(charseq)-sz+1):
        cprob = ngram_probs.get(charseq[i:i+sz],0)
        if cprob == 0:
            totprob += eps
        else:
            totprob += np.log(cprob)

    return totprob


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