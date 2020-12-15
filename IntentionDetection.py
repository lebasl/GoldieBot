# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 20:10:11 2020

@author: Eduardo Vicente
"""
from SPARQLProcessor import sparql_query
from OntoPT import synsets
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
from nltk.corpus import stopwords
import random


question_words = ["quem", "como", "onde", "quando"]

sin_loja = synsets("loja")

verbs_cancelamento = ['acabar', 'cancelar', 'parar', 'sair']

verbs_localizacao = ['localizar', 'ficar', 'pertencer', 'estar']

verbs_como = ['conseguir', 'poder', 'fazer', 'ver', 'mandar']

verbs_quando = ['começar', 'tentar', 'deixar', 'pedir', 'vir', 'continuar',
                'pretender', 'solicitar', 'comprar', 'encomendar', 'chegar',
                'receber', 'despachar', 'enviar']

verbs_search = ['encontrar', 'achar', 'descobrir', 'obter', 'conseguir',
                'achar', 'ter', 'possuir', 'arranjar', 'sondar',
                'intencionar', 'tencionar', 'pesquisar', 'rastrear',
                'tentar', 'procurar', 'encontrar', 'encomendar', 'querer']

verbs_onde = ['manter', 'ser', 'existir', 'haver', 'conseguir', 'poder',
              'fazer', 'ver', 'mandar', 'começar', 'tentar', 'deixar', 'pedir',
              'vir', 'continuar', 'pretender', 'solicitar', 'comprar',
              'encomendar', 'chegar', 'receber', 'despachar', 'enviar']

verbs_changed = 0

# NO RDF INFORMATION:
def no_IR_info(filtered, pos_tag):

    return ""


def find_type(filtered, pos_tag, q_type):
    # LOOK FOR VERBS
    for i in range(len(filtered)):
        v = pos_tag[i]
        if v == 'VERB':
            verb = filtered[i]
            if verb in verbs_cancelamento:
                # cancelar
                return 0
            if q_type == "onde":
                if verb in verbs_localizacao:
                    # localizacao
                    return 1
                elif verb in verbs_search:
                    # pesquisa
                    return find_nouns(filtered, pos_tag, q_type)
                elif verb in verbs_onde:
                    # onde procurar artigos
                    return 2
                else:
                    # pesquisa por similaridade
                    return 5
            elif q_type == "como" or q_type == "quando":
                if verb in verbs_como:
                    # como encomendar
                    return 3
                elif verb in verbs_quando:
                    # detalhes encomenda
                    return 4
                else:
                    # pesquisa por similaridade
                    return 5
            else:
                # se nao tem question word tenta identificar pesquisa
                if verb in verbs_search:
                    return find_nouns(filtered, pos_tag, q_type)
                else:
                    # pesquisa por similaridade
                    return 5
    return -1


def find_nouns(filtered, pos_tag, q_type):
    store = 0
    non_verbs = []
    for i in range(len(filtered)):
        pos = pos_tag[i]
        if pos != 'VERB':
            word = filtered[i].lower()
            non_verbs.append(word)
            if q_type == "onde":
                if word == "loja" or word in sin_loja:
                    store = 1

    if store:
        response = "Estamos na Rua Direita, em Terra Esquerda!"
    else:
        results = sparql_query(non_verbs)
        response = results

    return response


def load_data():
    questions = []
    answers = []
    query_questions = []
    query_answers = []
    query = 0
    filename = 'perguntas.txt'

    f = open(filename, 'r', encoding=("utf8"))
    lines = f.readlines()

    for line in lines:

        # ignorar identificacao do tipo de pergunta
        if "||" in line:
            # identifica inicio de dados com parametros para query
            if "ARTIGO_INFORM" in line:
                query = 1
            continue

        line = line.lower()

        if "<<" in line:
            # significa que precisa de manter a informacao anterior
            # e obter novos dados
            extra_data = line.split("<<")
            line = extra_data[0]

            # pergunta a fazer para ter o resto da informacao
            # find_more = extra_data[1]
            # TODO funcao que envie a pergunta (find_more) e
            # guarde a resposta para juntar os dados e fazer query

        # identifica pergunta e resposta
        info = line.split(">>")
        answer = info[1]
        question = info[0]

        # separa info para query e info direta
        if (query == 1):
            query_questions.append(question)
            query_answers.append(answer)
        else:
            questions.append(question)
            answers.append(answer)

    f.close()

    return [questions, answers, query_questions, query_answers]


def preprocessing(questions):
    punctuation = string.punctuation
    white_space = string.whitespace
    stop_words = set(stopwords.words('portuguese'))
    filtered_questions = []

    # pre processing do dataset
    for question in questions:
        filtered_words = []
        filtered_question = ""
        # remove pontuacao, whitespace e stopwords
        for word in question.split(' '):
            if word not in punctuation and word not in white_space and word not in stop_words:
                filtered_words.append(word)

        # formula frase a partir das palavras filtradas
        for palavra in filtered_words:
            filtered_question = filtered_question + palavra
            filtered_question = filtered_question + " "

        filtered_questions.append(filtered_question)

    return filtered_questions


def find_best_reply(filtered_questions, answers, query):

    response = ""
    vectorizer = TfidfVectorizer()
    vectorizer.set_params(lowercase=False)
    similares = []
    opcoes = []

    # importancia das palavras do dataset - importante para poder fazer cosine
    # similarity que exige matrizes do mesmo tamanho
    tfidf = vectorizer.fit_transform(filtered_questions)
    # similaridade entre dataset e pergunta
    values = cosine_similarity(tfidf[-1], tfidf)
    # indice similaridade mais alta
    index = values.argsort()[0][-2]
    # ordenar o array por similaridade (crescente)
    flat = values.flatten()
    flat.sort()
    # value mais alto (sem contar o correspondente a pergunta em si)
    similaridade = flat[-2]

    # se encontrou uma pergunta similar
    if similaridade != 0:

        # verifica se ha mais que um resultado
        # com o mesmo valor de similaridade
        similares.append(similaridade)
        for info in values:
            i = 0
            for value in info:
                # se a similaridade nao e a ja encontrada
                if value == similaridade and i != index:
                    similares.append(value)
                i = i + 1

        # se encontrou varios valores iguais
        if len(similares) > 1:
            i = 0
            # recolhe as frases correspondentes as
            # perguntas com similaridade igual
            for i in range(len(similares)):
                pos = -2 - i
                opcoes.append(filtered_questions[values.argsort()[0][pos]])
                i = i + 1

            # escolhe uma resposta aleatoriamente
            response = random.choice(opcoes[:])

            # ve se a resposta corresponde a uma query
            if (query == 1):
                response = sparql_query(response)
        # se so encontrou um valor maximo vai buscar
        # a resposta correspondente
        else:
            response = answers[index]

            # ve se a resposta corresponde a uma query
            if (query == 1):
                response = sparql_query(response)

    return [response, similaridade]


def find_similarity(filtered):
    pergunta = ""
    filtered_questions = []
    filtered_query_questions = []
    # vai buscar as perguntas e respostas correspondentes
    # identica o indice a partir do qual faz query com as respostas
    [questions, answers, query_questions, query_answers] = load_data()

    # preprocessing das perguntas
    filtered_questions = preprocessing(questions)
    filtered_query_questions = preprocessing(query_questions)

    # formula frase para comparar com as do documento
    for word in filtered:
        pergunta = pergunta + word
        pergunta = pergunta + " "
    filtered_questions.append(pergunta)
    filtered_query_questions.append(pergunta)

    # inteiro passado como parametro serve para saber se trata
    # as respostas como query ou nao
    [best_reply, similarity] = find_best_reply(filtered_questions, answers, 0)
    [best_query_reply, query_similarity] = find_best_reply(filtered_query_questions, query_answers, 1)

    if similarity > query_similarity:
        return best_reply

    return best_query_reply


def switch_terminals(verb):
    verbs = []
    terminals = ["ar", "er", "ir"]
    match = -1

    # ve qual o terminal usado
    terminal = verb[-2:]
    for term in terminals:
        match = match + 1
        # encontra terminal do verbo
        if term == terminal:
            # print("encontrou terminal original do verbo")
            break

    # conforme o terminal original cria as outras opcoes
    if match == -1:
        # se nao encontra terminal e verbo irregular
        return verbs

    elif match == 0:
        # terminal original ar
        # troca terminais
        aux = verb[0:-2] + verb[-2].replace('a', 'e') + verb[-1]
        verbs.append(aux)
        aux = verb[0:-2] + verb[-2].replace('a', 'i') + verb[-1]
        verbs.append(aux)

    elif match == 1:
        # terminal original er
        # troca terminais
        aux = verb[0:-2] + verb[-2].replace('e', 'a') + verb[-1]
        verbs.append(aux)
        aux = verb[0:-2] + verb[-2].replace('e', 'i') + verb[-1]
        verbs.append(aux)

    elif match == 2:
        # terminal original ir
        # troca terminais
        aux = verb[0:-2] + verb[-2].replace('i', 'a') + verb[-1]
        verbs.append(aux)
        aux = verb[0:-2] + verb[-2].replace('i', 'e') + verb[-1]
        verbs.append(aux)

    return verbs


def test_replacement(filtered, verbs, verb_pos, pos_tag, q_type):
    # verb_pos identifica indice da palavra a substituir
    responses = []

    for verb in verbs:
        replaced = []
        # inclui palavras numa nova lista
        for i in range(len(filtered)):
            if i != verb_pos:
                replaced.append(filtered[i])
            # quando encontra a posicao do verbo a substituir
            else:
                replaced.append(verb)
        # faz query e adiciona resultado a lista
        response = find_response(replaced, pos_tag, q_type)
        responses.append(response)

    return responses


def check_terminal(filtered, pos_tag, q_type):
    responses = []
    verbs = []
    global verbs_changed

    # encontra verbo
    for i in range(len(filtered)):
        v = pos_tag[i]
        if v == 'VERB':
            # substitui terminal do verbo
            verbs = switch_terminals(filtered[i])
            verbs_changed = verbs_changed + 1
            if verbs_changed > 1:
                responses = []
                return responses
            print("novas terminacoes")
            print(verbs)
            # se e verbo regular
            if len(verbs) > 0:
                # troca palavra e faz query
                responses = test_replacement(filtered, verbs, i, pos_tag, q_type)
                return responses
            # se nao e verbo regular
            else:
                return responses


def find_response(filtered, pos_tag, q_type):
    # procura tipo de verbo
    tipo = find_type(filtered, pos_tag, q_type)
    response = "Desculpe não entendi, ainda estou a aprender... :("
    responses_verb_variations = []

    if tipo == -1:
        # nao encontrou verbos entao procura nomes e tenta fazer query
        response = find_nouns(filtered, pos_tag, q_type)
        return response
    elif tipo == 5:
        # faz query para tentar encontrar resposta na KBDB
        response = "" + sparql_query(filtered)
        # se nao encontrou nenhum artigo
        if "Nenhum Artigo Encontrado" in response:
            # testa com outras terminacoes do verbo
            responses_verb_variations = check_terminal(filtered, pos_tag, q_type)
            if len(responses_verb_variations) > 0:
                # percorre respostas obtidas a ver se alguma devolveu artigos
                for attempt in responses_verb_variations:
                    if "Nenhum Artigo Encontrado" not in attempt:
                        # devolve primeiro match possivel
                        return attempt
            # se as variacoes estao vazias o verbo e irregular
            # pesquisa por similaridade
            response = find_similarity(filtered)
        return response
    elif tipo == 0:
        # cancelar
        response = "A encomenda pode ser cancelada por telefone, ligue!"
        return response
    elif tipo == 1:
        # localizacao
        response = "Estamos na Rua Direita, em Terra Esquerda!"
        return response
    elif tipo == 2:
        # onde encontrar artigos
        response = "Eu posso ajudar a encontrar o que quer! O que procura?"
        return response

    if q_type == "como" or q_type == "quando":
        if tipo == 3:
            # como encomendar
            response = "Basta adicionar o artigo ao carrinho e concluir a compra!"
        elif tipo == 4:
            # detalhes encomenda
            response = "As encomendas chegam em 2-3 dias úteis! Se quiser saber mais alguma coisa procure na Área Pessoal"

    else:
        # se nao encontra question word (ou le "onde") faz query
        response = tipo

    return response


def detect(filtered, pos_tag):
    response = "Desculpe não entendi, ainda estou a aprender... :("
    q_type = "nenhuma"
    i = 0

    # TODO ex camisola mulher só devolve todas as camisolas

    if len(filtered) > 0:
        while i < len(filtered):

            # TODO e se tiver mais que uma keyword?

            if filtered[i].lower() in question_words:
                q_type = filtered[i].lower()
                # TODO ao tirar aqui da lista n dá merda com os
                # indices ao percorrer as palavras????

                filtered.pop(i)
                pos_tag.pop(i)
            i = i + 1

        if q_type == "quem":
            response = "Será que importa? Vamos mudar de assunto!"
        elif q_type == "como" or q_type == "quando":
            # associamos a encomenda
            response = find_response(filtered, pos_tag, q_type)
        elif q_type == "onde":
            response = find_response(filtered, pos_tag, q_type)
        else:
            # nao encontra question word
            response = find_response(filtered, pos_tag, q_type)

        return response

    else:
        return

# print(detect(['Quando', 'chegar', 'pedir'], ['ADV', 'VERB', 'VERB']))
