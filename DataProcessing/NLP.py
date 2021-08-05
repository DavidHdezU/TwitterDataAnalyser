import spacy
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.probability import FreqDist
import re

class NLP():
    def __init__(self, language):
        self.stopwords = set(stopwords.words(language))
        self.language = language
        print(self.stopwords)
        
    def top_frequent_words_in_replies(self, replies_df, limit):
        words = []
        n = limit if limit < len(replies_df['tweet']) else len(replies_df['tweet'])-1
        
        for i in range(n):
            sentence = replies_df['tweet'][i]
            for word in sentence.split():
                words.append(word)
                
        words = [re.sub(r'[^A-Za-z0-9]+', '', s) for s in words] # Remove punctuation
        s_stemmer = SnowballStemmer(language=self.language) # stemming the words to their root
        
        stemmed_words = []
        for word in words:
            if word != '':
                stemmed_words.append(s_stemmer.stem(word))
              
        final_words = []
        for word in stemmed_words:
            if word not in self.stopwords:
                final_words.append(word)
            
        frecuency_count = FreqDist()
        for word in final_words:
            frecuency_count[word.lower()] += 1
            
        return frecuency_count
        
        
        
