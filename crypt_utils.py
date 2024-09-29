import string
import numpy as np
from collections import OrderedDict

def encrypt(plaintext, key):
    """
    Encrypt plaintext using a substitution cipher with the given key.

    Parameters:
    - plaintext (str): The message to encrypt.
    - key (str): A 26-character string representing the substitution key where
                 key[i] is the cipher letter for plaintext letter 'a' + i.

    Returns:
    - cipher (str): The encrypted message.
    """
    trans = str.maketrans(string.ascii_lowercase, key)
    cipher = plaintext.translate(trans)
    return cipher

def decrypt(ciphertext, key):
    """
    Decrypt ciphertext using a substitution cipher with the given key.

    Parameters:
    - ciphertext (str): The message to decrypt.
    - key (str): A 26-character string representing the substitution key where
                 key[i] is the cipher letter for plaintext letter 'a' + i.

    Returns:
    - plaintext (str): The decrypted message.
    """
    trans = str.maketrans(key, string.ascii_lowercase)
    plaintext = ciphertext.translate(trans)
    return plaintext

def paternify(instr):
    """
    Generates a pattern string for the input word. Each unique letter is assigned
    a unique lowercase letter starting from 'a'.

    Parameters:
    - instr (str): The input word.

    Returns:
    - pattern (str): The pattern string.
    """
    ht = dict()
    pattern = ""
    cnt = 97  # ASCII value for 'a'
    for i in instr.lower():
        if i in ht:
            pattern += ht[i]
        else:
            pattern += chr(cnt)
            ht[i] = chr(cnt)
            cnt += 1
    return pattern

def isconsistent(assignment, cipher_word, plain_word):
    """
    Checks if the current assignment is consistent with mapping cipher_word to plain_word.

    Parameters:
    - assignment (dict): Current mapping from cipher letter ordinals to plain letter ordinals.
    - cipher_word (str): The cipher word.
    - plain_word (str): The candidate plain word.

    Returns:
    - bool: True if consistent, False otherwise.
    """
    for c, p in zip(cipher_word.lower(), plain_word.lower()):
        c_ord = ord(c)
        p_ord = ord(p)
        if c_ord in assignment:
            if assignment[c_ord] != p_ord:
                return False
        elif p_ord in assignment.values():
            return False
    return True

def get_assignment(cipher_word, plain_word):
    """
    Generates a mapping from cipher letters to plain letters based on the word pair.

    Parameters:
    - cipher_word (str): The cipher word.
    - plain_word (str): The candidate plain word.

    Returns:
    - dict: Mapping from cipher letter ordinals to plain letter ordinals.
    """
    trans = dict()
    for c, p in zip(cipher_word.lower(), plain_word.lower()):
        c_ord = ord(c)
        p_ord = ord(p)
        trans[c_ord] = p_ord
    return trans

def build_key_from_mapping(mapping):
    """
    Build the key string for decryption from cipher_ord to plain_ord mapping.

    Parameters:
    - mapping (dict): Mapping from cipher letter ord to plain letter ord.

    Returns:
    - key_str (str): 26-character key string where key[i] is the plain letter for 'a' + i.
                      Unmapped letters are represented by '_'.
    """
    key = ['_'] * 26  # Initialize with '_' for unmapped letters
    reverse_mapping = {}
    for cipher_ord, plain_ord in mapping.items():
        plain_char = chr(plain_ord)
        cipher_char = chr(cipher_ord)
        reverse_mapping[plain_char] = cipher_char

    for i in range(26):
        plain_char = chr(ord('a') + i)
        if plain_char in reverse_mapping:
            key[i] = reverse_mapping[plain_char]
        else:
            key[i] = '_'  # Use '_' for unmapped letters

    return ''.join(key)


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