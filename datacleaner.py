# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 15:14:32 2020

@author: Precious
 Module cleans text dataframe to allow text processing
 total of 3 cleaning stages and 3 word/lexical modelling functions
 cleanall_phase1: creates a dataframe with a summarised version
                 of our data by combining ALL the reviews for ALL
                 customers for A particular drugName under A particular
                 medical condition.
                 input>>dataframe
                 output>>dataframe[drugName,condition,chunk(combination of reviews),usefulTo,averageRating]
                 
cleanall_phase2: works on the chunk aspect of the dataframe and 
                converts all text to to lower cases, removes string 
                formatting and all punctuation stored 
                input>>dataframe
                output>>series[chunk]
                Note: this should be apploed on the data
                
cleanall_phase3:this converts the chunk data from the corpus 
                format to the document matrix format(spreading
                out the words into columns across the observation)
                input>>dataframe
                output>>dataframe[each word as a column](with multiIndexing)
                
word_stemmer: built on the stemmer function to cut words into short 
             forms which is not necceasarily an english word 
             input>>series[chunk]
             output>>series[chunk] less words taken out

word_stopwords: built to remove stop words from the chunk aspect
                of the dataframe
                input>>series[chunk]
                output>>series[chunk] less words taken out
                
word_lematizer: built on the lemmatizer function to cut words into short 
             forms which is an english word but has tradeoff which involves 
             computational expenses
             input>>series[chunk]
             output>>series[chunk] less words taken out
             
"""
#importing all libraries needed 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from  sklearn.feature_extraction.text import CountVectorizer
import pdb 
from nltk.stem import *
from nltk.corpus import stopwords
import re
import string

def cleanall_phase1(data): 
    
    """
    creates a dataframe with a summarised version of the data 
    by combining ALL the reviews for ALL customers for A 
    particular drugName under A particular medical condition.
                 
                 

    Parameters
    ----------
    data : dataframe
    
    output>>dataframe[drugName,condition,chunk(combination of reviews),usefulTo,averageRating]
    -------
    
    """
    variable = list(data.condition.unique())
    #dummydata = np.zeros((len(variable),))
    conditionList =[]
    drugnameList=[]
    chunkList=[]
    ratingList=[]
    usefulCountList=[]
    #iterating through a condition
    for i in range(len(variable)):        
        conditionVariable= data0.loc[data0['condition']==variable[i]]
        #iterating through each drug in the condition
        for t in list(conditionVariable.drugName.unique()):
            drugname = conditionVariable.loc[conditionVariable['drugName']==t]
            rating = data.rating[(data.drugName==t) & (data.condition ==variable[i])].mean()
            usefulcount = data.usefulCount[(data.drugName==t) & (data.condition ==variable[i])].sum()
            #appending each review of each drug under one condition into one big chunk of text
            chunk = ''.join(drugname.review)
            #Storing my data into a list and then a dictionary for my dataframe
            conditionList.append(variable[i])
            drugnameList.append(t)
            chunkList.append(chunk)
            ratingList.append(round(rating,2))
            usefulCountList.append(usefulcount)
    final_dict ={"Condition":conditionList,"drugName":drugnameList,"chunk":chunkList,"averageRating":ratingList,"usefulTo":usefulCountList}
    final = pd.DataFrame(final_dict)
    return(final)


                
def cleanall_phase2(data):
    
    """
    

    Parameters
    ----------
    data : works on the chunk aspect of the dataframe and 
          converts all text to to lower cases, removes string 
          formatting and all punctuation stored
          input>>dataframe
    Returns
    -------
    output>>series[chunk]
    Note: this should be applied on the data

    """
    clean = data.chunk
    clean = clean.str.lower()
    ##pdb.set_trace()
    clean = clean.str.replace('\[.,*?\]', '')
    clean = clean.str.replace('\w*\d\w*', '')
    clean = clean.str.replace('[%s]' % re.escape(string.punctuation), '')
    clean = clean.str.replace('\n','')
    clean = clean.str.replace('[‘’“”…]', '')
    return clean

stemmer = PorterStemmer()    
def word_stemmer(text):
    """ 
    Parameters
    ----------
    text : built on the stemmer function to cut words into short 
             forms which is not necceasarily an english word 
             input>>series[chunk]
             

    Returns
    -------
    stem_text : output>>series[chunk] less words taken out

    """
    stem_text = "".join([stemmer.stem(i) for i in text])
    return stem_text 

lemmatizer = WordNetLemmatizer()
def word_lemmatizer(text):
    """
    

    Parameters
    ----------
    text : built on the lemmatizer function to cut words into short 
             forms which is an english word but has tradeoff which involves 
             computational expenses
             input>>series[chunk]
             

    Returns
    -------
    lem_text : series[chunk] less words taken out

    """
    lem_text = "".join([lemmatizer.lemmatize(i) for i in text])
    return lem_text

def remove_stopwords(text):
    words = [w for w in text if w not in stopwords.words('english')]
    return words

def cleanall_phase3(data,stopword):
    """
    

    Parameters
    ----------
    data : this converts the chunk data from the corpus 
    format to the document matrix format(spreading
    out the words into columns across the observation)
    input>>dataframe
                
    

    Returns
    -------
    data_dtm : dataframe[each word as a column](with multiIndexing)

        DESCRIPTION.

    """
    cv = CountVectorizer(stop_words=stopword)
    #temp=["0"] * len(data.chunk)
    
    #for i in range(len(data.chunk)):
    data_cv = cv.fit_transform(data.chunk)
        #temp[i]= data_cv
        
    data_dtm =pd.DataFrame(data_cv.toarray(),columns=cv.get_feature_names())
    data_info = data[['Condition','drugName']]
    #data_merged = pd.concat([data_info,test],axis=1)
    
    data_dtm.index = pd.MultiIndex.from_frame(data_info)
    return data_dtm