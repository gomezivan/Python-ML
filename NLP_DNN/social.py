#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 16:39:23 2017

@author: Erick
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import os

import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
import requests
import unicodedata
import emoji



finder={'url' : '(https?\\:\\/\\/)?([A-Za-z0-9][A-Za-z0-9\\-]*\\.)+[^ ]+',
        'http' : 'https?:[^ $]+',
        'hash' : '#\\w+',
        'hashtag' : '(?<=#)\\S+',
        'neg' : '\\b(no\\b[^\\.!\\?¿¡,]+|ni\\b[^\\.!\\?¿¡,]+|nada\\b[^\\.!\\?¿¡,]+|sin\\b[^\\.!\\?¿¡,]+|nunca\\b[^\\.!\\?¿¡,]+|ninguno\\b[^\\.!\\?¿¡,]+|ninguna\\b[^\\.!\\?¿¡,]+|nadie\\b[^\\.!\\?¿¡,]+|menos\\b[^\\.!\\?¿¡,]+|negar\\b[^\\.!\\?¿¡,]+|nego\\b[^\\.!\\?¿¡,]+|quitar\\b[^\\.!\\?¿¡,]+|quitarle\\b[^\\.!\\?¿¡,]+)',
        'mention' : '@(\\w+)',
        'happy' : '(:-\\)|:\\)|:o\\)|:]|:3|=]|=\\))',
        'funny' : '(:-D|:D|8D|x-D|xD|X-D|XD|=-D|=D|=3)',
        'sad' : "(:-\\(|:\\(|:-c|:c|:-<|:-\\[|:\\[|:{|:'-\\(|:'\\()",
        'boring' : '(:\\\\|:-\\/|:-\\.|:\\/\\b|:\\\\\\b|=\\/|=\\\\|:L|=L|:S|>\\.<|:\\||:-\\|)+',
        'repeated_not_celnor' : '([abdf-kmp-qs-z])\\1+',
        'repeated_celnor' : '([l|r|n|c|o|e])\\1{2,}',
        's_words' : list(set().union(stopwords.words('spanish'),['0','01','1','2','4','5','6','7','8','9','a','al','alla','alli','aqui','asi','como','con','[a-zñ]','va','d','de','del','desde','dia','donde','e','el','en','entre','es','esa','esas','ese','eso','esos','esta','estamos','estan','este','esto','estos','fue','ha','habia','hace','hacia','hay','hoy','la','las','le','le','les','lo','los','mas','me','menos','mi','mil','mis','ni','no','nos','nuestro','nunca','o','para','pero','por','porque','q','que','se','ser','sera','si','siempre','simb_arroba','sin','sobre','solo','son','su','sus','t','tb','te','ti','tmb','todo','tu','tus','un','una','usted','x','xa','xq','y','ya','ð','ð'])),
        'o_words' : ['ahora','cual','cuales','cuando','da','debe','debemos','dice','eres','esta','este','estoy','fueron','fui','gran','hacer','han','hasta','he','hemos','muy','otro','primer','puede','quiere','sea','sido','somos','soy','tan','tenemos','tener','tengo','tiene','tiene','tienen','ud','va','vamos','van','ver','via','viene','yo'],
        'jaja' : '\\w*(jaja|haha|jajja|jeje|hehe|jiji)\\w*'}



def replace(pattern, replacement, tweet):
    n_pat = len(pattern)
    n_rep = len(replacement)
    if (n_rep <= n_pat) & (n_pat % n_rep == 0):
        replacement = list(np.repeat(replacement, n_pat/n_rep))
    else:
        'length of pattern is not a multiple of length of replacement'
        return

    for i in range(n_pat):
        tweet = re.sub(pattern[i], replacement[i],tweet)
    tweet=re.sub(' +',' ',tweet)
    tweet=re.sub('^ | $','',tweet)
    return(tweet)


def replace_breakline(tweet):
    tweet=re.sub(r' ?\n\.? ?([A-ZÑ])','. \\1',tweet)
    tweet=re.sub(' ?\n ?',' ',tweet)
    return(tweet)

def replace_emoticon(tweet):
    tweet=replace(pattern=[finder['happy'],finder['funny'],finder['sad'],finder['boring']],
            replacement=['emot' + x for x in ['feliz', 'divertido', 'triste', 'aburrido']],
            tweet=tweet)
    return(tweet)


def replace_repeated_not_celnor(tweet):
    tweet = replace(pattern=[finder['repeated_not_celnor']], replacement=['\\1'],tweet=tweet)
    return(tweet)



def replace_jaja(tweet):
    tweet = replace(pattern=[finder['jaja']], replacement=['jaja'],tweet=tweet)
    return(tweet)


def replace_repeated_celnor(tweet):
    tweet = replace(pattern=[finder['repeated_celnor']], replacement=['\\1\\1'],tweet=tweet)
    return(tweet)


