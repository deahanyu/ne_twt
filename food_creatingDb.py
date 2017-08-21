import sqlite3 as sqlite
import csv
import datetime
import unicodecsv

initial_directory1 = '../../data/head.sql'
initial_directory2 = '../../data/tweets_collection_all_sources_unique_filt_new.sql'
database_directory = r'../../data/food_tweets.db'
print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

fd = open(initial_directory1, 'r')
sqlFile = fd.read()
fd.close()

sqlCommands = [k.replace('\n','')+';' for k in sqlFile.split(';') if len(k.replace('\n',''))>0 ][:-1]

fd = open(initial_directory2, 'r')
sqlFile = fd.read()
fd.close()
sqlFile = sqlFile.split('\n')
sqlFile = [tuple(each.split('\t')) for each in sqlFile if len(tuple(each.split('\t')))==43]

with sqlite.connect(database_directory) as con: 
	
	con.text_factory = str
	#this is for 
	#ProgrammingError: You must not use 8-bit bytestrings unless you use a text_factory that can interpret 8-bit bytestrings (like text_factory = str). It is highly recommended that you instead just switch your application to Unicode strings.

	cur = con.cursor()
	for i in sqlCommands:
		try:
			cur.execute(i)
		except:
			print i
	cur.executemany('''INSERT INTO tweets_collection_all_sources_unique_filt 
		(text,clean_text,food_related,word_count,food_words,num_food_words,
		food_words_healthy1,num_healthy1,food_words_healthy2,num_healthy2,
		food_words_unhealthy1,num_unhealthy1,food_words_unhealthy2,num_unhealthy2,
		food_words_alcohol,num_alcohol,score_unhealthy,score_healthy,score_sum,
		senti_pos,senti_neg,num_senti_pos,num_senti_neg,id,source_collection,
		truncated,replytosid,replytosn,replytouid,favorited,favoritecount,
		created,statussource,screenname,retweetcount,isretweet,retweeted,latitude,
		longitude,tract,state,county,countyname) 
		VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);''',sqlFile)
  	con.commit()


