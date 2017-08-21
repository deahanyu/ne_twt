import sqlite3 as sqlite
import csv
import datetime
import sys
import geoList
import codecs
import string
import nltk
import re
from HTMLParser import HTMLParser
print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
sys.path.append('/Users/deahanyu/anaconda/lib/python2.7/site-packages')

# ##-----Step 1 : creating a field of random numbers

# # database_directory = r'../../data/tweets_all.db'

# # with sqlite.connect(database_directory) as con: 
# # 	cur = con.cursor()
# # 	strr = "ALTER TABLE tweets ADD COLUMN rd float"
# # 	ss=cur.execute(strr)
# # 	strr = "UPDATE tweets SET rd = random();"
# # 	ss=cur.execute(strr)


# ##-----Step 2 : random sample 1000 from each tract

# def clean(text):
# 	h = HTMLParser()
# 	cleantext = text.replace('&#8217;', '\'')
# 	cleantext = h.unescape(cleantext)
# 	cleantext = re.sub(r"@[A-Za-z0-9_]+", '@username', cleantext)
# 	cleantext = re.sub(ur"[^\w\d'/#:$@.\-\s,]+",' ',cleantext)
# 	cleantext = re.sub(r"([^0-9]+),([^0-9]+)", r"\1 \2",cleantext)
# 	cleantext = re.sub(r"[.]+([^A-Za-z0-9$#]+|$)",' ', cleantext)
# 	cleantext = re.sub(r"[:]+[^0-9]",' ', cleantext)
# 	cleantext = re.sub(r"([^A-Za-z0-9][-][^0-9])|(- )",' ', cleantext)
# 	cleantext = re.sub(r"[#]", " #", cleantext)
# 	finaltext = cleantext.replace('  ',' ').lower()
# 	return finaltext

# database_directory = r'../../data/tweets_all.db'

# with sqlite.connect(database_directory) as con:

# 	cur = con.cursor()

# 	# #-----Step 2-0: to check my query works well
# 	# strr = "SELECT * FROM tweets AS a WHERE a.id IN (SELECT b.id FROM tweets as b WHERE b.geoid = '26125141700' AND date(created) > '2013-12-31' AND date(created) < '2017-01-01' ORDER BY rd LIMIT 1) ;"
# 	# ss=cur.execute(strr)
# 	# print ss.fetchall()
# 	# print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# 	# strr = "SELECT * FROM tweets AS a WHERE a.id IN (SELECT b.id FROM tweets as b WHERE b.geoid = '26099263200' AND date(created) > '2013-12-31' AND date(created) < '2017-01-01' ORDER BY rd LIMIT 1) ;"
# 	# ss=cur.execute(strr)
# 	# print ss.fetchall()

# 	gList = [i[0]for i in geoList.theList]
# 	with open('new_sorted_222.csv', 'wb') as wo:
# 		# writer = csv.writer(f)
# 		# writer.writerow(['text1', 'created', 'id','screenname','geoid'])
# 		wo.write('text_cleaned,created,id,screeenname,geoid\n')
# 		for i in range(len(gList)):
# 			if i >= 1319:
# 				# strr = "SELECT * FROM tweets AS a WHERE a.id IN (SELECT b.id FROM tweets as b WHERE b.geoid = "+str(gList[i])+" AND date(created) > '2013-12-31' AND date(created) < '2017-01-01' ORDER BY rd LIMIT 1500) ;"
# 				strr = "SELECT * FROM tweets WHERE geoid = "+str(gList[i])+" AND date(created) > '2013-12-31' AND date(created) < '2017-01-01' ORDER BY rd LIMIT 1500;"
# 				ss = cur.execute(strr)
# 				ss = ss.fetchall()
# 				count = 1
# 				for j in range(len(ss)):
# 					if count <= 1000: 
# 						eachTwt = ss[j][0].replace('\n','').replace('\r','').replace('\r\n','')
# 						eachTwt = clean(eachTwt).replace(',','').replace('_','').split(' ')
# 						eachTwt = [a for a in eachTwt if len(a)>0]
# 						eachTwt = ' '.join(eachTwt)
# 						if len(eachTwt)!=0:
# 							wo.write('{},{},{},{},{}\n'.format(eachTwt,ss[j][1].encode('utf-8'),ss[j][2],ss[j][3].encode('utf-8'),ss[j][4].encode('utf-8')))
# 							count+=1
# 				print i,len(gList)
# 				print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")



