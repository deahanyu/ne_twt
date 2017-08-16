
import pandas as pd
import os
import numpy as np
import re

def gettingPebbles(dt,ki,oldList):
	#dt:data, ki:keepindex[i]
	stepOne = re.findall(r'/METHOD=(.*)',dt[ki])[0]
	if 'STEPWISE' in stepOne:	
		oldList += [k for k in stepOne.split('STEPWISE')[1].split(' ') if len(k)>0 and k not in oldList]
	else:
		oldList += [k for k in stepOne.split('ENTER')[1].split(' ') if len(k)>0 and k not in oldList]
	return oldList


thisData =[x for x in os.listdir(os.getcwd()) if x[-3:]=='txt'][0]
with open(thisData,'r') as kk:
	thisData=kk.readlines()

keepIndex=[]

for i in range(len(thisData)):
	if re.findall(r'/METHOD=',thisData[i]):
		keepIndex.append(i)
	if re.findall(r'/SCATTERPLOT=',thisData[i]):
		keepIndex.append(i)


stone=[]
for i in range(0,len(keepIndex),2):
	if re.findall(r'/METHOD=',thisData[keepIndex[i]]) and re.findall(r'/SCATTERPLOT=',thisData[keepIndex[i+1]]):
		for j in range(keepIndex[i],keepIndex[i+1]):
			if j == keepIndex[i]:
				stone = gettingPebbles(thisData,j,stone)
			else:
				stone+=[b for b in thisData[j].split(' ') if len(b)>0 and b not in stone]
	else:
		if re.findall(r'/METHOD=',thisData[keepIndex[i]]) and re.findall(r'/METHOD=',thisData[keepIndex[i+1]]):
			stone = gettingPebbles(thisData,keepIndex[i],stone)
			if not re.findall(r'/SCATTERPLOT=',thisData[keepIndex[i+2]]):
				stone = gettingPebbles(thisData,keepIndex[i+1],stone)
		else:
			for k in range(keepIndex[i-1],keepIndex[i]):
				if k == keepIndex[i-1]:
					stone = gettingPebbles(thisData,k,stone)
				else:
					stone+=[b for b in thisData[k].split(' ') if len(b)>0 and b not in stone]
thisVar=[k.replace('.','').replace('\n','') for k in stone if len(k.replace('.','').replace('\n',''))>0]


tvData =[x for x in os.listdir(os.getcwd()) if x[-3:]=='csv'][0]
df_tv = pd.read_csv(tvData)

foodData = [x for x in os.listdir('../dataProcessing/output') if 'Food_v2.csv' in x][0]
df_food = pd.read_csv('../dataProcessing/output/'+foodData)

############################################################################
# #['Neighborhood_Affluence_Index_2Vars','Neighborhood_Disadvantage_Index_3Vars','Liquor_Density','Religious_Density','PCT_21_to_29']
# #['num_alcohol','alcohol_related_tweets','score_healthy','score_unhealthy','net_score']
# #Subsetting a data
# df_food = df_food[['GEOID10','countyname','YEAR','num_alcohol','alcohol_related_tweets','score_healthy','score_unhealthy','net_score']]
# #Groupby "GEOID10"
# df_food = df_food.groupby(['GEOID10','countyname']).sum().reset_index()
############################################################################

#Renaming variable names
df_tv.rename(columns={df_tv.columns[0]:'GEOID10'},inplace=True)
thisVar+=['GEOID10']
df_tv = df_tv[thisVar]


df = pd.merge(df_tv,df_food,on='GEOID10',how='outer')
df.replace(np.nan,'.',inplace=True)
df.replace(' ','.',inplace=True)

# df = df[['GEOID10','countyname','num_alcohol','alcohol_related_tweets','score_healthy','score_unhealthy','net_score','Neighborhood_Affluence_Index_2Vars','Neighborhood_Disadvantage_Index_3Vars','Liquor_Density','LOG10_Liquor_Density_2015','Religious_Density','LOG10_Religious_Density_2015','PCT_21_to_29','LOG10_PCT_21_to_29_09_13']]

df.to_csv('output/myData1.csv', index=False)







