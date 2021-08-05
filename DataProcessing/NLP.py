import spacy
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.probability import FreqDist
import re

class NLP():
    """
    A class that contains all Natural Language Processing methods needed
    """
    def __init__(self, language):
        """
        Creates a NLP object

        Args:
            language (String): Language used to analyze
        """
        self.stopwords = set(stopwords.words(language))
        self.language = language
        
        if self.language == 'english':
            self.nlp = spacy.load('en_core_web_sm')
        else:
            self.nlp = spacy.load('es_core_news_sm') # Spanish
            
    def get_most_mentioned_organizations(self, top_n, limit, df):
        """
        Returns the most mentioned organizations from a replies or posts Data Frame

        Args:
            top_n (int): Top n mentioned organizations
            limit (int): Limit of replies/posts to iterate over
            df (pd.DataFrame): Replies or posts Data Frame to analyze

        Returns:
            pd.Series: Top n mentioned organizations
        """
        words = []
        n = limit if limit < len(df['tweet']) else len(df['tweet'])-1
        for i in range(n):
            sentence = df['tweet'][i]
            for word in sentence.split():
                words.append(word)
                
        normalized_words = [] # Remove punctuation
        for s in words:
            word = re.sub(r'[^A-Za-z0-9]+', '', s)
            if word != '':
                normalized_words.append(word)
        
        text = ' '.join(normalized_words)
        doc = self.nlp(text)
        
        data = {'Word' : [s.text for s in doc.ents],
                'Entity' : [s.label_ for s in doc.ents]
                }
        aux_df = pd.DataFrame(data)
        df_org = aux_df.where(aux_df['Entity'] == 'ORG') # Get only the entites that are classified as Organizations
        values = df_org['Word'].value_counts()
        
        return values[:top_n,]
        
        
        
    def get_top_frequecy_dictionary(self, df, limit):
        """
        Returns most frequent words used in a replies or posts Data Frame

        Args:
            df (pd.DataFrame): Replies or posts Data Frame to analyze
            limit (int): Limit of replies/posts to iterate over

        Returns:
            FreqDist: Frequency Dictionary that contains the frequency of each word
        """
        words = []
        n = limit if limit < len(df['tweet']) else len(df['tweet'])-1
        
        for i in range(n):
            sentence = df['tweet'][i]
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
        
        
        
