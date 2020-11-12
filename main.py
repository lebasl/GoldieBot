# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import csv
import pandas as pd
import numpy as np
import rdflib
import pprint

from rdflib import Namespace, Graph, Literal, BNode, URIRef
from rdflib.namespace import NamespaceManager, RDF


def translate():
    dados = pd.read_csv("Attribute dadosSet.csv", delimiter=';', header=0)

    dados = dados.replace(np.nan, 'Sem informacao')
    dados = dados.replace('Brief', 'Intimo')
    dados = dados.replace('brief', 'Intimo')
    dados = dados.replace('cute', 'Fofo')
    dados = dados.replace('Cute', 'Fofo')
    dados = dados.replace('bohemian', 'Boemio')
    dados = dados.replace('Bohemian', 'Boemio')
    dados = dados.replace('Novelty', 'Novo')
    dados = dados.replace('novelty', 'Novo')
    dados = dados.replace('Flare', 'Requintado')
    dados = dados.replace('flare', 'Requintado')
    dados = dados.replace('sexy', 'Sensual')
    dados = dados.replace('Sexy', 'Sensual')
    dados = dados.replace('casual', 'Casual')
    dados = dados.replace('vintage', 'Vintage')
    dados = dados.replace('Party', 'Festa')
    dados = dados.replace('party', 'Festa')
    dados = dados.replace('Work', 'Trabalho')
    dados = dados.replace('work', 'Trabalho')
    dados = dados.replace('OL', 'Trabalho')
    dados = dados.replace('Average', 'Medio')
    dados = dados.replace('average', 'Medio')
    dados = dados.replace('Low', 'Baixo')
    dados = dados.replace('low', 'Baixo')
    dados = dados.replace('High', 'Alto')
    dados = dados.replace('high', 'Alto')
    dados = dados.replace('Medium', 'Medio-Alto')
    dados = dados.replace('medium', 'Medio-Alto')
    dados = dados.replace('very-high', 'Muito alto')
    dados = dados.replace('Very-high', 'Muito alto')
    dados = dados.replace('very high', 'Muito alto')
    dados = dados.replace('Very high', 'Muito alto')
    dados = dados.replace('', 'Sem informacao')
    dados = dados.replace('free', 'Tamanho unico')
    dados = dados.replace('small', 'S')
    dados = dados.replace('medium', 'Medio-Alto')
    dados = dados.replace('Automn', 'Outono')
    dados = dados.replace('Autumn', 'Outono')
    dados = dados.replace('Spring', 'Primavera')
    dados = dados.replace('spring', 'Primavera')
    dados = dados.replace('Summer', 'Verao')
    dados = dados.replace('summer', 'Verao')
    dados = dados.replace('Winter', 'Inverno')
    dados = dados.replace('winter', 'Inverno')
    dados = dados.replace('backless', 'Sem costas')
    dados = dados.replace('boat-neck', 'U')
    dados = dados.replace('bowneck', 'Laco')
    dados = dados.replace('halter', 'Alcas')
    dados = dados.replace('mandarin-collor', 'Mandarim')
    dados = dados.replace('NULL', 'Sem informacao')
    dados = dados.replace('o-neck', 'O')
    dados = dados.replace('open', 'Aberto')
    dados = dados.replace('peterpan-collor', 'Peter Pan')
    dados = dados.replace('ruffled', 'Folhos')
    dados = dados.replace('Scoop', 'Colher')
    dados = dados.replace('slash-neck', 'Bateau')
    dados = dados.replace('sqare-collor', 'Quadrado')
    dados = dados.replace('Sweetheart', 'Coracao')
    dados = dados.replace('sweetheart', 'Coracao')
    dados = dados.replace('turndowncollor', 'Botoes')
    dados = dados.replace('v-neck', 'V')
    dados = dados.replace('butterfly', 'Borboleta')
    dados = dados.replace('cap-sleeves', 'Muito curta')
    dados = dados.replace('capsleeves', 'Muito curta')
    dados = dados.replace('full', 'Comprida')
    dados = dados.replace('half', 'Meia')
    dados = dados.replace('halfsleeve', 'Meia')
    dados = dados.replace('Petal', 'Petala')
    dados = dados.replace('short', 'Curta')
    dados = dados.replace('sleeevless', 'Nenhuma')
    dados = dados.replace('sleeveless', 'Nenhuma')
    dados = dados.replace('sleevless', 'Nenhuma')
    dados = dados.replace('threequarter', 'Tres Quartos')
    dados = dados.replace('threequater', 'Tres Quartos')
    dados = dados.replace('thressqatar', 'Tres Quartos')
    dados = dados.replace('turndowncollor', 'Botoes')
    dados = dados.replace('urndowncollor', 'Botoes')
    dados = dados.replace('dropped', 'Caida')
    dados = dados.replace('empire', 'Imperio')
    dados = dados.replace('natural', 'Natural')
    dados = dados.replace('princess', 'Princesa')
    dados = dados.replace('acrylic', 'Acrilico')
    dados = dados.replace('cashmere', 'Caxemira')
    dados = dados.replace('silk', 'Seda')
    dados = dados.replace('cotton', 'Algodao')
    dados = dados.replace('knitting', 'Malha')
    dados = dados.replace('lace', 'Renda')
    dados = dados.replace('linen', 'Linho')
    dados = dados.replace('lycra', 'Licra')
    dados = dados.replace('microfiber', 'Microfibra')
    dados = dados.replace('milksilk', 'Seda de leite')
    dados = dados.replace('mix', 'Variados')
    dados = dados.replace('modal', 'Seda artificial')
    dados = dados.replace('model', 'Seda artificial')
    dados = dados.replace('rayon', 'Seda artificial')
    dados = dados.replace('nylon', 'Nylon')
    dados = dados.replace('other', 'Outros')
    dados = dados.replace('polyster', 'Poliester')
    dados = dados.replace('shiffon', 'Sintetico')
    dados = dados.replace('chiffonfabric', 'Sintetico')
    dados = dados.replace('spandex', 'Spandex')
    dados = dados.replace('viscos', 'Viscose')
    dados = dados.replace('wool', 'La')
    dados = dados.replace('batik', 'Batik')
    dados = dados.replace('broadcloth', 'Pano grosso')
    dados = dados.replace('chiffon', 'Seda')
    dados = dados.replace('shiffon', 'Seda')
    dados = dados.replace('Corduroy', 'Veludo')
    dados = dados.replace('dobby', 'Pano')
    dados = dados.replace('flannael', 'Flanela')
    dados = dados.replace('flannel', 'Flanela')
    dados = dados.replace('jersey', 'Malha')
    dados = dados.replace('knitted', 'Malha')
    dados = dados.replace('knitting', 'Malha')
    dados = dados.replace('lace', 'Renda')
    dados = dados.replace('organza', 'Organza')
    dados = dados.replace('other', 'Outros')
    dados = dados.replace('poplin', 'Poplin')
    dados = dados.replace('satin', 'Cetim')
    dados = dados.replace('sattin', 'Cetim')
    dados = dados.replace('terry', 'Terry')
    dados = dados.replace('tulle', 'Tule')
    dados = dados.replace('wollen', 'La')
    dados = dados.replace('woolen', 'La')
    dados = dados.replace('worsted', 'La')
    dados = dados.replace('applique', 'Apliques')
    dados = dados.replace('beading', 'Perolas')
    dados = dados.replace('pearls', 'Perolas')
    dados = dados.replace('bow', 'Laco')
    dados = dados.replace('button', 'Botao')
    dados = dados.replace('cascading', 'Cascata')
    dados = dados.replace('crystal', 'Cristal')
    dados = dados.replace('draped', 'Em cortina')
    dados = dados.replace('embroidary', 'Bordado')
    dados = dados.replace('feathers', 'Penas')
    dados = dados.replace('flowers', 'Flores')
    dados = dados.replace('hollowout', 'Buracos')
    dados = dados.replace('lace', 'Renda')
    dados = dados.replace('none', 'Nada')
    dados = dados.replace('plain', 'Liso')
    dados = dados.replace('pleat', 'Prega')
    dados = dados.replace('pockets', 'Bolsos')
    dados = dados.replace('rivet', 'Rivet')
    dados = dados.replace('ruched', 'Dobras')
    dados = dados.replace('ruffles', 'Folhos')
    dados = dados.replace('sashes', 'Faixa')
    dados = dados.replace('sequined', 'Lantejoulas')
    dados = dados.replace('tassel', 'Pendao')
    dados = dados.replace('Tiered', 'Camadas')
    dados = dados.replace('animal', 'Animal')
    dados = dados.replace('character', 'Personagem')
    dados = dados.replace('dot', 'Pontos')
    dados = dados.replace('floral', 'Floral')
    dados = dados.replace('geometric', 'Geometrico')
    dados = dados.replace('leapord', 'Leopardo')
    dados = dados.replace('leopard', 'Leopardo')
    dados = dados.replace('patchwork', 'Mistura')
    dados = dados.replace('plaid', 'Xadrez')
    dados = dados.replace('print', 'Impressao')
    dados = dados.replace('solid', 'Solido')
    dados = dados.replace('splice', 'Trancas')
    dados = dados.replace('striped', 'Riscas')

    dados.to_csv('PT Attribute dadosset.csv', sep=';')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # translate()
    data = pd.read_csv("PT Attribute Dataset.csv", delimiter=';', header=0)
    data = data.astype(str)
    artigos = data.itertuples(index=False, name='Artigo')
    # for row in artigos:
    #     print(row)

    rdf = rdflib.Graph()

    # n = Namespace("http://example.org/")
    # flag = 0
    for row in artigos:
    #     n[row[0]]
    #     # id = BNode()
        for i in range(1, 14):

            # rdf.add((URIRef(row[0]), RDF.subject, URIRef(n[row[0]])))
            # rdf.add((URIRef(row[0]), RDF.predicate, n[data.columns[i]]))
            # rdf.add((URIRef(row[0]), RDF.object, Literal(row[i])))

            # print('\nIndex '+ row[0])
            # print('Column ' + data.columns[i])
            # print('Value ' + row[i])

            rdf.add((rdflib.URIRef(row[0]), rdflib.URIRef(data.columns[i]), rdflib.Literal(row[i])))
            # if (i == 13):
            #     flag = 1
            # if (not flag):
            #     n[data.columns[i]]

            # rdf.add(n[row[0]], n[data.columns[i]], Literal(row[i]))


    # for nt in rdf:
    #     pprint.pprint(nt)

    # formato nt mostra id - coluna - valor (n-triples)
    # formato turtle mostra junta os pares coluna - valor para cada id
    # s = rdf.serialize(format='nt').decode("utf-8")
    # # print(s)
    # pprint.pprint(rdf.value(subject=None, predicate='Preco', object='Baixo'))

    # s = rdf.serialize(format='turtle').decode("utf-8")
    # graph = rdflib.Graph()
    # graph = graph.parse(data=rdf, format='turtle')
    # sub = rdf.predicate_objects('200')
    # pprint.pprint(sub)

    # Subject e o ID do artigo
    # subjects = rdf.subjects(predicate=None, object=None)
    # for subject in subjects:
    #     print(subject)

    # Predicate e a Coluna (Padrao, Tecido, Preco...)
    # predicates = rdf.predicates(subject=None, object=None)
    # for predicate in predicates:
    #     print(predicate)

    # Object e o valor do predicado (Solido, Algodao, Medio...)
    # objects = rdf.objects(predicate=None, subject=None)
    # for object in objects:
    #     print(object)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
