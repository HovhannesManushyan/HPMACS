import string
import random
import numpy as np
from collections import OrderedDict

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
        elif ord(j) in assignment.values():
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


def gen_ordered_dict(a,b):

    foc_dict = dict()
    mp_dict = OrderedDict()
    for index,key in enumerate(a):
        if key not in mp_dict:
            foc_dict[key]=index

    for index, key in enumerate(b):
        if key in foc_dict:
            if foc_dict[key] in mp_dict:
                mp_dict[foc_dict[key]].append(index)
            else:
                mp_dict[foc_dict[key]]=[index]
    return mp_dict

def check_consistency(word1,word2, ord_dict):
    for i,j in ord_dict.items():
        for c in j:
            if word1[i]!=word2[c]:
                return False

    return True

def revise(word1,word2,domain):

    ord_dict = gen_ordered_dict(word1,word2)
    
    rm_set = set()
    revised = False
    for i in domain[word1]:
        tmp = False

        for j in domain[word2]:
            if check_consistency(i,j,ord_dict):
                tmp=True
                break

        if tmp==False:
            rm_set.add(i)
            revised = True

    domain[word1] = domain[word1]-rm_set

    return revised  
