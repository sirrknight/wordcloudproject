# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 18:53:29 2020

@author: Precious
"""

from wordcloud import wordcloud
import datacleaner


def topwords(data,n):
    """
    

    Parameters
    ----------
    data : the document based metrix of the chunk data
    n : int
       Number of words to retrieve 

    Returns
    -------
    top_dict : list 
        top words in the document based metrix per drugName.

    """
    top_dict = {}
    for c in data.columns:
        top = data[c].sort_values(ascending=False).head(n)
        top_dict[c]= list(zip(top.index,top.values))

    return top_dict





