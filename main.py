# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import rdflib
import pprint
import nltk
from nltk.corpus import stopwords

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


def input_file(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        print(line)

if __name__ == '__main__':
    filename = 'inputs.txt'
    input_file(filename)
    # remover pontuacao, simbolos, etc
    # atencao a acentos
    # print(stopwords.words('portuguese'))
    