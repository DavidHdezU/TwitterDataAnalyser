import numpy as np
import pandas as pd
import os
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import seaborn as sns

class GraphGenerator():
    """
    Una clase para generar gráficas que se necesiten para visualizar de mejor manera el analisis hecho
    """
    def genera_wordcloud(self, dicc_frecuencia):
        """
        Método que genera un wordcloud mediante un diccionario de frecuencias

        Args:
            dicc_frecuencia (Diccionario): Diccionario de frecuecias
        """
        wc = WordCloud(background_color="black",width=1000,height=1000,relative_scaling=0.5,normalize_plurals=False).generate_from_frequencies(dicc_frecuencia)
        plt.figure()
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.show()
        
    def genera_grafica_barras(self, x_label_list, y_label_list, title, xlabel_title, ylabel_title):
        """
        Método que genera una gráfica de barras

        Args:
            x_label_list ([Lista]): Variable independiente
            y_label_list ([Lista]): Variable dependinete
            title (String): Titulo de la gráfica
            xlabel_title (String): Nombre de la variable independiente
            ylabel_title (String): Nombre de la variable dependiente
        """
        plt.figure(figsize=(20, 10))
        plt.title(title)
        sns.barplot(x=x_label_list, y=y_label_list, alpha=0.8)
        plt.xlabel(xlabel_title, fontsize=12)
        plt.ylabel(ylabel_title, fontsize=12)
        plt.show()
        
    def genera_grafica_linea(self, x_label_list, y_label_list, title, xlabel_title, ylabel_title):
        """
        Método que genera una gráfica de linea

        Args:
            x_label_list ([Lista]): Variable independiente
            y_label_list ([Lista]): Variable dependinete
            title (String): Titulo de la gráfica
            xlabel_title (String): Nombre de la variable independiente
            ylabel_title (String): Nombre de la variable dependiente
        """
        plt.figure(figsize=(20, 10))
        plt.title(title)
        sns.lineplot(x=x_label_list, y=y_label_list)
        plt.xlabel(xlabel_title)
        plt.ylabel(ylabel_title)
        plt.show()
        
    def genera_heatmap(self, data, title, xlabel_title, ylabel_title):
        """
        Método que genera un mapa de calor

        Args:
            data (DataFrame) : Data a usar
            title (String): Titulo de la gráfica
            xlabel_title (String): Nombre de la variable independiente
            ylabel_title (String): Nombre de la variable dependiente
        """
        plt.figure(figsize=(14,7))
        plt.title(title)
        sns.heatmap(data=data, annot=True)
        plt.xlabel(xlabel_title)
        plt.ylabel(ylabel_title)
        plt.show()
        
    def genera_grafica_puntos(self, x_label_list, y_label_list, title, xlabel_title, ylabel_title):
        """
        Método que gráfica un conjunto de puntos

        Args:
            x_label_list ([Lista]): Variable independiente
            y_label_list ([Lista]): Variable dependiente
            title (String): Titulo de la gráfica
            xlabel_title (String): Nombre de la variable independiente
            ylabel_title (String): Nombre de la variable dependiente
        """
        plt.figure(figsize=(20,10))
        plt.title(title)
        sns.scatterplot(x=x_label_list, y=y_label_list)
        plt.xlabel(xlabel_title)
        plt.ylabel(ylabel_title)
        plt.show()
        
    def genera_regression_line(self, x_label_list, y_label_list, title, xlabel_title, ylabel_title):
        """
        Método que genera una linea de regresión dado un conjunto de puntos

        Args:
            x_label_list ([Lista]): Variable independiente
            y_label_list ([Lista]): Variable dependinete
            title (String): Titulo de la gráfica
            xlabel_title (String): Nombre de la variable independiente
            ylabel_title (String): Nombre de la variable dependiente
        """
        plt.figure(figsize=(20,10))
        plt.title(title)
        sns.regplot(x=x_label_list, y=y_label_list)
        plt.xlabel(xlabel_title)
        plt.ylabel(ylabel_title)
        plt.show()
        
    def genera_grafica_puntos_3Variables(self, x_label_list, y_label_list, title, xlabel_title, ylabel_title, hue):
        """
        Método que genera una gráfica de puntos, dado 3 variables

        Args:
            x_label_list ([Lista]): Variable independiente
            y_label_list ([Lista]): Variable dependinete
            title (String): Titulo de la gráfica
            xlabel_title (String): Nombre de la variable independiente
            ylabel_title (String): Nombre de la variable dependiente
            hue (List): Tercera variable
        """
        plt.figure(figsize=(20,10))
        plt.title(title)
        sns.scatterplot(x=x_label_list, y=y_label_list, hue=hue)
        plt.xlabel(xlabel_title)
        plt.ylabel(ylabel_title)
        plt.show()
        
    def genera_grafica_categorica(self, x_label_list, y_label_list, title, xlabel_title, ylabel_title):
        """
        Método que genera una gráfica categorica

        Args:
            x_label_list ([Lista]): Variable independiente
            y_label_list ([Lista]): Variable dependinete
            title (String): Titulo de la gráfica
            xlabel_title (String): Nombre de la variable independiente
            ylabel_title (String): Nombre de la variable dependiente
        """
        plt.figure(figsize=(20,10))
        plt.title(title)
        sns.swarmplot(x=x_label_list, y=y_label_list)
        plt.xlabel(xlabel_title)
        plt.ylabel(ylabel_title)
        plt.show()
        
    def genera_grafica_histograma(self, data):
        """
        Método que genera un histograma dado un conjunto de datos

        Args:
            data (List): Conjunto de datos a usar
        """
        plt.figure(figsize=(20,10))
        sns.distplot(a=data, kde=False)
        plt.show()
    
    
    
        
    
        
    
