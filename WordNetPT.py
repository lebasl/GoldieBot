# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 23:23:30 2020

@author: Eduardo Vicente
"""
import requests, ast


def encode_aux(string):
    
    return string.encode('latin1').decode('utf-8')

def remove_duplicates(lista):
    
    return list(dict.fromkeys(lista))

    
    
def process_content(content):
    
    conteudo = str(content)
    conteudo = conteudo.split("'")
    
    l = ast.literal_eval(conteudo[1])
    return l    


def synsets(word):
   
    URL_search ="http://wordnet.pt/api/por/search/"
    URL_synset ="http://wordnet.pt/api/por/synset/"
    r =  requests.get(URL_search+word)
    # print(r.encoding)

    l = process_content(r.content)
    # print(l)
    sin = list()
   
    if len(l) > 0:
        for i in range(len(l)):
            
            ss = encode_aux(str(l[i]))
            
            r2 = requests.get(URL_synset+ss)
            l2 = process_content(r2.content)

            if len(l2) > 0:
                
                for j in range(len(l2)):
                    strx = encode_aux(str(l2[j]))
                    sin.append(strx)
                    
            else:
                # print("Não deu!")
                return []
            # sin.append()
            # print(r2.content)
    else:
        # print("Não deu!")
        return []
    return remove_duplicates(sin)
        
print(synsets("camisola"))
##Testes com encoding

# x = 'mo\xc3\x83\xc2\xa7a'

# print(x.encode('ascii').decode('iso-8859-1'))
















