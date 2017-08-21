import re
#from nltk.tokenize import word_tokenize
import codecs
import string
import csv
import nltk
import preprocessor as p
from HTMLParser import HTMLParser
import pandas as pd 

#---Change directories below
#---Go to line 76 and change deahan to jin
#---Run it ! 

liwc_dir = 'data/combinePosNegWords_LIWC.csv'
newliwc_dir = 'data/combined_pos_neg_LIWC_with_brad_add_ins.csv'
twtdata_dir = 'data/dataForSentiment.csv'
write_dir = 'output/allFoodTweets_sentiment_1sthalf.csv'

totalNumber = 1661642
half = 1661642/2
deahan = range(0,half)
jin = range(half,totalNumber+1)


####################### CREATING POSITIVE NEGATIVE LIST #########################


neg_old = []
pos_old = [] 
neg_new = []
pos_new = []

with open(liwc_dir,'r') as f:
	file1 = csv.reader(f)
	file1.next()
	for row in file1:
		if row[1] != '':
			neg_old.append(row[1])
		if row[0] != '':
			pos_old.append(row[0])

with open(newliwc_dir,'r') as f:
	file2 = csv.reader(f)
	file2.next()
	for row in file2:
		if row[1] != '':
			neg_new.append(row[1])
		if row[0] != '':
			pos_new.append(row[0])

########################## TOKENIZING/LABELING TWEETS ###########################
def clean(text):
	h = HTMLParser()
	#p.set_options(p.OPT.EMOJI)
	#cleantext = p.clean(text.encode('utf-8'))
	cleantext=text
	cleantext = cleantext.replace('&#8217;', '\'')
	cleantext = h.unescape(cleantext)
	cleantext = re.sub(r"http\S*", ' ', cleantext)
	cleantext = re.sub(r"@[A-Za-z0-9_]+", '@username', cleantext)
	cleantext = re.sub(ur"[^\w\d'/#:$@.\-\s,]+",' ',cleantext)
	cleantext = re.sub(r"([^0-9]+),([^0-9]+)", r"\1 \2",cleantext)
	cleantext = re.sub(r"[.]+([^A-Za-z0-9$#]+|$)",' ', cleantext)
	cleantext = re.sub(r"[:]+[^0-9]",' ', cleantext)
	cleantext = re.sub(r"([^A-Za-z0-9][-][^0-9])|(- )",' ', cleantext)
	cleantext = re.sub(r"[#]", " #", cleantext)
	finaltext = cleantext.replace('  ',' ').lower()
	return finaltext

ste_handle = nltk.stem.SnowballStemmer('english')

with codecs.open(twtdata_dir,encoding='iso-8859-1') as twts:
	twts=twts.readlines()

with open(write_dir, 'w') as newfile:
	newfile.write(', '.join(('text_cleaned','Old_sentiment_words','Old_positive','Old_negative','New_sentiment_words','New_positive','New_negative\r\n')))
	for i in deahan:
		if i!=0:
			eachTwt=twts[i]
			eachTwt=eachTwt.replace('\n','')
			newEachTwt=[]

			newEachTwt = clean(eachTwt)
			newEachTwt = newEachTwt.replace(',','').replace('_','').split(' ')
			newEachTwt = [a for a in newEachTwt if len(a)>0]

			positive_old = 0
			negative_old = 0
			sentiPos_old=[]
			sentiNeg_old=[]
			positive_new = 0
			negative_new = 0
			sentiPos_new=[]
			sentiNeg_new=[]

			for l in newEachTwt:
				stem = ste_handle.stem(l)
				if l in pos_old or stem in pos_old:
					positive_old += 1
					sentiPos_old.append(l)
				elif l in neg_old or stem in neg_old:
					negative_old += 1
					sentiNeg_old.append(l)
				if l in pos_new or stem in pos_new:
					positive_new += 1
					sentiPos_new.append(l)
				elif l in neg_new or stem in neg_new:
					negative_new += 1
					sentiNeg_new.append(l)
			totalSenti_old=sentiPos_old+sentiNeg_old
			totalSenti_new=sentiPos_new+sentiNeg_new
			row=(' '.join(newEachTwt),'/'.join(totalSenti_old),str(positive_old),str(negative_old),'/'.join(totalSenti_new),str(positive_new), str(negative_new))
			newfile.write(', '.join(row).encode('iso-8859-1')+'\n')
			print i
newfile.close()