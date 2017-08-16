import sqlite3 as sqlite
import csv
import datetime
import sys
import geoList
print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")



##-----Step 1 : creating a field of random numbers

# database_directory = r'../data/tweets_all.db'

# with sqlite.connect(database_directory) as con: 
# 	cur = con.cursor()
# 	strr = "ALTER TABLE tweets ADD COLUMN rd float"
# 	ss=cur.execute(strr)
# 	strr = "UPDATE tweets SET rd = random();"
# 	ss=cur.execute(strr)



##-----Step 2 : random sample 1000 from each tract

database_directory = r'../data/tweets_all.db'

with sqlite.connect(database_directory) as con:

	# #-----Step 2-0: to check my query works well
	# strr = "SELECT * FROM tweets AS a WHERE a.id IN (SELECT b.id FROM tweets as b WHERE b.geoid = '26125141700' AND date(created) > '2013-12-31' AND date(created) < '2017-01-01' ORDER BY rd LIMIT 1) ;"
	# ss=cur.execute(strr)
	# print ss.fetchall()
	# print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	# strr = "SELECT * FROM tweets AS a WHERE a.id IN (SELECT b.id FROM tweets as b WHERE b.geoid = '26099263200' AND date(created) > '2013-12-31' AND date(created) < '2017-01-01' ORDER BY rd LIMIT 1) ;"
	# ss=cur.execute(strr)
	# print ss.fetchall()


	cur = con.cursor()

	gList = [i[0]for i in geoList.theList]

	for i in range(len(gList)):
		
		if i == 0:
			#-----Step 2-2: to create another table with the query
			strr = "DROP TABLE IF EXISTS sorted;"
			ss = cur.execute(strr)
			strr = "CREATE TABLE sorted AS SELECT * FROM tweets AS a WHERE a.id IN (SELECT b.id FROM tweets as b WHERE b.geoid = "+str(gList[i])+" AND date(created) > '2013-12-31' AND date(created) < '2017-01-01' ORDER BY rd LIMIT 1000) ;"
			ss=cur.execute(strr)
		else:
			strr = "INSERT INTO sorted SELECT * FROM tweets AS a WHERE a.id IN (SELECT b.id FROM tweets as b WHERE b.geoid = "+str(gList[i])+" AND date(created) > '2013-12-31' AND date(created) < '2017-01-01' ORDER BY rd LIMIT 1000) ;"
			ss=cur.execute(strr)

		print i,len(gList)
		print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")



	








print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")



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


database_directory = r'../data/practice.db'
import time

pList = ['10','10','10','10','20','20','20','20']
with sqlite.connect(database_directory) as con: 
	cur = con.cursor()

	# #adding Random number column
	# strr = "ALTER TABLE tweets ADD COLUMN rd float"
	# strr = "UPDATE tweets SET rd = random();"
	# ss=cur.execute(strr)

	# #TO SEE TABLES
	# strr = "SELECT name FROM sqlite_master WHERE type = 'table';"
	# ss=cur.execute(strr)
	# print ss.fetchall()	

	with open('output.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(['Column 1', 'Column 2', 'col3','4','5','6'])
		for i in range(len(pList)):
			if i == 0: 
				strr = "SELECT * FROM tweets AS a WHERE a.subjectid IN (SELECT b.subjectid FROM tweets as b WHERE b.geoid = "+str(pList[i])+" AND date(created) > '2013-12-31' AND date(created) < '2017-01-01' ORDER BY rd LIMIT 1) ;"
				ss=cur.execute(strr)
				writer.writerows(ss.fetchall())
				
			else:
				strr = "SELECT * FROM tweets AS a WHERE a.subjectid IN (SELECT b.subjectid FROM tweets as b WHERE b.geoid = "+str(pList[i])+" AND date(created) > '2013-12-31' AND date(created) < '2017-01-01' ORDER BY rd LIMIT 1) ;"
				ss=cur.execute(strr)
				writer.writerows(ss.fetchall())
			print i,len(pList)
			time.sleep(5)


    






	