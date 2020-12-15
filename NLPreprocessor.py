# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 01:20:50 2020

@author: Eduardo Vicente and Isabel Carvalho
"""

from wordspell_corrector import *
from NLPyPort.FullPipeline import *
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize as tokenize
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import floresta
import joblib
from nltk import word_tokenize

question_words = ['que','quanto','quantos','cujo','cujos','quem','onde','quando','como','por','qual','quais','para','em']


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
    endoffile = 'EOS'
    filtered = []

    for w in words:
        if w is not endoffile and w not in punctuation and w not in white_space:
            filtered.append(w)

    return filtered


def remove_stopwords(words):
    filtered = []
    # print("STOP:\n")
    # print(words)
    stop_words = set(stopwords.words('portuguese'))
#    print(stop_words)

    for w in words:
        # print(w+"\n")
        if w.lower() not in question_words:
            if w not in stop_words:
                filtered.append(w)
        else:
            filtered.append(w)

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
def autocorrect(tokens):
    arr = []
    print(tokens)
    for t in tokens:
        if t.isalpha() and t != "EOS":
            arr.append(correction(t))
    print(arr)
    return arr

def NLPyPort_transform(msg):

    options = {
			"tokenizer" : True,
			"pos_tagger" : True,
			"lemmatizer" : True,
			"entity_recognition" : True,
			"np_chunking" : True,
			"pre_load" : False,
			"string_or_array" : True
    }
    text = new_full_pipe(msg,options=options)
    dic_pos = dict()
    tags = text.pos_tags


    #SAVE POS_TAGS POSITIONS
    for i in range(len(tags)):
        dic_pos[text.lemas[i]] = tags[i]


    #PRINT PARAMETERS FROM TEXT:

    # if(text!=0):
    #   print("TOKENS: "+ str(text.tokens)+" \n")
    #   print("POS_TAG: "+ str(text.pos_tags)+" \n")
    #   print("ENTITIES: "+ str(text.entities)+" \n")
    #   print("NP_TAGS: "+ str(text.np_tags)+" \n")

    filtered = autocorrect(text.tokens)

    #FIND GREETING WORDS ->
    [greeting,idx_g] = find_greeting(filtered)

    #FIND THANKFULL WORDS ->
    [thanks,idx_t] = find_thanks(filtered)

    filtered = text.lemas

    #REMOVE PONCTUATION NOISE and EOS
    filtered = remove_noise(filtered)
    #REMOVE STOPWORDS
    filtered = remove_stopwords(filtered)

    # TRADUZ ACENTOS
    filtered = translate(filtered)

    arr_tag = []
    for i in range(len(filtered)):
        if filtered[i] in list(dic_pos.keys()):
            arr_tag.append(dic_pos[filtered[i]])

    return [greeting,thanks,filtered,arr_tag]

def Spacy_NLP_transform(msg):


    ##RETURN A TUPLE LIKE -> (greetings,thanks,[vector of tokens],[pos_tag],extra_info (target))
    nlp = spacy.load("pt_core_news_lg")
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

    # TRADUZ ACENTOS
    filtered = translate(filtered)

    #STEMMING & LEMMATIZATION
    filtered = stemming_lemmatization(filtered,nlp)

    #PART-OF-SPEECH TAG POS
    pos_tag = part_of_speech(filtered,nlp)
    print(pos_tag)
    #BAG OF WORDS
    # bagwords = bag_of_words(filtered)

    return [greeting,thanks,filtered,pos_tag]


def translate(words):
    acentos = ["padrão", "preço", "recomendações", "decoração",
               "classificação", "estação", "médio", "pétala", "tranças",
               "acrílico", "botão", "geométrico", "pendão", "caída",
               "algodão", "único", "pólo", "império", "íntimo", "boémia",
               "médio-alto", "verão", "laço", "coração", "botões",
               "alças", "três", "lã", "poliéster", "sintético", "pérolas",
               "sólido", "impressão", "calças", "calções"]
    traducao = ["padrao", "preco", "recomendacoes", "decoracao",
                "classificacao", "estacao", "medio", "petala", "trancas",
                "acrilico", "botao", "geometrico", "pendao", "caida",
                "algodao", "unico", "polo", "imperio", "intimo", "boemia",
                "medio-alto", "verao", "laco", "coracao", "botoes",
                "alcas", "tres", "la", "poliester", "sintetico", "perolas",
                "solido", "impressao", "calcas", "calcoes"]
    filtered = []

    for word in words:
        i = 0
        for i in range(len(acentos)):
            if word == acentos[i]:
                filtered.append(traducao[i])
                continue
        filtered.append(word)

    return filtered


def preprocess_msg(msg,type_nlp):

    if type_nlp:
        return NLPyPort_transform(msg)
    else:
        return Spacy_NLP_transform(msg)
    # print(arr_tag)



# preprocess_msg("Ola, estou a procura de uma camisola para a minha filha.")