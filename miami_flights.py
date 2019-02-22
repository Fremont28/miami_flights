import pandas as pd 
import numpy as np 
from sklearn.ensemble import RandomForestClassifier
import sklearn 
from sklearn.model_selection import train_test_split

flights=pd.read_csv("flights18.csv") #oct 2018  

#airports with average longest routes 
dist=flights.groupby('ORIGIN')['DISTANCE'].mean() 
dist=pd.DataFrame(dist)
dist.reset_index(level=0,inplace=True)
long_dist=dist.sort_values('DISTANCE',ascending=False)
long_dist=long_dist[long_dist.DISTANCE<=1500]

#taxi out time by airport (departures)
taxi_out=flights.groupby('ORIGIN')['TAXI_OUT'].mean() 
taxi_out=pd.DataFrame(taxi_out)
taxi_out.reset_index(level=0,inplace=True)
long_taxi=taxi_out.sort_values('TAXI_OUT',ascending=False)

#carrier delays
flights['CARRIER_DELAY'].fillna(0, inplace=True) #fill na with 0 
flights['WEATHER_DELAY'].fillna(0,inplace=True)
flights['NAS_DELAY'].fillna(0,inplace=True) 
flights['SECURITY_DELAY'].fillna(0,inplace=True)
flights['LATE_AIRCRAFT_DELAY'].fillna(0,inplace=True)

#total delays 
flights['tol_delay']=flights['CARRIER_DELAY']+flights['WEATHER_DELAY']+flights['NAS_DELAY']+flights['SECURITY_DELAY']+flights['LATE_AIRCRAFT_DELAY']
flights['CARRIER_DELAY'].describe() #3.10 average 
flights['tol_delay'].mean() #9.83 

#delays by day 
del_day=flights.groupby('DAY_OF_WEEK')['tol_delay'].mean() #11.53 min on wednesday average delay 

#15 minute delays 
flights['15_del']=np.where(flights['tol_delay']>=15,1,0)

#airport code (categorical to numeric) 
#origin airport 
flights['origin_code'] = pd.Categorical(flights.ORIGIN_CITY_NAME)
flights.origin_code=flights.origin_code.cat.codes

#destination 
flights['dest_code'] = pd.Categorical(flights.DEST_CITY_NAME)
flights.dest_code=flights.dest_code.cat.codes

#carrier
flights['carrier_code'] = pd.Categorical(flights.OP_UNIQUE_CARRIER)
flights.carrier_code=flights.carrier_code.cat.codes

#one hot encode 
one_hot=pd.get_dummies(flights['origin_code'])
flights=flights.join(one_hot)
one_hot1=pd.get_dummies(flights['dest_code'])
flights1=pd.concat([flights,one_hot1],axis=1)
one_hot2=pd.get_dummies(flights['carrier_code'])
flights2=pd.concat([flights1,one_hot2],axis=1)

#train and test sets 
X=flights2["DAY_OF_WEEK"]
X1=flights2.iloc[:,45:740]
X2=pd.concat([X,X1],axis=1)
y=flights2.iloc[:,41]

#X and y 
X_train,X_test,y_train,y_test=train_test_split(X2,y,test_size=0.25,random_state=0)

X_train=X_train.iloc[1:50000]
X_test=X_test.iloc[50001:62501]
y_train=y_train.iloc[1:50000]
y_test=y_test.iloc[50001:62501]

#random forest model
rf=RandomForestClassifier(n_estimators=250,random_state=0)
rf.fit(X_train,y_train)

#predictions 
preds=rf.predict(X_test) #classification 
preds1=rf.predict_proba(X_test) #probability (0,1)

X_train=X2.iloc[1:100000]
X_test=X2.iloc[100001:125001]
y_train=y.iloc[1:100000]
y_test=y.iloc[100001:125001]

#model 1 
rf=RandomForestClassifier(n_estimators=250,random_state=0)
rf.fit(X_train,y_train)
preds2=rf.predict_proba(X_test) #(0,1)
f2=pd.DataFrame(preds2)
f2.columns=['prob_no_delay','prob_delay']

#combine with the original dataframe
f1=flights2[["ORIGIN_CITY_NAME","DEST_CITY_NAME","DAY_OF_WEEK","OP_UNIQUE_CARRIER","DISTANCE"]].iloc[100001:125001]
f1.reset_index(level=0,inplace=True)
f3=pd.concat([f1,f2],axis=1)

#highest average prob of 15 minute delay 
high_delays1=f3.groupby(['ORIGIN_CITY_NAME','DEST_CITY_NAME'])['prob_delay'].mean()
high_delays1=pd.DataFrame(high_delays1)
high_delays1.sort_values('prob_delay')
high_delays1.to_csv("high_delays.csv")

##delays by origin 
flights_delays=flights[flights['15_del']==1]
flightsX=flights_delays.groupby('ORIGIN_CITY_NAME')['15_del'].count() 
flightsX=pd.DataFrame(flightsX)
flightsX.reset_index(level=0,inplace=True)
flightsX1=flights.groupby('ORIGIN_CITY_NAME')['FLIGHTS'].count()
flightsX1=pd.DataFrame(flightsX1)
flightsX1.reset_index(level=0,inplace=True)
merge_delays=pd.merge(flightsX,flightsX1,on="ORIGIN_CITY_NAME")
merge_delays['percent_delays']=merge_delays['15_del']/merge_delays['FLIGHTS']
merge_delays.to_csv("delays_orlando.csv")

#percent of delays 
merge_delays1=merge_delays[merge_delays.FLIGHTS>1000]
merge_delays1['percent_delays'].mean() 
merge_delays1.sort_values('percent_delays',ascending=False)
merge_delays1.to_csv("orl_takeout.csv")


flights=pd.read_csv("flights18.csv") 
flights['ORIGIN_CITY_NAME'].head(4)

#california based flights (flying to los angeles)
cal=flights[flights.DEST_CITY_NAME=="Los Angeles, CA"]
cal_based=cal.groupby('ORIGIN_CITY_NAME').agg(np.sum)['FLIGHTS']
cal_based=pd.DataFrame(cal_based)
cal_based.reset_index(level=0,inplace=True)
cal_based.sort_values('FLIGHTS',ascending=False)

#overall origin to destination 
todos_based=flights.groupby(['ORIGIN_CITY_NAME','DEST_CITY_NAME']).agg(np.sum)['FLIGHTS']
todos_based=pd.DataFrame(todos_based)
todos_based.reset_index(level=0,inplace=True)
todos_based.sort_values('FLIGHTS',ascending=False)
