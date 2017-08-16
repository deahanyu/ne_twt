import os
import pandas as pd
import re
import numpy as np 

def creatingBinaryColumn(ddff,first,second,new):
	if second == 0:
		ddff[new]=ddff[first]
	else:
		ddff[new]=ddff[first]+ddff[second]
	ddff.loc[ddff[new] != 0, new] = 1
	return 1

def normalizing(ddff,listOfNumerator,denominator,listOfNewCol):
	for i in range(len(listOfNumerator)):
		ddff[listOfNewCol[i]] = ddff[listOfNumerator[i]]/ddff[denominator].astype(float)
		ddff[listOfNewCol[i]].replace(np.nan,0,inplace=True)
	return 1 

def creatingColumns(ddff,listOfNewCol,thisValue=0):
	for i in range(len(listOfNewCol)):
		ddff[listOfNewCol[i]] = thisValue
	return 1

thisData =[x for x in os.listdir(os.getcwd()) if x[-3:]=='csv'][0]
df = pd.read_csv(thisData)
df.food_related = df.food_related.astype(str)

#----------Subsetting a data frame with "food_related" == "1"
df = df.loc[df.food_related=='1',]
del df['food_related']

#----------Creating "YEAR" column from "create" column
df['YEAR']=[int(re.findall(r'20[0-9]{2}',i)[0]) for i in list(df.created)]
del df['created']

#----------Subsetting a data frame after 2013
df = df.loc[df.YEAR>=2014,]

#----------Creating "GEOID10" column from "state", "county", and "tract"
df.state = df.state.astype(str)
df.ix[df.county < 100, 'county'] = '0'+df.ix[df.county < 100, 'county'].astype(str)
df.county = df.county.astype(str)
df.tract = ['0'*(6-len(str(x)))+str(x) for x in list(df.tract)]
df['GEOID10'] = df[['state', 'county','tract']].apply(lambda x:''.join(x),axis=1)
df.drop(['state','county','tract'],axis=1,inplace=True)

#----------Renaming variable names
df.rename(columns={'word_count':'num_words','score_sum':'net_score','num_alcohol':'num_alcohol_words'},inplace=True)

#----------Creating more variables
creatingBinaryColumn(df,'num_alcohol_words',0,'alcohol_related_tweets')
creatingBinaryColumn(df,'num_healthy1','num_healthy2','healthy_related_tweets')
creatingBinaryColumn(df,'num_unhealthy1','num_unhealthy2','unhealthy_related_tweets')
creatingBinaryColumn(df,'healthy_related_tweets','unhealthy_related_tweets','food_related_tweets')
df['net_healthy_unhealthy_related_tweets'] = df.healthy_related_tweets - df.unhealthy_related_tweets

#----------Creating a new variable : "num_tweets"
creatingColumns(df,['num_tweets'],thisValue=1)

#----------Creating two different dataframes 
df_by_censustract = df.drop('screenname',axis=1,inplace=False)
df_by_user = df

#----------Group by "GEOID10" and "screenname"
#----------If we want separate YEAR too, then add YEAR
df_by_censustract = df_by_censustract.groupby(['GEOID10','countyname']).sum().reset_index()
df_by_user = df_by_user.groupby(['GEOID10','screenname']).sum().reset_index()
df_by_censustract.drop('YEAR',axis=1,inplace=True)
df_by_user.drop('YEAR',axis=1,inplace=True)

#----------Creating a new variable : "num_unique_users"
creatingColumns(df_by_censustract,['num_unique_users'])

#---------df_by_censustract - Normalization A - Num_food_words 
this = ['score_healthy','score_unhealthy','net_score']
that = ['NormA_tract_score_healthy','NormA_tract_score_unhealthy','NormA_tract_net_score']
normalizing(df_by_censustract,this,'num_food_words',that)
#---------df_by_censustract - Normalization B - Food_related_tweets & Alcohol_related_tweets
that = ['NormB_tract_score_healthy','NormB_tract_score_unhealthy','NormB_tract_net_score']
normalizing(df_by_censustract,this,'food_related_tweets',that)
normalizing(df_by_censustract,['num_alcohol_words'],'num_tweets',['NormB_tract_num_alcohol_words'])

#---------df_by_user - Normalization A
that = ['NormA_user_score_healthy','NormA_user_score_unhealthy','NormA_user_net_score']
normalizing(df_by_user,this,'num_food_words',that)
#---------df_by_user - Normalization B 
that = ['NormB_user_score_healthy','NormB_user_score_unhealthy','NormB_user_net_score']
normalizing(df_by_user,this,'food_related_tweets',that)
normalizing(df_by_user,['num_alcohol_words'],'num_tweets',['NormB_user_num_alcohol_words'])

#----------Creating columns
this = ['NormA_user_score_healthy','NormA_user_score_unhealthy','NormA_user_net_score','NormB_user_score_healthy','NormB_user_score_unhealthy','NormB_user_net_score','NormB_user_num_alcohol_words']
creatingColumns(df_by_censustract,this)

#---------Calculating user-count average of normalization
for i in df_by_censustract.GEOID10:
	for j in this:
		df_by_censustract.ix[df_by_censustract.GEOID10==i,j] = df_by_user.loc[df_by_user.GEOID10==i,j].mean()
	df_by_censustract.ix[df_by_censustract.GEOID10==i,'num_unique_users'] = len(df_by_user.loc[df_by_user.GEOID10==i,].index)

#---------Writing the final table
thisOrder = ['GEOID10','countyname','num_healthy1','num_healthy2','num_unhealthy1','num_unhealthy2','score_healthy','score_unhealthy','net_score','num_tweets','num_unique_users','num_words','num_food_words','num_alcohol_words','food_related_tweets','alcohol_related_tweets','healthy_related_tweets','unhealthy_related_tweets','net_healthy_unhealthy_related_tweets','NormA_tract_score_healthy','NormA_user_score_healthy','NormA_tract_score_unhealthy','NormA_user_score_unhealthy','NormA_tract_net_score','NormA_user_net_score','NormB_tract_score_healthy','NormB_user_score_healthy','NormB_tract_score_unhealthy','NormB_user_score_unhealthy','NormB_tract_net_score','NormB_user_net_score','NormB_tract_num_alcohol_words','NormB_user_num_alcohol_words']
df_by_censustract = df_by_censustract[thisOrder]
df_by_censustract.to_csv('output/NE_Twitter_Food_v2.csv', index=False)




