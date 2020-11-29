# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 23:11:32 2020

@author: Eduardo Vicente
"""

import pandas as pd
import rdflib
from rdflib import Graph, Namespace, URIRef, Literal
import rdflib.plugins.sparql as SPARQL
import csv
import json
#import nltk
# import string
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize as tokenize
# import spacy
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import random


def save_rdf(filename):
    
    data = pd.read_csv("PT Attribute Dataset v2.csv", delimiter=';', header=0)
    data = data.astype(str)
    # forma triplos
    artigos = data.itertuples(index=False, name='Artigo')
    # for row in artigos:
    #     print(row)
    dic = dict()
    res = dict()
    rdf = rdflib.Graph()
    # rdf = rdflib.ConjunctiveGraph()
    
    n = Namespace("http://example.org/")
    # flag = 0
    for row in artigos:
        artigo = URIRef(n[row[0]])
        #     n[row[0]]
        #     # id = BNode()
        for i in range(1, 17):
            
            u = URIRef(n[data.columns[i]])
            # print(data.columns[i])
            rdf.add((artigo, u, Literal(row[i])))
            
            if data.columns[i].lower() in dic and data.columns[i].lower() != "ID" and data.columns[i].lower() != "id":
                dic[data.columns[i].lower()].append(row[i])    
            else:
                if data.columns[i].lower() != "ID" and data.columns[i].lower() != "id":
                    dic[data.columns[i].lower()] = [row[i]]    


    
        # formato nt mostra id - coluna - valor (n-triples)
        # formato turtle mostra junta os pares coluna - valor para cada id
    # rdf.serialize(format='nt').decode('utf-8')
    rdf.serialize(destination=filename, format="turtle")
    
    # for key,value in dic.items():
    #     print(value)
    #     print(res.values())
    #     if value not in res.values():
    #         res[key] = value
    
    for key in dic.keys():
        lista = dic.get(key)
        aux = list(dict.fromkeys(lista))
        for i in range(len(aux)):
            aux[i] = aux[i].lower()
        
        dic[key] = aux
        
    # print(dic)
    with open("dict_pred_obj.txt","w") as f:
        f.write(json.dumps(dic))
  
        
        
def load_dict(filename):
    
    # with open('dict_pred_obj.csv',mode='r') as infile:
    #     reader = csv.reader(infile)
    #     mydict = {rows[0]:rows[1] for rows in reader}
    # reader = csv.DictReader(open(filename))
    # dictobj = next(reader)
    
    # with open(filename, 'w') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #         print(row.keys())
    
    with open(filename,'r') as f:
        dict_pred_obj = json.load(f)
    


    return dict_pred_obj
    
def load_rdf(filename):
    
    graph = Graph()
    graph.parse(filename, format="turtle")
    
    return graph
    
    

if __name__ == '__main__':
    
    #save_rdf('demo.rdf')
    
    dictx = load_dict('dict_pred_obj.txt')
    # print(dictx)
    
    rdf_graph = load_rdf('demo.rdf')
    # print(rdf_graph)
    
    ####        TESTE DO VALUE DENTRO DO GRAFO
    
    #      x = URIRef('http://example.org/111')   
    #      print(rdf_graph.value(subject=x, predicate=URIRef('http://example.org/Sexo')))


    ####        SPARQL TESTES
  
    # query="""\
    #     SELECT ?Subject 
    #     WHERE { 
    #         ?Subject ns1:Cintura "Natural" .
    #         ?Subject ns1:Classificacao "0" .
    #         ?Subject ns1:Decoracao "Bordado" .
    #         ?Subject ns1:Decote "O" .
    #         ?Subject ns1:Estacao "Primavera" .
    #         ?Subject ns1:Tamanho "S" .
    #         ?Subject ns1:Tecido "Seda" .
    #         ?Subject ns1:Tipo "sweatshirt" .
    #     }"""
        
    # for row in rdf_graph.query(query):
    #     print(row)  
        