def replace_mention(tweet,anonymous=False):
    if not anonymous:
        tweet=replace(pattern= ["@RoyBarreras",
                                "@AABenedetti",
                                "@PachoSantosC",
                                "@mluciaramirez",
                                "@A_OrdonezM",
                                "@IvanDuque",
                                "@CarlosHolmesTru",
                                "@petrogustavo",
                                "@ClaudiaLopez",
                                "@sergio_fajardo",
                                "@German_Vargas",
                                "@CristoBustos",
                                "@DeLaCalleHum",
                                "@JERobledo",
                                "@ClaraLopezObre",
                                "@partidodelaucol",
                                "@CeDemocratico",
                                "@soyconservador",
                                "@PartidoLiberal",
                                "@PCambioRadical",
                                "@PartidoVerdeCoL",
                                "@PoloDemocratico",
                                "@JuanManSantos",
                                "@AlvaroUribeVel",
                                finder['mention']],
                          replacement= ["roy barreras",
                                        "armando benedetti",
                                        "pacho santos",
                                        "marta lucía ramírez",
                                        "alejandro ordoñez",
                                        "ivan duque",
                                        "carlos holmes",
                                        "gustavo petro",
                                        "claudia lopez",
                                        "sergio fajardo",
                                        "german vargas lleras",
                                        "juan fernando cristo",
                                        "humberto de la calle",
                                        "jorge robledo",
                                        "clara lopez",
                                        "partido u",
                                        "centro democratico",
                                        "partido conservador",
                                        "partido liberal",
                                        "cambio radical",
                                        "partido verde",
                                        "polo democratico",
                                        "juan manuel santos",
                                        "alvaro uribe",
                                        "\\1"],
                                      tweet=tweet)
    else:
        candidates=["\\broy( barreras)?",
            "(armando )?benedetti",
            "pacho santos",
            "marta lucía ramírez",
            "alejandro ordonhez",
            "ivan duque",
            "carlos holmes( trujillo)?",
            "(gustavo )?petro\\b",
            "claudia lopez",
            "(sergio )?fajardo",
            "(german )?vargas lleras",
            "juan fernando cristo",
            "(humberto )?de la calle",
            "(jorge )?(enrique )?robledo",
            "clara lopez",
            "partido u",
            "centro democratico",
            "partido conservador",
            "partido liberal",
            "cambio radical",
            "partido verde",
            "polo democratico",
            "(juan )?(manuel )?santos",
            "(alvaro )?uribe"]

        tweet = replace(pattern=[finder['mention']]+candidates,
                replacement=['@arroba'] + np.repeat("simb_nombre",len(candidates)).tolist(),
                tweet=tweet)
    return(tweet)



def replace_link(tweet):
    tweet = replace(pattern=[finder['url']], replacement=[' \\2 '],tweet=tweet)
    return(tweet)


def replace_hash(tweet):
        while(bool(re.search(finder['hash'],tweet))):
            hashtag=re.search(finder['hashtag'],tweet).group(0)
            replacement = re.sub(r'([A-ZÁÉÍÓÚÑ])([a-záéíóúñ0-9])', ' \\1\\2', hashtag)
            tweet = re.sub(r'#'+re.escape(hashtag), replacement,tweet)
        return(tweet)


def replace_neg(tweet):
    if (not bool(re.search(finder['neg'],tweet))):
        return(tweet)

    neg_replacement=pd.Series(re.findall(finder['neg'],tweet))
    neg_replacement=list(neg_replacement.str.replace('\\W+(\\w+)',' neg_\\1'))
    for i in range(len(neg_replacement)):
        tweet=re.sub(re.escape(re.findall(finder['neg'],tweet)[i]),neg_replacement[i],tweet)
    return(tweet)


def tokenize(tweet):
    return(re.split('\\W+',tweet))


def replace_spanish(tweet):
    tweet=replace(['á', 'é', 'í', 'ó', 'ú', 'ñ'],['a', 'e', 'i', 'o', 'u', 'nh'],tweet)
    return(tweet)

def replace_form_features(tweet,remove=True):

    pattern=['(\\"|‘|’|\\\)+',
               '…|\\.{2,10}',
               '(\\?|¿)+',
               '!+|¡+',
               '-',
               '[0-9][0-9]?(:[0-9][0-9])?\\s?(am|pm|a.m.|p.m.)',
               '\\b[0-9][0-9]?(\\.|:)',
               '➡️']

    if(not remove):
        tweet=replace(pattern=pattern,
            replacement=[' simb_comillas ',
                         ' simb_suspensivos ',
                         ' simb_interrogacion ',
                         ' simb_exclamacion ',
                         ' simb_guion ',
                         ' simb_hora ',
                         ' simb_bullet ',
                         ' simb_flecha '],tweet=tweet)
        tweet=re.sub(r'[ ]+',' ',tweet)

    else:
        tweet=replace(pattern=pattern,
            replacement=[' '],tweet=tweet)
    return(tweet)


