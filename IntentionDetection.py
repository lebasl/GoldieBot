# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 20:10:11 2020

@author: Eduardo Vicente
"""
import random
from SPARQLProcessor import *
from OntoPT import *
import json


termin = ['ar','er','ir','or','ur']

question_words = ['que','quanto','quantos','cujo','cujos','quem','onde','quando','como','por','qual','quais','para','em']

verbs_quando = ['conseguir','poder','fazer','ver','mandar','começar',
                'tentar','deixar','pedir','vir','continuar','pretender'
                ,'solicitar','comprar','encomendar','chegar','receber',
                'despachar','enviar','acabar','cancelar','parar','sair']

verbs_search = ['encontrar','achar','descobrir','obter','conseguir','achar','ter','possuir','arranjar','sondar','intencionar','tencionar','pesquisar','rastrear','tentar','procurar','encontrar','encomendar','querer']
 
verbs_onde = ['localizar','ficar','pertencer','estar','manter','ser','existir','haver',
                'conseguir','poder','fazer','ver','mandar','começar',
                'tentar','deixar','pedir','vir','continuar','pretender'
                ,'solicitar','comprar','encomendar','chegar','receber','despachar','enviar','acabar',
                'cancelar','parar','sair']

encomendas_prep_resp =['Iniciada a encomenda, o processo só pode ser cancelado via telefone com um Operador','Quando quiser!\nPara encomendar a peça de roupa desejada necessita apenas de carregar no botão sobre o produto que diz "Colocar no Carrinho"\nAutomaticamente o produto é colocado na lista de produtos a comprar no carrinho. Depois apenas tem de prosseguir normalmente com a encomenda!','Pode consultar todos os detalhes acerca das suas encomendas na Área Pessoal, ou então consultar os recibos eletrónicos via email','As encomendas chegam em 2-3 dias úteis, pode consultar e ver o trajeto da sua encomenda em Área Pessoal > Recibos/Encomendas']
encomendas2_prep_resp = ['Pode consultar-me a mim ou então utilizar a nossa ferramenta de pesquisa integrada com os mais sofisticados filtros']
localizacao_prep_resp = ['A loja encontra-se fisicamente instalada na Rua Adolfo Loureiro, Edificio nº 34','Estamos situados em Coimbra','Possuimos uma loja fisica situada em Coimbra e virtualmente neste dominio']

# verbo ter!!!
##PRONOMES ADJETIVOS INTERROGATIVOS
#que -> (que carro é aquele? ) -> SCONJ
#Quanto -> PRON
#cujo -> PRON

##PRONOMES SUBJANTIVOS INTERROGATIVOS
#QUEM -> PRON

#quem + ser; 


#que -> (o que ...) PRON
    #IR-RDF ->
    
    
    #!IR-RDF -> 
                
                
#quantos -> PRON

##ADVERBIOS INTERROGATIVOS

#onde (lugar)-> ADV

    #IR-RDF -> onde + encontrar(*); onde + haver
    
    
    #!IR-RDF -> onde + ser;  
                #onde + estar; onde + encontrar(*)
                #onde + ficar; onde + manter;
                #onde + existir; onde + localizar;
                #onde + pertencer;

#quando (tempo)-> ADV


    #IR-RDF ->
    
    #!IR-RDF -> quando + sair; quando + receber;
              

#como (modo) -> ADV
#por que (razão/causa)-> ADV
#para que (objectivo/finalidade) -> SCONJ

##TARGET VERBOS
#procurar,encontrar,comprar,vender
#fabricar,produzir,custar,servir,haver

#recebe -> filtered , tag_pos




#NO RDF INFORMATION:
def no_IR_info(filtered,pos_tag):
    
    
    
    
    
    return ""


def detect(filtered,pos_tag):
    
    sin_loja = synsets("loja")
    response = ""
    #SPLIT INTO QUESTION-WORD AND ARGS
    left = []
    i=0
    
    if len(filtered) > 0:
        while i < len(filtered):
            
            if filtered[i].lower() in question_words:
                q_type = filtered[i].lower()
                filtered.pop(i)
                pos_tag.pop(i)
            i = i + 1         
        
        # print(pos_tag)
        # print(q_type)
        
        if q_type == question_words[0]:
            print("xD1")
            
            
        elif q_type == question_words[1]:
            print("xD2")
       
        
        elif q_type == question_words[2]:
            print("xD3")
        
        elif q_type == question_words[3]:
            print("xD4")
       
        
        elif q_type == question_words[4]:
            print("xD5")
        elif q_type == question_words[5]:
            print("xD6")
            
            #ONDE
        elif q_type == question_words[6]:
                 # print("xD8")
             cancela = 0
             local = 0
             info_2 = 0
             pesquisa = 0
             #LOOK FOR VERBS
             verb_aux = []
             for i in range(len(filtered)):
                 v = pos_tag[i]
                 if v =='VERB':
                    v_aux = filtered[i]
                         
                    if v_aux in verbs_onde[-4:]:
                        cancela = 1
                    elif v_aux in verbs_onde[0:4]:
                        print(verbs_onde[0:4])
                        local = 1
                    elif v_aux in verbs_search:
                        pesquisa = 1
                    else:
                        info_2 = 1
                             
             if cancela:
                response = "" + encomendas_prep_resp[0] 
                
             elif local:
                response = "" + random.choice(localizacao_prep_resp[:])
                
             elif pesquisa:
                 store=0
                 non_verbs = []
    
                 for i in range(len(filtered)):
                     x = pos_tag[i]
                     print(x)
                     if x != 'VERB':
                         y = filtered[i].lower()
                         
                         if y[-2:] not in termin:
                             print(y)
                             non_verbs.append(y)
                             print(non_verbs)
                             if y == "loja" or y in sin_loja:
                                store = 1
                             
                 if store:
                     response = "" +  random.choice(localizacao_prep_resp[:])
                 else:
                     print(non_verbs)
                     
                     results = sparql_query(non_verbs)
                     response = results
                     # print("RDF Loading...")
                     
                                       
             elif info_2:
                response = "" + random.choice(encomendas2_prep_resp[:])
                
             else:
                response = "Desculpe não entendi, ainda estou a aprender... :("
             
             
             #QUANDO
        elif q_type == question_words[7]:
             # print("xD8")
             cancela = 0
             info_1 = 0
             info_2 = 0
             #LOOK FOR VERBS
             verb_aux = []
             for i in range(len(filtered)):
                 v = pos_tag[i]
                 if v =='VERB':
                     v_aux = filtered[i]
                     if v_aux in verbs_quando:
                         
                         if v_aux in verbs_quando[-4:]:
                             cancela = 1
                         elif v_aux in verbs_quando[:5]:
                             print(verbs_quando[:5])
                             info_1 = 1
                         else:
                             info_2 = 1
                             
             if cancela:
                response = "" + encomendas_prep_resp[0] 
             elif info_1:
                response = "" + encomendas_prep_resp[1]
             elif info_2:
                response = "" + random.choice(encomendas_prep_resp[2:])
             else:
                response = "Desculpe não entendi, ainda estou a aprender... :("
                
        elif q_type == question_words[8]:
             print("xD9")
        elif q_type == question_words[9]:
            print("xD11")
        elif q_type == question_words[10]:
            print("xD12")
        elif q_type == question_words[11]:
            print("xD13")
        elif q_type == question_words[12]:
            print("xD14")
        elif q_type == question_words[13]:
            print("xD15")
        else:
            print("xDnull")
        
        return response

    else:
        return
      
    
            
# print(detect(['Quando', 'chegar', 'pedir'], ['ADV', 'VERB', 'VERB']))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

