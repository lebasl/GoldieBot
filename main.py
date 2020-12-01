# -*- coding: utf-8 -*-

from onto_test import synsets as onto_syn

import pandas as pd
import rdflib
from NLPyPort.FullPipeline import *
from NLPyPort.LemPyPort import *
import nltk
from nltk.stem import SnowballStemmer as snowball
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize as tokenize
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random





def find_intention(question, response):
    # analisa a pergunta e ve qual parte da resposta o user quer

    # ver question words

    answer = response.split(',')
    if 'onde' in question:
        return answer[2]

    response = 'artigo'
    response += answer[0]
    return response

###################################################################################
#####################################OUTPUT########################################
###################################################################################

def test_dataset(filename):
    dataset = []
    f = open(filename, 'r')
    
    lines = f.read().split('.')
    
    i = 0
    for line in lines:
        
        line = line.lower()
        dataset.insert(i, line)
        i += 1

    f.close()

    return dataset


def output_generator(question, dataset, greeting, thank):
    greetings = ['ola', 'oi', 'boas', 'hey', 'viva', 'saudacoes',
                 'cumprimentos']
    thanks = ['de nada', 'ora essa', 'o prazer foi todo meu', 'sem problema',
              'estou aqui para ajudar']

    #answer = ''
    pergunta = ''
    response = ''

    # question tem de estar no formato str apenas
    for i in range(len(question)):
        pergunta += question[i]
        pergunta += ' '
    dataset.append(pergunta)

    vectorizer = TfidfVectorizer()
    vectorizer.set_params(lowercase=False)

    # importancia das palavras do dataset - importante para poder fazer cosine
    # similarity que exige matrizes do mesmo tamanho
    tfidf = vectorizer.fit_transform(dataset)
    # converter a matriz para dataframe
    # features = vectorizer.get_feature_names()
    # df = pd.DataFrame(tfidf.todense(), columns=features)
    # print(df)

    # similaridade entre dataset e question
    values = cosine_similarity(tfidf[-1], tfidf)
    # print(pergunta)
    # print(values)
    # print(values)
    # array de indices para ordenar por values
    index = values.argsort()[0][-2]
    # ordenar o array
    flat = values.flatten()
    flat.sort()

    # FALTA CONSIDERAR SITUACAO EM QUE HA MAIS QUE UM VALUES
    # IGUAIS (como esta usa o ultimo encontrado)

    # value mais alto (sem contar o correspondente a pergunta em si)
    similaridade = flat[-2]

    # se nao ha qualquer similaridade entre a pergunta e o dataset
    if similaridade == 0:
        if greeting:
            response += random.choice(greetings)
            response += ' '
        response = 'Nao percebi, que me queres dizer?'
    else:
        # answer = find_intention(question, dataset[index])
        if greeting:
            response += random.choice(greetings)
            response += ' '
        if thank:
            response += random.choice(thanks)
            response += ' '
        # vai buscar a resposta que retornou o value mais similar
        # analisa a pergunta e devolve a parte da resposta que o user quer
        # response += answer
        response += dataset[index]

    return response

###################################################################################
#######################################MAIN########################################
###################################################################################


if __name__ == '__main__':
    
    
    # PACKAGES NECESSARIAS
    # nltk.download('wordnet')
    # nltk.download('omw')
    #nltk.download('floresta')
    # nltk.download('rslp') N USADA
    
    filename = 'inputs.txt'
    f = open(filename, 'r')
    
    lines = f.readlines()
    
    
    filtered = []
    pos_tag = []
    pos_greetings = []
    pos_thanks = []
    
    greeting = 0
    thanks = 0
    j = 0
    
    answer = ''
    
    print(onto_syn("castanho"))

    # # dataset onde vai buscar as respostas
    # teste = test_dataset('teste.txt')

    # for line in lines:
    #     line = line.lower()
    #     print(line)
        

    
    #     tokens = tokenize(line)
    #     # #print(tokens)

    #     # # procura cumprimento
    #     greeting = find_greeting(tokens)
        
    #     # # # procura agradecimento
    #     thanks = find_thanks(tokens)

    #     # # # se encontrar guarda o indice da linha
    #     if greeting:
    #         pos_greetings.append(j)

    #     # # # se encontrar guarda o indice da linha
    #     if thanks:
    #         pos_thanks.append(j)

    #     # # remove whitespace e pontuacao
    #     filtered = remove_noise(tokens)
    #     # # print(filtered)
    #     # # # remove palavras irrelevantes
    #     filtered = remove_stopwords(filtered)
    #     # # print(filtered)
        
    #     pos_tag = part_of_speech(filtered)
        
    #     print(pos_tag)
    #     for i in range(0, len(pos_tag)):
    #         if(pos_tag[i]=="NOUN"):
    #             if(filtered[i][-1]=='o'):
    #                 filtered.append('M')
    #             elif(filtered[i][-1]=='a'):
    #                 filtered.append('F')
    #     #      print(filtered[i])
        
    #     # # # stemming e pos tagging
    #     # [filtered, pos_tag] = stemming(filtered)
    #     print(filtered)
        

        # deteta ocorrencia de cada palavra
        # bagwords = bag_of_words(filtered)
        
        # res = wn.synset('dog').lemma_names('por')
        # for result in wordnet.synsets("filha",lang='por'):
        # x = wn.lemmas('cane',lang='ita')
        
        #print(ptext3.similar('chegar'))
        # x2 = wn.synsets("invernar",lang='por')[0].lemma_names('por')
        # print(x2)
        
        # x2 = wn.synsets("inverno",lang='por')[0].lemma_names('por')
        # print(x2)
        
 

        # gera resposta a partir do dataset
        # answer = output_generator(filtered, teste, greeting, thanks)

        # print('para a pergunta')
        # print(line)
        # print('responde')
        # print(answer)
        # print('\n')

        # a pergunta do inverno da erro porque o stemming muda a
        # palavra para invernar :(

    # j += 1
        # j usado no pos_greeting e pos_thanks

    f.close()

    # atencao a acentos
    # usar wordnet para p.ex. traduzir filho para M