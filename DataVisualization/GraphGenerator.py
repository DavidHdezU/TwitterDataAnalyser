import numpy as np
import pandas as pd
import os
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import seaborn as sns

class GraphGenerator():
    """
    A class that generates graphs to visualize data
    """
    def create_wordcloud(self, freq_dicc):
        """
        Creates a world cloud given a frequency dictionary

        Args:
            freq_dicc (Dictionary): frequency dictionary
        """
        wc = WordCloud(background_color="black",width=1000,height=1000,relative_scaling=0.5,normalize_plurals=False).generate_from_frequencies(freq_dicc)
        plt.figure()
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.show()
        
    def create_graph_bar(self, x_label_list, y_label_list, title, xlabel_title, ylabel_title):
        """
        Creates a graph bar

        Args:
            x_label_list ([List]): Independent variable
            y_label_list ([List]): Dependent variable
            title (String): Graph title
            xlabel_title (String): Independent variable name
            ylabel_title (String): Dependent variable name
        """
        plt.figure(figsize=(20, 10))
        plt.title(title)
        sns.barplot(x=x_label_list, y=y_label_list, alpha=0.8)
        plt.xlabel(xlabel_title, fontsize=12)
        plt.ylabel(ylabel_title, fontsize=12)
        plt.show()
        
    def plot_line(self, x_label_list, y_label_list, title, xlabel_title, ylabel_title):
        """
        Plots a line given a set of (x, y) points

        Args:
            x_label_list ([List]): Independent variable
            y_label_list ([List]): Dependent variable
            title (String): Graph title
            xlabel_title (String): Independent variable name
            ylabel_title (String): Dependent variable name
        """
        plt.figure(figsize=(20, 10))
        plt.title(title)
        sns.lineplot(x=x_label_list, y=y_label_list)
        plt.xlabel(xlabel_title)
        plt.ylabel(ylabel_title)
        plt.show()
        
    def create_heatmap(self, data, title, xlabel_title, ylabel_title):
        """
        Creates a heatmap

        Args:
            data (DataFrame) : data to use
            title (String): Graph title
            xlabel_title (String): Independent variable name
            ylabel_title (String): Dependent variable name
        """
        plt.figure(figsize=(14,7))
        plt.title(title)
        sns.heatmap(data=data, annot=True)
        plt.xlabel(xlabel_title)
        plt.ylabel(ylabel_title)
        plt.show()
        
    def plot_points(self, x_label_list, y_label_list, title, xlabel_title, ylabel_title):
        """
        Método que gráfica un conjunto de puntos

        Args:
            x_label_list ([List]): Independent variable
            y_label_list ([List]): Dependent variable
            title (String): Graph title
            xlabel_title (String): Independent variable name
            ylabel_title (String): Dependent variable name
        """
        plt.figure(figsize=(20,10))
        plt.title(title)
        sns.scatterplot(x=x_label_list, y=y_label_list)
        plt.xlabel(xlabel_title)
        plt.ylabel(ylabel_title)
        plt.show()
        
    def plot_regression_line(self, x_label_list, y_label_list, title, xlabel_title, ylabel_title):
        """
        Plots a regression line given a set of (x, y) points

        Args:
            x_label_list ([List]): Independent variable
            y_label_list ([List]): Dependent variable
            title (String): Graph title
            xlabel_title (String): Independent variable name
            ylabel_title (String): Dependent variable name
        """
        plt.figure(figsize=(20,10))
        plt.title(title)
        sns.regplot(x=x_label_list, y=y_label_list)
        plt.xlabel(xlabel_title)
        plt.ylabel(ylabel_title)
        plt.show()
        
    def plot_points_3Variables(self, x_label_list, y_label_list, title, xlabel_title, ylabel_title, hue):
        """
        Plots a set points given 3 variables

        Args:
            x_label_list ([List]): Independent variable
            y_label_list ([List]): Dependent variable
            title (String): Graph title
            xlabel_title (String): Independent variable name
            ylabel_title (String): Dependent variable name
            hue (List): hue List
        """
        plt.figure(figsize=(20,10))
        plt.title(title)
        sns.scatterplot(x=x_label_list, y=y_label_list, hue=hue)
        plt.xlabel(xlabel_title)
        plt.ylabel(ylabel_title)
        plt.show()
        
    def create_categorical_graph(self, x_label_list, y_label_list, title, xlabel_title, ylabel_title):
        """
        Creates a categorical graph

        Args:
            x_label_list ([List]): Independent variable
            y_label_list ([List]): Dependent variable
            title (String): Graph title
            xlabel_title (String): Independent variable name
            ylabel_title (String): Dependent variable name
        """
        plt.figure(figsize=(20,10))
        plt.title(title)
        sns.swarmplot(x=x_label_list, y=y_label_list)
        plt.xlabel(xlabel_title)
        plt.ylabel(ylabel_title)
        plt.show()
        
    def create_histogram(self, data):
        """
        Creates a histogram given a data set

        Args:
            data (List): Data set
        """
        plt.figure(figsize=(20,10))
        sns.distplot(a=data, kde=False)
        plt.show()
    
    
    
        
    
        
    
