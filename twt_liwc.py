import re
#from nltk.tokenize import word_tokenize
import codecs
import string
import csv
import nltk
import preprocessor as p
from HTMLParser import HTMLParser

####################### CREATING POSITIVE NEGATIVE LIST #########################
neg_old = []
pos_old = [] 
neg_new = []
pos_new = []
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


with open('data/combinePosNegWords_LIWC.csv','r') as f:
	file1 = csv.reader(f)
	file1.next()
	for row in file1:
		if row[1] != '':
			neg_old.append(row[1])
		if row[0] != '':
			pos_old.append(row[0])

with open('data/combined_pos_neg_LIWC_with_brad_add_ins.csv','r') as f:
	file2 = csv.reader(f)
	file2.next()
	for row in file2:
		if row[1] != '':
			neg_new.append(row[1])
		if row[0] != '':
			pos_new.append(row[0])

########################## TOKENIZING/LABELING TWEETS ###########################
cat_twts = []
ste_handle = nltk.stem.SnowballStemmer('english')

with codecs.open('data/dataForSentiment.csv',encoding='iso-8859-1') as twts:
	twts=twts.readlines()

 

kk = 1#all food tweets data is 1 and the small set was 0.



with open('output/allFoodTweets_sentiment_0809.csv', 'w') as newfile:
	#newfile.write(', '.join(('text','label','cats','positive','negative\r\n')))
	newfile.write(', '.join(('text_cleaned','sentiment_words','positive','negative\r\n')))
	#'Old_sentiment_words','Old_positive','Old_negative','New_sentiment_words','New_positive','New_negative\r\n')))
	for i in range(len(twts)):
		if kk==0:
			splitter = re.findall(r'\,[0-1]\,dummy',twts[i])
			if len(splitter) != 1:
			#Ignore this unless you see this statement on the terminal. This is just in case we have tweets that contain our splitter format by any chance. 
				print str(i)+'th tweet does not follow   ,[0 or 1],dummy   format.'
			else:
				c=twts[i].split(splitter[0])
				eachTwt=c[0]
				newEachTwt=[]
				## eachTwtTwokenized = word_tokenize(eachTwt)
				# eachTwtTwokenized = eachTwt.split(' ')
				# for j in range(len(eachTwtTwokenized)):
				# 	listOfTokens = re.findall(r'[\'a-zA-z0-9]*',eachTwtTwokenized[j])
				# 	newString = ''.join(listOfTokens)
				# 	for l in string.punctuation:
				# 		newString=newString.replace(l,'')
				# 	if len(newString)!=0:
				# 		newEachTwt.append(newString.lower())
				# print newEachTwt
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
				#cat_twts.append((twts[i].rstrip(), unicode(positive), unicode(negative)))
				cat_twts.append((twts[i].rstrip(),' '.join(newEachTwt),'/'.join(totalSenti_old),str(positive_old),str(negative_old),'/'.join(totalSenti_new),str(positive_new), str(negative_new)))
		else: 
			if i!=0:
				eachTwt=twts[i]
				eachTwt=eachTwt.replace('\n','')
				newEachTwt=[]
					## eachTwtTwokenized = word_tokenize(eachTwt)
					# eachTwtTwokenized = eachTwt.split(' ')
					# for j in range(len(eachTwtTwokenized)):
					# 	listOfTokens = re.findall(r'[\'a-zA-z0-9]*',eachTwtTwokenized[j])
					# 	newString = ''.join(listOfTokens)
					# 	for l in string.punctuation:
					# 		newString=newString.replace(l,'')
					# 	if len(newString)!=0:
					# 		newEachTwt.append(newString.lower())
					# print newEachTwt
				newEachTwt = clean(eachTwt)
				newEachTwt = newEachTwt.replace(',','').replace('_','').split(' ')
				newEachTwt = [a for a in newEachTwt if len(a)>0]

				# positive_old = 0
				# negative_old = 0
				# sentiPos_old=[]
				# sentiNeg_old=[]
				positive_new = 0
				negative_new = 0
				sentiPos_new=[]
				sentiNeg_new=[]

				for l in newEachTwt:
					stem = ste_handle.stem(l)
					# if l in pos_old or stem in pos_old:
					# 	positive_old += 1
					# 	sentiPos_old.append(l)
					# elif l in neg_old or stem in neg_old:
					# 	negative_old += 1
					# 	sentiNeg_old.append(l)
					if l in pos_new or stem in pos_new:
						positive_new += 1
						sentiPos_new.append(l)
					elif l in neg_new or stem in neg_new:
						negative_new += 1
						sentiNeg_new.append(l)
				# totalSenti_old=sentiPos_old+sentiNeg_old
				totalSenti_new=sentiPos_new+sentiNeg_new
				# #cat_twts.append((twts[i].rstrip(), unicode(positive), unicode(negative)))
				# cat_twts.append((' '.join(newEachTwt),'/'.join(totalSenti_new),str(positive_new), str(negative_new)))
				# 	#twts[i].rstrip(),' '.join(newEachTwt),'/'.join(totalSenti_new),str(positive_new), str(negative_new)))
				# 	#'/'.join(totalSenti_old),str(positive_old),str(negative_old),'/'.join(totalSenti_new),str(positive_new), str(negative_new)))
				row=(' '.join(newEachTwt),'/'.join(totalSenti_new),str(positive_new), str(negative_new))
				newfile.write(', '.join(row).encode('iso-8859-1')+'\n')
				print i
newfile.close()
	

# ########################## WRITING OUT TO NEW FILE ###########################
# with open('output/allFoodTweets_sentiment_0809.csv', 'w') as newfile:
# 	#newfile.write(', '.join(('text','label','cats','positive','negative\r\n')))
# 	newfile.write(', '.join(('text_cleaned','sentiment_words','positive','negative\r\n')))
# 		#'Old_sentiment_words','Old_positive','Old_negative','New_sentiment_words','New_positive','New_negative\r\n')))
# 	for row in cat_twts:
# 		newfile.write(', '.join(row).encode('iso-8859-1') + '\n')

# newfile.close()



	