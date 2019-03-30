#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 8 14:52:58 2017

@author: juan
"""
from nltk.corpus import stopwords
from string import punctuation
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

spanish_stopwords = stopwords.words('spanish')
non_words = list(punctuation)
non_words.extend(['¿', '¡'])  
non_words.extend(map(str,range(10)))

def crear_vocabulario(textos, ngrammax=2, min_df=1, max_df=1.0, remove_monowords = False):
    vectorizer = CountVectorizer(
                        input = textos,
                        analyzer = 'word',
#                        tokenizer = tokenize,
                        lowercase = True,
                        stop_words = spanish_stopwords,
                        max_df = max_df,
                        min_df = min_df,
                        ngram_range = (1, ngrammax))
    dtm=vectorizer.fit_transform(textos)  # a sparse matrix
    freq = dtm.sum(axis=0)
    freq = freq.transpose()
    vocab = vectorizer.get_feature_names()  # a list
    dictionary = {vocab[i]: np.asscalar(freq[i]) for i in range(len(vocab))}
    if remove_monowords == True:
        for key1 in list(dictionary.keys()):
            for key2 in list(dictionary.keys()):
                if (key1 != key2 and key1 in key2):
                    dictionary[key1] = dictionary[key1] - dictionary[key2]
    dictionary = {k:v for k, v in dictionary.items() if v>0}
    return dictionary

def crear_dtm(textos, ngrammax, min_df=1, max_df=1.0):
    vectorizer = CountVectorizer(
                        input = textos,
                        analyzer = 'word',
#                        tokenizer = tokenize,
                        lowercase = True,
                        stop_words = spanish_stopwords,
                        max_df = max_df,
                        min_df = min_df,
                        ngram_range = (1, ngrammax))
    vectorizer.fit_transform(textos)  # a sparse matrix
    dtm = vectorizer.fit_transform(textos)  # a sparse matrix
    dtm = dtm.toarray()
    return dtm

## Ejemplo
#textos = ["Alvaro Uribe Velez es maravilloso", "Peñalosa es un genio", "Petro es un gran ciudadano", "Gustavo Petro es un gran gerente", "Uribe Velez mejoró este país", "Jorge robledo es un excelente economista", "Germán Vargas Lleras es consistente", "Enrique Peñalosa es honesto", "Claudia López es respetuosa", "Uribe siempre dice la verdad", "Sergio Fajardo es humilde y sencillo", "Vargas será un gran presidente"]
#diccionario = crear_vocabulario(textos, ngrammax=2, min_df=1, max_df=1.0, remove_monowords = False)
#diccionario2 = crear_vocabulario(textos, ngrammax=2, min_df=1, max_df=1.0, remove_monowords = True)