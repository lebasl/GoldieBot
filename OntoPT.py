# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 03:05:47 2020

@author: Eduardo Vicente
"""
import requests
import re,string
from nltk.corpus import stopwords

def find_uppercase(a_str):
    for c in a_str:
        if c in string.ascii_uppercase:
            return True
    return False
    
 
def remove_stopwords(words):
    filtered = []
    stop_words = set(stopwords.words('portuguese'))
#    print(stop_words)

    for w in words:
        if w not in stop_words:
            filtered.append(w)

    return filtered

def synsets(word):
    
    payload = {"pesquisa":word}
    r = requests.get("http://ontobusca.dei.uc.pt:8080/ontobusca/ServletXML",params=payload)
    # print(r.html)
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, ' ', r.text)
    
    
    punctuation = string.punctuation
    white_space = string.whitespace
    
    for c in cleantext:
       # print(c)
       if c in punctuation or c in white_space:
           # print("omg")
           cleantext = cleantext.replace(c," ")
       
    arr = cleantext.split(" ")   
    # print(arr)
    for w in arr:
        if find_uppercase(w):
            arr.remove(w)
    
    # print(arr)
    str_list = list(filter(None, arr))
    # print(str_list)
    
    final = remove_stopwords(str_list)
    return final

