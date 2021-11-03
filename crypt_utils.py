import pandas as pd
import string
import random
import pickle
import numpy as np

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