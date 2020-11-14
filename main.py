# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import rdflib
import pprint
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize as tokenize
# from nltk import SnowballStemmer as snowball
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random


def dataset():
    data = pd.read_csv("PT Attribute Dataset.csv", delimiter=';', header=0)
    data = data.astype(str)
    artigos = data.itertuples(index=False, name='Artigo')

    rdf = rdflib.Graph()

    for row in artigos:
        for i in range(1, 14):
            rdf.add((rdflib.URIRef(row[0]), rdflib.URIRef(data.columns[i]),
                     rdflib.Literal(row[i])))

    s = rdf.serialize(format='nt').decode("utf-8")
    print(s)


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

    for w in words:
        if w not in stop_words:
            filtered.append(w)

    return filtered
    stop_words = set(stopwords.words('portuguese'))
    filtered = []

    for w in words:
        if w not in stop_words:
            filtered.append(w)

    return filtered


def stemming(words):
    filtered = []
    pos_tag = []
    # stemmer = nltk.stem.RSLPStemmer()
    # stemmer = snowball('portuguese', ignore_stopwords=True)

    # using spacy pt
    nlp = spacy.load("pt_core_news_lg")
    for w in words:
        for token in nlp(w):
            # w = stemmer.stem(w)
            w = token.lemma_
            filtered.append(w)
            pos = token.pos_
            pos_tag.append(pos)
            # print(w)
            # print(pos)

    return [filtered, pos_tag]


def bag_of_words(words):
    ocurrences = []

    return ocurrences


def find_greeting(words):
    greetings = ['ola', 'oi', 'boas', 'hey', 'viva', 'saudacoes',
                 'cumprimentos']
    greeting = 0

    for w in words:
        if w in greetings:
            greeting = 1
            break

    return greeting


def find_thanks(words):
    thanks = ['obrigado', 'obrigada', 'grato', 'grata', 'agradecido',
              'agradecida', 'brigado', 'brigada', 'ty', 'thanks',
              'thank you', 'gracias', 'agradecimentos']
    thank = 0

    for w in words:
        if w in thanks:
            thank = 1
            break

    return thank


def output_generator(question, sentences, greeting, thank):
    greetings = ['ola', 'oi', 'boas', 'hey', 'viva', 'saudacoes',
                 'cumprimentos']
    thanks = ['de nada', 'ora essa', 'o prazer foi todo meu', 'sem problema',
              'estou aqui para ajudar']

    answer = ''
    sentences.append(question)
    # tokenizer e a funcao que vai ser usada para remover pontuacao etc
    TfidVec = TfidfVectorizer(tokenizer=remove_noise,
                              stop_words=stopwords.words('portuguese'))
    # transforma em Tf-idf-weighted matrix
    tfidf = TfidVec.fit_transform(sentences)
    # similaridade entre sentences e question
    values = cosine_similarity(tfidf[-1], tfidf)
    # array de indices para ordenar
    index = values.argsort()[0][-2]
    # ordenar por row matrix
    flat = values.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    # se nao ha qualquer similaridade entre a pergunta e o texto (sentences)
    if req_tfidf == 0:
        if greeting:
            answer += random.choice(greetings)
            answer += ' '
        answer = 'Nao percebi, que me queres dizer?'
    else:
        if greeting:
            answer += random.choice(greetings)
            answer += ' '
        if thank:
            answer += random.choice(thanks)
            answer += ' '
        # vai buscar a resposta mais similar
        answer += sentences[index]

    return answer
    thanks = ['obrigada', 'obrigado', 'gracias', 'ty', 'thanks', 'grato',
              'grata', 'agradecido', 'agradecida']
    thank = 0

    for w in words:
        if w in thanks:
            thank = 1
            break

    return thank


def input_processing(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    raw = f.read()
    raw = raw.lower()

    # answer = []
    filtered = []
    pos_tag = []
    greeting = 0
    thanks = 0
    pos_greetings = []
    pos_thanks = []
    j = 0

    # PACKAGES NECESSARIAS
    # nltk.download('punkt')
    # nltk.download('wordnet') N USADA
    # nltk.download('rslp') N USADA

    for line in lines:
        line = line.lower()
        tokens = tokenize(line)

        # isto aqui e para as respostas!!!!!!!!!!!!!!!!!!!!!!!
        sentences = nltk.sent_tokenize(line, language='portuguese')
        words = nltk.word_tokenize(line, language='portuguese')

        # procura cumprimento
        greeting = find_greeting(tokens)
        # se encontrar guarda o indice da linha
        if greeting:
            pos_greetings.append(j)

        # procura agradecimento
        thanks = find_thanks(tokens)
        # se encontrar guarda o indice da linha
        if thanks:
            pos_thanks.append(j)

        # identificar question words?

        # remove whitespace e pontuacao
        filtered = remove_noise(tokens)
        # remove palavras irrelevantes
        filtered = remove_stopwords(filtered)
        # stemming e pos tagging
        [filtered, pos_tag] = stemming(filtered)

        # for i in range(0, len(filtered)):
        #     print(filtered[i])
        #     print(pos_tag[i])

        # deteta ocorrencia de cada palavra
        # bagwords = bag_of_words(filtered)

        # gera resposta
        # SENTENCES TEM DE SER AS RESPOSTAS POSSIVEIS, OU INFO DE ONDE AS TIRAR
        output_generator(filtered, sentences, greeting, thanks)

        j += 1

    # for w in filtered:
    #     print(w)
    #     # imprime valor no indice correspondente do bagwords

    return filtered

    # atencao a acentos
    # question words

    # fuck, e se escrevem tshirt em vez de t-shirt e essas merdas? (sweat em
    # vez de sweatshirt, calcao em vez de calcoes) bue merdas lel


def find_intention(filtered):
    # regras
    # ex. se encontra onde responde com a localizacao da loja
    return


if __name__ == '__main__':
    filename = 'inputs.txt'
    filtered = input_processing(filename)
    find_intention(filtered)