def replace_stopwords(tweet,addedSW=[]):
    addedSW=addedSW+finder['s_words']
    patt=['\\b('+'|'.join(addedSW)+'|neg_'+'|neg_'.join(addedSW)+')\\b']
    tweet=replace(pattern=patt,replacement=[''],tweet=tweet)
    return(tweet)

def replace_emoji(tweet):
    emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]", flags=re.UNICODE)
    def extract_emojis(str):
        return [c for c in str if c in emoji.UNICODE_EMOJI]
    unicodes1=re.findall(emoji_pattern,tweet)
    unicodes2=extract_emojis(tweet)
    unicodes=list(set().union(unicodes1,unicodes2))
    for unicode in unicodes:
        tweet=re.sub(unicode,' '+re.sub(' ','',unicodedata.name(unicode))+' ',tweet)
    tweet=re.sub(' +',' ',tweet)
    return(tweet)



def remplazadora_fechas(tweet):
    tweet=replace(pattern=["Jan","Feb","Mar","Apr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dec","\\+[0-9]+",
                                        "[0-9][0-9]:[0-9][0-9]:[0-9][0-9]",
                                        "Fri|Sat|Sun|Mon|Tue|Thu|Wed",
                                        "^ ",
                                        "\\s+"],replacement=["01","02","03","04","05","06","07","08","09","10","11","12",
                                            "",
                                            "",
                                            "",
                                            "",
                                            "-"],tweet=tweet)
    return(tweet)

def minimize_tweet(tweet):
    tweet=tokenize(replace_repeated_celnor(replace_repeated_not_celnor(str.lower(replace_neg(replace_mention(replace_link(replace_hash(replace_emoji(replace_emoticon(tweet))))))))))
    return(tweet)

def remove_puntuation(tweet):
    tweet=replace(pattern=['[\\.,:]'],replacement=[''],tweet=tweet)
    return(tweet)

def remove_rt(tweet):
    tweet=replace(pattern=['\\b[Rr][tT]:|\\b[Rr][tT]\\b|^[Rr][tT]:|^[Rr][tT]\\b'],replacement=[''],tweet=tweet)
    return(tweet)


def process_tweet(tweet,replaceemoticon=True,replaceemoji=True,replacehash=True,replacelink=True,replacemention=True,replacebreakline=True,replaceneg=True,replaceformfeatures=True,replacestopwords=True,
                  remove_form_features=True,anonymous_mentions = False,addedSW=[],removepuntuation=True,removert=True):

    if(replaceemoticon):
        tweet=replace_emoticon(tweet)

    if(replaceemoji):
        tweet=replace_emoji(tweet)

    if(replacehash):
        tweet=replace_hash(tweet)

    if(replacelink):
        tweet=replace_link(tweet)

    if(replacemention):
        tweet=replace_mention(tweet,anonymous=anonymous_mentions)

    if(replacebreakline):
        tweet=replace_breakline(tweet)


    tweet=str.lower(tweet)

    if(replaceneg):
        tweet=replace_neg(tweet)

    tweet=replace_jaja(replace_spanish(replace_repeated_celnor(replace_repeated_not_celnor(tweet))))

    if(replaceformfeatures):
        tweet=replace_form_features(tweet,remove=remove_form_features)

    if(replacestopwords):
        tweet=replace_stopwords(tweet,addedSW=addedSW)

    if(removepuntuation):
        tweet=remove_puntuation(tweet)

    if(removert):
        tweet=remove_rt(tweet)

    return(tweet)

def process_tweets(tweets,removeempty=False,replaceemoticon=True,replaceemoji=True,replacehash=True,replacelink=True,replacemention=True,replacebreakline=True,replaceneg=True,replaceformfeatures=True,replacestopwords=True,
                  remove_form_features=True,anonymous_mentions = False,addedSW=[],removepuntuation=True,removert=True):
    tweets=[process_tweet(tweet,replaceemoticon=replaceemoticon,replaceemoji=replaceemoji,replacehash=replacehash,replacelink=replacelink,replacemention=replacemention,replacebreakline=replacebreakline,replaceneg=replaceneg,replaceformfeatures=replaceformfeatures,replacestopwords=replacestopwords,remove_form_features=remove_form_features,anonymous_mentions = anonymous_mentions,addedSW=addedSW,removepuntuation=removepuntuation,removert=removert) for tweet in tweets]
    if(removeempty):
        tweets=list(pd.Series(tweets)[~ pd.Series(tweets).str.contains('^$')])
    return tweets
