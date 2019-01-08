import pandas as pd 
import numpy as np 

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
flights['CARRIER_DELAY'].fillna(0, inplace=True) #fill nan with 0 
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

#carrier delays 
car_del=flights.groupby('OP_UNIQUE_CARRIER')['CARRIER_DELAY'].mean() 
car_del=pd.DataFrame(car_del)
car_del.reset_index(level=0,inplace=True)
car_del_high=car_del.sort_values('CARRIER_DELAY',ascending=False)

#Miami flights 
mia=flights[flights.ORIGIN=="MIA"]
#count airport landings 
mia_dest=mia.groupby('DEST')['MONTH'].count() 
mia_dest=pd.DataFrame(mia_dest)
mia_dest.reset_index(level=0,inplace=True)
mia_dest['MONTH'].sum() 
mia_dest_high=mia_dest.sort_values('MONTH',ascending=False)

#percentage of arrival flights (on miami departures)
mia_dest['def_col']=6936 
mia_dest['percent']=mia_dest['MONTH']/mia_dest['def_col']

#cities and delays
flights['plus_minus_air']=flights['AIR_TIME']-(flights['AIR_TIME']+(flights['ARR_DELAY']+flights['DEP_DELAY'])) 
air_delays=flights.groupby(['ORIGIN','DEST'])['plus_minus_air'].mean() 
air_delays=pd.DataFrame(air_delays)
air_delays.reset_index(level=0,inplace=True)

#miami flights (best and worst cities to fly into from miami)
mia_flights=air_delays[air_delays.ORIGIN=="MIA"]
mia_flights.sort_values('plus_minus_air',ascending=False)
mia_dest.sort_values('percent',ascending=False) 