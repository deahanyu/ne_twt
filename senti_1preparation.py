import sqlite3 as sqlite
import csv
import datetime

initial_directory = '../../../../tweets_collection_all_sources_unique.csv'
database_directory = r'../data/all_tweets.db'
print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

with open(initial_directory,'r') as dt: 
	dr = csv.DictReader(dt) # comma is default delimiteree
	toDb = [(i['text1'],i['created'],i['id'],i['screenname'],i['state']+(3-len(i['county']))*'0'+i['county']+(6-len(i['tract']))*'0'+i['tract']) for i in dr]

print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

with sqlite.connect(database_directory) as con: 
	
	con.text_factory = str
	#this is for 
	#ProgrammingError: You must not use 8-bit bytestrings unless you use a text_factory that can interpret 8-bit bytestrings (like text_factory = str). It is highly recommended that you instead just switch your application to Unicode strings.

	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS all_tweets")
	cur.execute("CREATE TABLE all_tweets (text1 text, created text, id int, screenname text, geoid text);")
	cur.executemany("INSERT INTO all_tweets (text1,created,id,screenname,geoid) VALUES (?,?,?,?,?);", toDb)
  	con.commit()

print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


	