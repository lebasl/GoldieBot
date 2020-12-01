# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 01:20:50 2020

@author: Eduardo Vicente and Isabel Carvalho
"""

import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize as tokenize
import spacy
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import floresta


def find_greeting(words):
    greetings = ['olá','ola', 'oi', 'boas', 'hey', 'viva', 'saudacoes','saudações',
                 'cumprimentos']
    greeting = 0
    idx=-1
    for w in words:
        if w.lower() in greetings:
            greeting = 1
            idx = words.index(w)
            break

    return greeting,idx


def find_thanks(words):
    thanks = ['obrigado', 'obrigada', 'grato', 'grata', 'agradecido',
              'agradecida', 'brigado', 'brigada', 'ty', 'thanks',
              'thank you', 'gracias', 'agradecimentos']
    thank = 0
    idx = -1
    for w in words:
        if w.lower() in thanks:
            thank = 1
            idx = words.index(w)
            break

    return thank,idx



def remove_noise(words):
    punctuation = string.punctuation
    white_space = string.whitespace
    filtered = []

    for w in words:
        if w not in punctuation and w not in white_space:
            filtered.append(w)

    return filtered


def remove_stopwords(words):
    filtered = []
    stop_words = set(stopwords.words('portuguese'))
#    print(stop_words)

    for w in words:
        if w not in stop_words:
            filtered.append(w)

    return filtered


def remove_all(words):
    filtered = remove_noise(words)
    filtered = remove_stopwords(words)
    return filtered


def part_of_speech(words,nlp):
    
    
    pos_tag = []
    
    # using spacy pt
    
    
    for w in words:  
        
        for token in nlp(w):
            #valor a nivel semantico das palavras
            pos = token.pos_
            pos_tag.append(pos)
            
    return pos_tag


def stemming_lemmatization(words,nlp):
    filtered = []

    for w in words:
               
        for token in nlp(w):
            # encontra root de cada palavra 
            w = token.lemma_
            filtered.append(w)
           
    
    return filtered

def bag_of_words(words):
    vectorizer = CountVectorizer()
    # encontra o numero de vezes que cada palavra e usada
    bag = vectorizer.fit_transform(words)
    # valor da coluna 0 e o indice da primeira ocorrencia
    df = pd.DataFrame(bag.todense(), columns=vectorizer.get_feature_names())

    # print(df)

    return df


def preprocess_msg(msg):
    
    ##RETURN A TUPLE LIKE -> (greetings,thanks,[vector of tokens],[pos_tag],extra_info (target))
    nlp = spacy.load('C:\\Users\\Eduardo Vicente\\Anaconda3\\Lib\\site-packages\\pt_core_news_lg\\pt_core_news_lg-2.3.0')

    #TOKENIZER -TOKENIZE WORDS/ELEMENTS IN THE MESSAGE STATMENT
    tokens = tokenize(msg)
    # print(tokens)
    
    #FIND GREETINGS ->
    [greeting,idx_g] = find_greeting(tokens)
    if greeting == 1:
        tokens.pop(idx_g)
    #FIND THANKFULL WORDS ->
    [thanks,idx_t] = find_thanks(tokens)
    if thanks == 1:
        tokens.pop(idx_t)
    # REMOVE WORDS ^ INDEX (GREETING OR THANKS) -> WE NEED TO PASS THIS INFORMATION FOR THE MSG CONSTRUCTOR
    
   
    #REMOVE WHITESPACES AND PONCTUACTION ELEMENTS
    filtered = remove_noise(tokens)
    
    #REMOVE STOPWORDS 
    filtered = remove_stopwords(filtered)
        
    #STEMMING & LEMMATIZATION
    filtered = stemming_lemmatization(filtered,nlp)
    
    #PART-OF-SPEECH TAG POS
    pos_tag = part_of_speech(filtered,nlp)
    print(pos_tag)
    #BAG OF WORDS 
    # bagwords = bag_of_words(filtered)
        
    return [greeting,thanks,filtered,pos_tag]



# preprocess_msg("Ola, estou a procura de uma camisola para a minha filha.")