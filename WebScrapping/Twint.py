import twint
import pandas as pd
import numpy as np
from classifier import SentimentClassifier
import gender_guesser.detector as gender
import re
from unidecode import unidecode
from textblob import TextBlob


class TwintScrapper():
    """
    A scrapper class to get data from Twitter
    """
    def __init__(self, country=None):
        """
        Creates a Twint Scapper object

        Args:
            country (String): Contries to make more accurate the gender guesser
        """
        if country == "spain": # In case we're evaluating only spanish comments/posts
            self.clf = SentimentClassifier() # Spanish sentiment classifier
            
            
        self.genderD = gender.Detector() # Gender detector
        self.country = country
        
        # Auxiliary mexican names
        nom_mujeres = "Mary, Marcella, Marcela, Luciana, Dory, María, Guadalupe, Margarita, Sofía, Camila, Josefina, Verónica, María Elena, Leticia, Rosa, Teresa, Alicia, Alejandra, Martha, Patricia, Elizabeth, Gabriela, Andrea, Lucía, Valentina, Isabella, Ximena, Natalia, Mía, María Fernanda, Nicole, Melanie, Regina, Renata, Antonella, Luna, Constanza, Zoe, Michelle, Aitana, Stephanie, María Luisa, Ana María, Adriana, María de Jesús, María Camila, Samantha, Mariana, María José, Alexa, Thalia, Bertha, Ingrid, Denisse, Karina, Andy, Arely, Edith, Grissel, Jocelyn, Joselyne, Karen, Kari, Minerva, Rubí, Susana, Carol, Mirna, Lore, Lorena"
        list_mujeres = nom_mujeres.split(", ")
        self.nombre_mujeres = set()
        for s in list_mujeres:
            self.nombre_mujeres.add(unidecode(s.lower()))
        
        nom_hombres = "Jony, Josue, Juan, Alex, Obed, Toño, Checo, Brandon, Alejandro, Juan, José Luis, Francisco, José, Pedro, Manuel, Juan Carlos, Roberto, Fernando, Daniel, Miguel Ángel, José Francisco, Jesús Antonio, Alejandro, Ricardo, Daniel, Jorge, Ricardo, Javier, Raúl, David, Enrique, Alfredo, Gabriel, Andrés, Pablo, Rubén, Diego, Rafael, Roberto, Carlos, Francisco Javier, Juan Manuel, Santiago, Sebastián, Diego, Nicolás, Daniel, Mateo, Matías, Gabriel, Emiliano, Rodrigo, Juan Pablo, Emmanuel, Emilio, Christopher, Jonathan, Iker, Gustavo, Pascual, Irving, Noé, Javier, Aquiles, Carlos, César, Dan, Dr., Gerardo, Héctor, Hiram, Julian, Johnny, Oscar, Ricky, Henry"
        list_hombres = nom_hombres.split(", ")
        self.nombre_hombres = set()
        for s in list_hombres:
            self.nombre_hombres.add(unidecode(s.lower()))
            
            
        
    def classify_text(self, text):
        """
        Classifies a text as Positive, Negative or Neutral

        Args:
            text (String): Text to classify

        Returns:
            String: The text classification
        """
        if self.country and self.country == "spain":
            res_text = self.clf.predict(text)
            
            if 0.5 <= res_text <= 0.55:
                return "Neutral"
            elif res_text < 0.5:
                return "Negative"
            else:
                return "Positive"
        
        analysis = TextBlob(text)
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return "Positive"
        elif analysis.sentiment.polarity == 0:
            return "Neutral"
        
        return "Negative"
    
    
    
    
    def classify_gender(self, name):
        """
        Guess the gender given a string, the string has to be a name in order to be right classified

        Args:
            name (String): Name to classify

        Returns:
            String: The gender guessed, it can be: male, female or unknown
        """
        first_name = name.split(" ", 1)[0]
        
        if self.country:
            g = self.genderD.get_gender(first_name, self.country)
        else:
            g = self.genderD.get_gender(first_name)
            
        if g == "unknown" or g == "andy":
            low = unidecode(first_name.lower())
            
            if low in self.nombre_hombres:
                return "male"
            elif low in self.nombre_mujeres:
                return "female"
            else:
                return "unknown"
            
        if g == "mostly_male":
            return "male"
        if g == "mostly_female":
            return "female"
            
        return g
    
        
        
        
        
    def search_replies_to(self, user, since, until, save_file, out_file):
        """
        Gets the replies to a user in a given range of time

        Args:
            user (String): User to search for replies
            since (String): Start date
            until (String): End date
            save_file (Bool): Indicator to save the df file
        """
        replies = twint.Config()
        replies.To = user
        replies.Until = until
        replies.Since = since
        replies.Hide_output = True
        replies.Pandas = True
        replies.Pandas_clean = True
                
        if save_file:
            replies.Store_csv = True
            replies.Output = out_file
            
        try:
            twint.run.Search(replies)    
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print("Problem with %s." % since)
        return twint.storage.panda.Tweets_df[["conversation_id",  "tweet", "name"]]
        
        
        
        
    def search_user_posts(self, user, since, until, save_file):
        """
        Gets the user's post in a given range of time

        Args:
            user (String): User to search for his posts
            since (String): Start date
            until (String): End date
            output (String): Output .csv file name
        """
        tweets = twint.Config()
        tweets.Username = user
        tweets.Since =  since
        tweets.Until = until
        tweets.Hide_output = True
        tweets.Pandas =  True
        tweets.Pandas_clean = True
        
        if save_file:
            tweets.Store_csv = True
            tweets.Output = user + "_posts.csv"
            
        twint.run.Search(tweets)    
            
        return twint.storage.panda.Tweets_df[["id", "conversation_id", "date", "tweet", "nretweets", "nlikes", "nreplies"]]
        
        
        
        
    def clean_tweet(self, text):
        """
        Auxiliary method to remove url, mentions and hashtags
        Args:
            tweet (String): Tweet text

        Returns:
            String: Normalized tweet text
        """
        text = re.sub(r"http\S+", "", text) #remove urls
        text=re.sub(r'\S+\.com\S+','',text) #remove urls
        text=re.sub(r'\@\w+','',text) #remove mentions
        text =re.sub(r'\#\w+','',text) #remove hashtags
        return text
    
    
    
    
    def clean_df_replies(self, df):
        """
        Method to get the data we care about in the replies Data Frame

        Args:
            df (pd.DataFrame): replies Data Frame

        """
        
        df['tweet'] = df['tweet'].apply(lambda s : self.clean_tweet(s))
        df['name'] = df['name'].replace(np.nan, "")
        df['gender'] = df['name'].apply(lambda s :self.classify_gender(s))
        df['sentiment'] = df['tweet'].apply(lambda s : self.classify_text(s))
    
    
    
    
    
    def clean_df_posts(self, df_posts, df_replies):
        """
        Method to get the data we care about in a given Data Frame

        Args:
            df_posts (pd.DataFrame): posts Data Frame to 'clean'
            df_replies (pd.DataFrame) : cleaned replies Data Frame

        """
        df_posts['date'] = pd.to_datetime(df_posts['date'])
        
        # We're just going to count how many males, females and unkwnows are in each post
        # We're also counting how many positive, negative and neutral comments are for each post
        aux_dicc = {}
        for i in range((len(df_replies['tweet']))):
            if df_replies['conversation_id'][i] not in aux_dicc:
                aux_dicc[df_replies['conversation_id'][i]] = [0, 0, 0, 0, 0, 0]
                
                if df_replies['sentiment'][i] == 'Positive':
                    aux_dicc[df_replies['conversation_id'][i]][3] += 1
                elif df_replies['sentiment'][i] == 'Negative':
                    aux_dicc[df_replies['conversation_id'][i]][4] += 1
                else:
                    aux_dicc[df_replies['conversation_id'][i]][5] += 1
                    
                if df_replies['gender'][i] == "male":
                    aux_dicc[df_replies['conversation_id'][i]][0] += 1
                elif df_replies['gender'][i] == "female":
                    aux_dicc[df_replies['conversation_id'][i]][1] += 1
                else:
                    aux_dicc[df_replies['conversation_id'][i]][2] += 1
                    
            else:
                if df_replies['sentiment'][i] == 'Positive':
                    aux_dicc[df_replies['conversation_id'][i]][3] += 1
                elif df_replies['sentiment'][i] == 'Negative':
                    aux_dicc[df_replies['conversation_id'][i]][4] += 1
                else:
                    aux_dicc[df_replies['conversation_id'][i]][5] += 1
                    
                if df_replies['gender'][i] == "male":
                    aux_dicc[df_replies['conversation_id'][i]][0] += 1
                elif df_replies['gender'][i] == "female":
                    aux_dicc[df_replies['conversation_id'][i]][1] += 1
                else:
                    aux_dicc[df_replies['conversation_id'][i]][2] += 1
        
        df_posts['males_count'] = np.zeros(len(df_posts['tweet']), dtype=np.int64)
        df_posts['females_count'] = np.zeros(len(df_posts['tweet']), dtype=np.int64)
        df_posts['unknown_count'] = np.zeros(len(df_posts['tweet']), dtype=np.int64)
        df_posts['positives_com'] = np.zeros(len(df_posts['tweet']), dtype=np.int64)
        df_posts['negatives_com'] = np.zeros(len(df_posts['tweet']), dtype=np.int64)
        df_posts['neutral_com'] = np.zeros(len(df_posts['tweet']), dtype=np.int64)
        
        for i in range(len(df_posts['conversation_id'])):
            if df_posts['conversation_id'][i] in aux_dicc:
                df_posts['males_count'][i] = aux_dicc[df_posts['conversation_id'][i]][0]
                df_posts['females_count'][i] = aux_dicc[df_posts['conversation_id'][i]][1]
                df_posts['unknown_count'][i] = aux_dicc[df_posts['conversation_id'][i]][2]
                df_posts['positives_com'][i] = aux_dicc[df_posts['conversation_id'][i]][3]
                df_posts['negatives_com'][i] = aux_dicc[df_posts['conversation_id'][i]][4]
                df_posts['neutral_com'] = aux_dicc[df_posts['conversation_id'][i]][5]
            
        
        df_posts['coef_acceptation'] = np.zeros(len(df_posts['tweet'])) # We're going to calculate it later
        
        df_posts = df_posts.sort_values(by="date", ascending=False)     # Sort Posts DF by date    
    
    

    
    
    
    
            
            
        
        

        
            

        
