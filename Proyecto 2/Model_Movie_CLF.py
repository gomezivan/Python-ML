import pandas as pd
from sklearn.externals import joblib
import category_encoders as ce
import sys
import os
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
import re 
import nltk
nltk.download('wordnet')

# BinEncoder = joblib.load('BinEncoder.pkl') 
clf = joblib.load('RF_generos2.pkl')

YearBinaryEnco = joblib.load('YearBinaryEnco.pkl')
tfidf_plot = joblib.load('tfidf_plot.pkl')
tfidf_title = joblib.load('tfidf_title.pkl')


def clasff_movie(title, plot, year):
    
    
    #Preprocess
    title_clean = text_clean(title, remove_stop_words=False)
    plot_clean  = text_clean(plot)
    
    #Transform
    YearBinary = YearBinaryEnco.transform(pd.DataFrame([year],columns=["year"]))
    title_tfidf_dtm = tfidf_title.transform(pd.Series([title_clean]))
    title_feat_tfidf = pd.DataFrame(title_tfidf_dtm.toarray(), columns=tfidf_title.get_feature_names())

    plot_tfidf_dtm = tfidf_plot.transform(pd.Series([plot_clean]))
    plot_feat_tfidf = pd.DataFrame(plot_tfidf_dtm.toarray(), columns=tfidf_plot.get_feature_names())

    #Create a dataframe 
    df_ = pd.concat([title_feat_tfidf, 
                  plot_feat_tfidf, 
                  YearBinary], axis=1) 
    
    #Predict
    predict_ = clf.predict_proba(df_)

    return predict_


# This function transform the text in order get ready data, remove stop words, stimming, Lemmatisation and n_grams
def text_clean(text, remove_stop_words=True):
    wordnet_lemmatizer = WordNetLemmatizer()
    stemmer = SnowballStemmer('english')
    document = text
    
    # Remove all the special characters
    document = re.sub(r'\W', ' ', document)

    # remove all single characters
    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

    # Remove single characters from the start
    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 

    # Substituting multiple spaces with single space
    document = re.sub(r'\s+', ' ', document, flags=re.I)

    # Removing prefixed 'b'
    document = re.sub(r'^b\s+', '', document)
    
    #Removing punctuation
    document = re.sub(r'[^\w\s]', '', document)

    #LowerCase    
    document = document.lower()
    
    #Split document word a word
    words_document = text.split()
    
    #Remove clean_words
    words_document = [word for word in words_document if word not in waste_words]
    #Remove stop words
    if remove_stop_words:
        words_document = [word for word in words_document if word not in custom_stopwords]
    
    #stimming
    words_document = [stemmer.stem(word) for word in words_document]
    
    #Lemmatisation
    words_document = [wordnet_lemmatizer.lemmatize(word) for word in words_document]
    words_document = [wordnet_lemmatizer.lemmatize(word, pos='v') for word in words_document]
           
    return ' '.join(words_document)

custom_stopwords =['a', 'about', 'above', 'across', 'after', 'afterwards', 'again',
       'against', 'ain', 'all', 'almost', 'alone', 'along', 'already',
       'also', 'although', 'always', 'am', 'among', 'amongst', 'amoungst',
       'amount', 'an', 'and', 'another', 'any', 'anyhow', 'anyone',
       'anything', 'anyway', 'anywhere', 'are', 'aren', "aren't",
       'around', 'as', 'at', 'back', 'be', 'became', 'because', 'become',
       'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind',
       'being', 'below', 'beside', 'besides', 'between', 'beyond', 'bill',
       'both', 'bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant',
       'co', 'con', 'could', 'couldn', "couldn't", 'couldnt', 'cry', 'd',
       'de', 'describe', 'detail', 'did', 'didn', "didn't", 'do', 'does',
       'doesn', "doesn't", 'doing', 'don', "don't", 'done', 'down', 'due',
       'during', 'each', 'eg', 'eight', 'either', 'eleven', 'else',
       'elsewhere', 'empty', 'enough', 'etc', 'even', 'ever', 'every',
       'everyone', 'everything', 'everywhere', 'except', 'few', 'fifteen',
       'fifty', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former',
       'formerly', 'forty', 'found', 'four', 'from', 'front', 'full',
       'further', 'get', 'give', 'go', 'had', 'hadn', "hadn't", 'has',
       'hasn', "hasn't", 'hasnt', 'have', 'haven', "haven't", 'having',
       'he', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein',
       'hereupon', 'hers', 'herself', 'him', 'himself', 'his', 'how',
       'however', 'hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed',
       'interest', 'into', 'is', 'isn', "isn't", 'it', "it's", 'its',
       'itself', 'just', 'keep', 'last', 'latter', 'latterly', 'least',
       'less', 'll', 'ltd', 'm', 'ma', 'made', 'many', 'may', 'me',
       'meanwhile', 'might', 'mightn', "mightn't", 'mill', 'mine', 'more',
       'moreover', 'most', 'mostly', 'move', 'much', 'must', 'mustn',
       "mustn't", 'my', 'myself', 'name', 'namely', 'needn', "needn't",
       'neither', 'never', 'nevertheless', 'next', 'nine', 'no', 'nobody',
       'none', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'o',
       'of', 'off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or',
       'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out',
       'over', 'own', 'part', 'per', 'perhaps', 'please', 'put', 'rather',
       're', 's', 'same', 'see', 'seem', 'seemed', 'seeming', 'seems',
       'serious', 'several', 'shan', "shan't", 'she', "she's", 'should',
       "should've", 'shouldn', "shouldn't", 'show', 'side', 'since',
       'sincere', 'six', 'sixty', 'so', 'some', 'somehow', 'someone',
       'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such',
       'system', 't', 'take', 'ten', 'than', 'that', "that'll", 'the',
       'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there',
       'thereafter', 'thereby', 'therefore', 'therein', 'thereupon',
       'these', 'they', 'thick', 'thin', 'third', 'this', 'those',
       'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to',
       'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty',
       'two', 'un', 'under', 'until', 'up', 'upon', 'us', 've', 'very',
       'via', 'was', 'wasn', "wasn't", 'we', 'well', 'were', 'weren',
       "weren't", 'what', 'whatever', 'when', 'whence', 'whenever',
       'where', 'whereafter', 'whereas', 'whereby', 'wherein',
       'whereupon', 'wherever', 'whether', 'which', 'while', 'whither',
       'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with',
       'within', 'without', 'won', "won't", 'would', 'wouldn', "wouldn't",
       'y', 'yet', 'you', "you'd", "you'll", "you're", "you've", 'your',
       'yours', 'yourself', 'yourselves']

waste_words =['!',
 '"',
 '$',
 '%',
 '&',
 "'",
 '(',
 ')',
 ',',
 '-',
 '.',
 '/',
 ':',
 ';',
 '=',
 '?',
 'a$$',
 'a&m',
 'aa',
 'aaa',
 'aam',
 '+',
 'aang']