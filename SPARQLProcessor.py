# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 23:11:32 2020

@author: Eduardo Vicente
"""

import pandas as pd
import rdflib
from rdflib import Graph, Namespace
import rdflib.plugins.sparql as SPARQL
import json


def load_dict(filename):
        
    with open(filename,'r') as f:
        dict_pred_obj = json.load(f)

    return dict_pred_obj



def load_rdf(filename):
    
    graph = Graph()
    graph.parse(filename, format="turtle")
    
    return graph
    

def process_nlp_input(nlp_values):
    
    print(nlp_values[2])
    
    return ""

def do_sparql_query(dic,rdf_graph):
    
    results = []
    response = ""
    ns1 = Namespace("http://example.org/")
    q_header = "SELECT ?s WHERE { "
    q_foot = "}"
    where_feat = []
    for key,value in dic.items():
        where_feat.append('?s ns1:'+key+" '"+value+"' "+". ")
    
    for i in range(len(where_feat)):
        q_header = q_header + where_feat[i]
        
        
    q_final= q_header + q_foot
    
    pretty_res = {}
    
    for row in rdf_graph.query(q_final):    
       
        x = str(row).split("'")[1]
        y = x.split("/")[3]
        results.append(y)  
    
    if len(results) == 1:
        print(results[0])
        response = "1 Artigo Encontrado:\n"+"ID: "+results[0] + ""
   
    elif len(results) == 0:
        response = "Nenhum Artigo Encontrado :(\n"
    
    else:
        response = "Vários Artigos Encontrados:\nID's:"
        for i in range(len(results)):
            response = response + results[i]+"|"

    return response
        

def sparql_query(keywords):
    
    #save_rdf('demo.rdf')
    
    dictx = load_dict('dict_pred_obj.txt')
    # print(dictx)
    
    rdf_graph = load_rdf('KDB.rdf')
    # print(rdf_graph)
    success = 0
    
    ##SEARCH FOR SIMILARITY IN THE DICT OF PREDICATES AND OBJECTS
    query_dict = {}
    for k in keywords:
        for key,values in dictx.items():
            if k in values:
                query_dict[key]=k
    
    if(len(query_dict.keys()) > 0):
        success = 1
        
    response = do_sparql_query(query_dict,rdf_graph) 
    
    
    return response

# print(sparql_query(['polo','m',]))