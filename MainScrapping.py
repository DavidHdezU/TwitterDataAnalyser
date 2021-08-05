from WebScrapping.Twint import TwintScrapper
from DataProcessing.NLP import NLP
from DataVisualization.GraphGenerator import GraphGenerator
import sys
import pandas as pd
import time
import datetime
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
from datetime import timedelta
from string import ascii_letters, digits
from os import mkdir, path
from glob import glob

USE="Usage\n Scrapping: python main.py [r or p] <twitter_username> <YY-MM-DD> <YY-MM-DD> <csv_name.csv>\n"
USE += "Clean Scrapping: python main.py [r or p] [c or cp] <twitter_username> <YY-MM-DD> <YY-MM-DD> <csv_name.csv>\n"
USE += "r flag is for getting the replies to a user in a given range of time.\n"
USE += "p flag is for getting the user's posts in a given range of time.\n"
USE += "c flag is for 'cleaning' the scrapped data, see TwitterScrapper documentation for more info.\n"
USE += "cp flag is for getting 'all data that matters' from all posts in the given range of time, see TwitterScrapper documentation for more info."


class Main():
    def __init__(self, args, upload_to_sheets):
        if len(args) == 1 or len(args) <= 4 or len(args) > 7:
            print(USE)
            sys.exit(-1)
        self.upload_to_sheets = upload_to_sheets
        if self.upload_to_sheets:
            self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            self.credentials = ServiceAccountCredentials.from_json_keyfile_name('sheets_cred.json', self.scope)
            self.client = gspread.authorize(self.credentials)
        self.args = args
        self.scrapper = TwintScrapper()
        self.graph_gen = GraphGenerator()
        self.nlp = NLP()
        
    
    def merge_dfs(self, df_list):
        """
        Returns a merged Data Frame

        Args:
            df_list (List): Data Frames list

        Returns:
            [pd.DataFrame]: DataFrame merged
        """
        df = pd.concat(df_list, ignore_index=True, sort=False)
        return df
        
    
    def twint_loop(self, searchterm, start, end):
        """
        Fetchs comments and/or posts day by day, given a range

        Args:
            searchterm (String): User to search
            start (String): Start date
            end (String): End date

        Returns:
            [List]: List of replies/posts Data Frames
        """
        daterange = pd.date_range(start, end)
        df_list = []
        for start_date in daterange:    
            since= start_date.strftime("%Y-%m-%d")
            until = (start_date + timedelta(days=1)).strftime("%Y-%m-%d")
            print('Getting %s ' % since )
            df = self.scrapper.search_replies_to(searchterm, since, until, False, "")
            print(type(df['conversation_id'][0]))

            df_list.append(df)
        return df_list
        
    def main(self):
        """
        Main method
        """
        if len(self.args) == 5:
            user_name = str(self.args[2])
            start_date = str(self.args[3])
            end_date = str(self.args[4])
            
            if self.args[1] == "r":
                self.scrapper.search_replies_to("@"+user_name, start_date, end_date, True, "")
                
            elif self.args[1] == "p":
                self.scrapper.search_user_posts(user_name, start_date, end_date, True)
                
            elif self.args[1] == "cp":
                begin_time = datetime.datetime.now()
                posts = self.scrapper.search_user_posts(user_name, start_date, end_date, False)
                print(posts)
                print("Fetched " + user_name + " posts...")
                
                replies = self.scrapper.search_replies_to("@"+user_name, start_date, end_date, False, "")
                print("Fetched " + user_name + " replies...")
                
                
                self.scrapper.clean_df_replies(replies)
                print("Normlized replies DF...")
                
                self.scrapper.clean_df_posts(posts, replies)
                print("Normlized posts DF...")
                
                replies.to_csv(user_name + "_" "replies.csv", index=False)
                print("The replies Data Base was saved as: " + user_name + "_" "replies.csv")
                
                posts.to_csv(user_name + "_" "posts.csv", index=False)
                print("The posts Data Base was saved as: " + user_name + "_" "posts.csv")
                
                if self.upload_to_sheets:
                    sp_key = '1WPjaPpaUslHj6dQZgnTyX8AuGP0iQYl7r2boFtKQJ-g'
                    wks_replies, wks_posts = 'Replies', 'Posts'
                    
                    d2g.upload(posts, sp_key, wks_posts, credentials=self.credentials, row_names=True)
                    print("Posts DF uploaded to Google Sheets...")
                    d2g.upload(replies, sp_key, wks_replies, credentials=self.credentials, row_names=True)
                    print("Replies DF uploaded to Google Sheets...")
                    
                frecuncy_word_in_replies = NLP.top_frequent_words_in_replies(replies, 100)
                frecuncy_word_in_replies.plot(20)
                
                print("-#"*30)
                print("The script ran in:")
                print(datetime.datetime.now() - begin_time)
                
        elif len(self.args) == 7:
            user_name = self.args[3]
            start_date = self.args[4]
            end_date = self.args[5]
            csv_name = self.args[6]
            if self.args[2] == "c": 
                if self.args[1] == "r":
                    self.scrapper.search_replies_to("@"+user_name, start_date, end_date, csv_name + ".csv")
                    df = pd.read_csv(csv_name+".csv")
                    self.scrapper.clean_df(df).to_csv(csv_name+"_clean.csv")
                elif self.args[1] == "p":
                    self.scrapper.search_user_posts(user_name, start_date, end_date, csv_name + ".csv")
                    df = pd.read_csv(csv_name+".csv")
                    self.scrapper.clean_df(df).to_csv(csv_name + "_clean.csv")
            else:
                print(USE)
                sys.exit(-1)
                
             
                
if __name__ == "__main__":
    handler = Main(sys.argv, False)
    handler.main()