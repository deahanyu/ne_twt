import sqlite3 as sqlite
import csv
import datetime
import pandas as pd
import nltk
zzz


database_directory = r'../../data/food_tweets.db'
print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


with sqlite.connect(database_directory) as con: 
	cur = con.cursor()
	check01=cur.execute("SELECT state,county,tract FROM tweets_collection_all_sources_unique_filt")
	check01 = check01.fetchall()
	check02=cur.execute("SELECT clean_text FROM tweets_collection_all_sources_unique_filt")
	check02 = check02.fetchall()

thisColumn=[]
for i in check01:
	a=i[0]
	b='0'*(3-len(i[1]))+i[1]
	c='0'*(6-len(i[2]))+i[2]
	thisColumn.append(a+b+c)

thisC = [j[0] for j in check02]
kk = pd.DataFrame()
kk['GEOID10']= thisColumn
kk['clean_text'] = thisC
kk.to_csv('../../data/sentiment_healthiness_load_1_tweets.csv', encoding='utf-8',heading=True, index=False)



print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
