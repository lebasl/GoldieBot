# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 02:19:14 2020

@author: Eduardo Vicente
"""

import pandas as pd
import rdflib
from rdflib import Namespace, URIRef, Literal
import json


def save_rdf(filename):
    
    #Load Raw Data (CSV format)
    
    data = pd.read_csv(".//DATASET//PT Attribute Dataset v2.csv", delimiter=';', header=0)
    data = data.astype(str)
    
    # forma triplos
    artigos = data.itertuples(index=False, name='Artigo')
    
    #Cria dicionario auxiliar
    dic = dict()
    
    rdf = rdflib.Graph()
    n = Namespace("http://example.org/")


    for row in artigos:
        
        idaux = str(row[0]).lower()
        artigo = URIRef(n[idaux])
 
        for i in range(1, 17):
            
            uaux = str(data.columns[i]).lower()
            u = URIRef(n[uaux])
            
            litaux = str(row[i]).lower()
            l =  Literal(litaux)

            #Adicionar elemento ao Grafo
            rdf.add((artigo, u,l))
            
            
            
            if data.columns[i].lower() in dic and data.columns[i].lower() != "ID" and data.columns[i].lower() != "id":
                dic[data.columns[i].lower()].append(row[i])    
            else:
                if data.columns[i].lower() != "ID" and data.columns[i].lower() != "id":
                    dic[data.columns[i].lower()] = [row[i]]    


    
        # formato nt mostra id - coluna - valor (n-triples)
        # formato turtle mostra junta os pares coluna - valor para cada id
        
    # rdf.serialize(format='nt').decode('utf-8')
    rdf.serialize(destination=filename, format="turtle")
        
    for key in dic.keys():
        lista = dic.get(key)
        aux = list(dict.fromkeys(lista))
        for i in range(len(aux)):
            aux[i] = aux[i].lower()
        
        dic[key] = aux
        
    with open("dict_pred_obj.txt","w") as f:
        f.write(json.dumps(dic))
  
        
# save_rdf("KDB.rdf")