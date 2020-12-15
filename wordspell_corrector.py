# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 03:13:13 2020

@author: Eduardo Vicente
"""
import re
from collections import Counter
def words(text): 
    return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))
words2 = []
def prepare_file():
    
    freq_file = open('word_freq.txt','r',encoding="utf-8")
    new_file = open('new_words.txt','w')
    
    for line in freq_file.readlines():
        line = line.split("\t")
        freq = int(line[0])
        word2 = str(line[1].split("\n")[0])
        words2.append(word2.lower())
        new_file.write(word2+"\n")
    freq_file.close()
    new_file.close()
    
def P(word, N=sum(WORDS.values())): 
    
    freq_file = open('word_freq.txt','r',encoding="utf-8")
    flag = 0
    for line in freq_file.readlines():
        line = line.split("\t")
        freq = int(line[0])
        word2 = str(line[1].split("\n")[0])
        if word == word2:
            flag=1
            res = freq
    if flag==0:
        res = WORDS[word]/N
    "Probability of `word`."
    return res

def correction(word): 
    "Most probable spelling correction for word."
    # print(candidates(word))
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    print(known2(word))
    return (known2(word) or known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def known2(w): 
    
    if w.lower() in words2:
        return set(w)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZàÁáÂâÃãõôÕÔÉÊêèÈéÍíçÇ'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

# print(correction("Olá"))
