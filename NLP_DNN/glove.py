#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 11:53:35 2017

@author: Erick
"""


from glove import Glove
from glove import Corpus
from sklearn.feature_extraction.text import CountVectorizer
import math
import pandas as pd
from tabulate import tabulate


def crear_matriz_glove(textos,
                       anonymous=True,
                       remove_form_features=False,
                       max_df=0.4,
                       min_df=0.0001,
                       skip_grams_window = 7,
                       word_vectors_size = 150,
                       n_iter = 500,
                       dirr=None):
     
    textos=process_tweets(textos,anonymous_mentions=anonymous,remove_form_features=remove_form_features,replacestopwords=False)
    textos = [replace(pattern=['\\b(neg_)?t\\.\\b|\\b(neg_)?t\\.$'],replacement=[''],tweet=textos[i]) for i in range(len(textos))]
    minCount =  math.floor(max(5,min_df*len(textos)))
    vectorizer = CountVectorizer(
                            input = textos,
                            analyzer = 'word',
    #                        tokenizer = tokenize,
                            lowercase = True,
                            stop_words = None,
                            max_df = max_df,
                            min_df = minCount,
                            ngram_range = (1, 1))
    vectorizer.fit_transform(textos)  # a sparse matrix
    vocab = vectorizer.get_feature_names()  # a list
    dictionary = {vocab[i]: i for i in range(len(vocab))}    
    def read_corpus(textos):
        for line in textos:
            yield tokenize(line)                
    corpus_model = Corpus(dictionary)
    corpus_model.fit(read_corpus(textos), window=skip_grams_window,ignore_missing=True)
    print('Tamanho del diccionario: %s' % len(corpus_model.dictionary))
    print('No de no ceros en la matriz de coo: %s' % corpus_model.matrix.nnz)        
    glove = Glove(no_components=word_vectors_size,max_count=10)
    glove.fit(corpus_model.matrix, epochs=n_iter,
              no_threads=1, verbose=True)
    glove.add_dictionary(corpus_model.dictionary)
    
    
    if dirr is not None:
        glove.save(dirr+'glove.model')
        # Para cargar el modelo correr Glove.load(dirr+'glove.model')
    
    return glove

def from_glove_to_tex(glove,list_palabras,num_palab=10):
    
    exportar=pd.DataFrame()
    for palabra in list_palabras:
        #palabra=list_palabras[2]
        if palabra in glove.dictionary:
            similares=glove.most_similar(palabra, number=num_palab)
            #similar=similares[2]
            fila=pd.Series([similar[0]+' ('+str(round(similar[1]*100, 2))+'%)' for similar in similares])
            fila=pd.Series(palabra).append(fila,1)
            exportar=exportar.append(fila,1)
            
    print(tabulate(exportar, tablefmt="latex", floatfmt=".2f",showindex="no"))

    
    

###ejemplo


with open ("/Users/apple/Dropbox (Quantil)/PartidoU/Bases/Glove/tweetsQuantweet2017-10-10---2017-10-31.txt", "r") as myfile:
    textos=myfile.readlines()







glove=crear_matriz_glove(textos,
                         anonymous=True,
                         remove_form_features=False,
                         max_df=0.4,
                         min_df=0.0001,
                         skip_grams_window = 7,
                         word_vectors_size = 150,
                         n_iter = 500,
                         dirr='/Users/apple/Dropbox (Quantil)/PartidoU/Bases/Glove/')

list_palabras=["castrochavismo","corrupcion","farc","fiscal","venezuela","crimen","politica","justicia","seguridad","economia","paz","salud","educacion"]


from_glove_to_tex(glove,list_palabras,num_palab=10)