##-----Step 3 : aggregate each csv file from step 2 



z1 = pd.read_csv('new_sorted_1.csv')
z2 = pd.read_csv('new_sorted_222.csv')

print len(z1.index)
print len(z2.loc[~(z2['geoid']==26125138301)].index)
z1 = z1.append(z2.loc[~(z2['geoid']==26125138301)], ignore_index=True)
print len(z1.index)
print len(z1.geoid.unique())


#z1.to_csv('../../data/sentiment_random_sample_1_tweets.csv',encoding='utf-8', index=False)



#--------practice code

# database_directory = r'../data/practice.db'
# toDb=[('a','a','2015-01-02','10','10'),('b','a','2015-01-02','10','10'),('c','a','2013-01-02','10','10'),('d','d','2015-01-02','20','20'),('e','d','2015-01-02','20','20'),('f','d','2013-01-02','20','20')]
# with sqlite.connect(database_directory) as con: 
	
# 	con.text_factory = str
# 	#this is for 
# 	#ProgrammingError: You must not use 8-bit bytestrings unless you use a text_factory that can interpret 8-bit bytestrings (like text_factory = str). It is highly recommended that you instead just switch your application to Unicode strings.

# 	cur = con.cursor()
# 	cur.execute("DROP TABLE IF EXISTS tweets")
# 	cur.execute("CREATE TABLE tweets (subjectid text,zzz text, created text, geoid text,kkk text);")
# 	cur.executemany("INSERT INTO tweets (subjectid,zzz,created,geoid,kkk) VALUES (?,?,?,?,?);", toDb)
#   con.commit()


# database_directory = r'../data/practice.db'
# import time

# pList = ['10','10','10','10','20','20','20','20']
# with sqlite.connect(database_directory) as con: 
# 	cur = con.cursor()

# 	# #adding Random number column
# 	# strr = "ALTER TABLE tweets ADD COLUMN rd float"
# 	# strr = "UPDATE tweets SET rd = random();"
# 	# ss=cur.execute(strr)

# 	# #TO SEE TABLES
# 	# strr = "SELECT name FROM sqlite_master WHERE type = 'table';"
# 	# ss=cur.execute(strr)
# 	# print ss.fetchall()	

# 	with open('output.csv', 'wb') as f:
# 		writer = csv.writer(f)
# 		writer.writerow(['Column 1', 'Column 2', 'col3','4','5','6'])
# 		for i in range(len(pList)):
# 			if i == 0: 
# 				strr = "SELECT * FROM tweets AS a WHERE a.subjectid IN (SELECT b.subjectid FROM tweets as b WHERE b.geoid = "+str(pList[i])+" AND date(created) > '2013-12-31' AND date(created) < '2017-01-01' ORDER BY rd LIMIT 1) ;"
# 				ss=cur.execute(strr)
# 				writer.writerows(ss.fetchall())
				
# 			else:
# 				strr = "SELECT * FROM tweets AS a WHERE a.subjectid IN (SELECT b.subjectid FROM tweets as b WHERE b.geoid = "+str(pList[i])+" AND date(created) > '2013-12-31' AND date(created) < '2017-01-01' ORDER BY rd LIMIT 1) ;"
# 				ss=cur.execute(strr)
# 				writer.writerows(ss.fetchall())
# 			print i,len(pList)
# 			time.sleep(5)


    






	