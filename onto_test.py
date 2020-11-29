# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 03:05:47 2020

@author: Eduardo Vicente
"""
import requests
import re,string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize as tokenize

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

payload = {"pesquisa":"Inverno"}
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
print(final)





# print(cleantext)
# cln = cleantext.replace(',', '')
# cln = cln.replace('.','')
# cleantext = remove_noise(cleantext)
# print(cleantext)
# tokens = tokenize(cleantext)


# print(cleantext)
# filtered = remove_stopwords(cleantext)
# print(filtered)

# for i in range(len(cleantext)-1):
    
#     # print(cleantext[i])
#     if cleantext[i] == '':
#         cleantext.remove(cleantext[i])    
#     # if "De" or "Se" in word:
#     #     cleantext.remove(word)
    
# print(cleantext[0])
# print(cleantext)
