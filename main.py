# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import gc
from sklearn.feature_extraction import text
from collections import Counter
import pickle
from gensim import matutils, models
import scipy.sparse
from textblob import TextBlob
#USER DEFINED MODULES
import datacleaner  
import exploratorydataanalysis 
import reporter

"""i created pickled object to store stages of my code, 
they would be commented underneath the code that generates 
them.. This should be CONSIDERED as a SECOND OPTION  
"""

#
#read in data
data = pd.read_csv("drugsComTrain_raw.tsv",sep="\t")

#making a copy to work with
data0 = data.copy()

#Importing my first clean function
data_combined = cleanall_phase1(data0)
#found a wrongly inputed condition and took it out -  671 entries removed
data_combined = data_combined[~data_combined['Condition'].str.contains("users found this")]                                                                                                                                                                                                                   
#quick look at the data
data_combined.head()

data_combined.chunk= cleanall_phase2(data_combined)
#both lemmatizer and stemmer had almost same impact on cleaning
#process so running either of any would do just fine
data_combined.chunk = data_combined.chunk.apply(lambda x: word_stemmer(x))
data_combined.chunk = data_combined.chunk.apply(lambda x: word_lemmatizer(x))


 
#it adds new_stop_words(gotten from looking at the data) to stop words list
new_stop_words =['im','like', 'just','ive', 'forwardyesterday', 'says','mei',
 'forwarned','forwardthis', 'forwas','forwards', 'forwhat',
 'forwhen', 'forwardmy','forwhile','did', 'took','wont','uti',
'forwish','forworked','forwardmethadone', 'іt','didnt','let','aa','aaa','aaaaa',
'zzzzzzzzthe','zzz','zzzzz', 'zzzzzzzzif','aaaaand', 'aaaaargmy', 'aaaand','aaahhi', 'aaand',
 'aaddthis', 'aafter', 'aai', 'aam', 'aamp', 'aampb', 'aampd',
 'aampe', 'aampee','aana', 'aap','aampeon', 'zzzzap','aampethe','abacavirlamivudinenevirapine',
 'aaps','aarp','aatd','ab','abbvie','taking']
stop_words = text.ENGLISH_STOP_WORDS.union(new_stop_words)
test = cleanall_phase3(data_combined,stop_words) 
test = test.transpose()

##############################
#FINISHED WITH DATA CLEANSING#
##############################

#should incase you ran line 43-53 afterwards and you get
#MemoryError, freeing the memory should solve the issue

#reassigning an integer to test and calling garbage collector
test = 0
gc.collect()



###########################
#EXPLORATORY_DATA_ANALYSIS#
###########################
#Get top words for each medication 
top_word = topwords(test,30)

#printing top 15  for each 
for drugName, top_words in top_word.items():
    print(drugName)
    print(', '.join([word for word, count in top_words[0:14]]))
    print('---')
    
# pull out the top 30 words for each drug
words = []
for drugName in test.columns:
    top = [word for (word, count) in top_word[drugName]]
    for t in top:
        words.append(t)

#  aggregate the list and identify the most common words 
Counter(words).most_common()

[word for word, count in Counter(words).most_common()]

##################
#REPORT GENERATOR#
##################
#This creates a word document with all the word cloud of the top 30 words
#It also contrast other related medications and suggests the 
#best medication (based on people's reviews )
wordcreator('Joint Infection','Rocephin')
wordcreator('Neutropenia','Filgrastim')
wordcreator('Zollinger-Ellison Syndrome','Omeprazole')
wordcreator('Coccidioidomycosis','Sporanox')
wordcreator('Manscaping Pain','Lidocaine')
wordcreator('ADHD','Dexmethylphenidate')
wordcreator('Coronary Artery Disease','Amlodipine')
wordcreator('Anemia, Chemotherapy Induced','Procrit')
wordcreator('Linear IgA Disease','Dapsone')
#run this to get the list of conditions and drugname
data_combined[["Condition","drugName"]]

#Sentiment analysis
pol =lambda x: TextBlob(x).sentiment.polarity
sub =lambda x: TextBlob(x).sentiment.subjectivity

data_combined['Polarity'] = data_combined["chunk"].apply(pol)
data_combined['Subjectivity'] = data_combined["chunk"].apply(sub)

# Topic Modelling
test_tm = test.transpose()
sparse_counts = scipy.sparse.csr_matrix(test_tm)
corpus = matutils.Sparse2Corpus(sparse_counts)
id2word = dict((v,k) for k, v in test.vocabulary_.items())
lda = models.ldamodel(corpus =corpus,num_topics =2,passes=10)
#visualization plot
sns.scatterplot(x="Polarity",y="Subjectivity",hue="drugName",data=data_combined[data_combined["Condition"]=='ADHD'],legend=False)
                                                             

