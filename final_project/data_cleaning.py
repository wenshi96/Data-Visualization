# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 13:47:10 2022

@author: mido
"""
import pandas as pd
import os
import time

#data=pd.read_csv(os.path.join(os.getcwd(),"crimes_data.csv"))
#data=data[data['Community Area']==41]
#data.to_csv(os.path.join(os.getcwd(),"data_hp.csv"))

data=pd.read_csv(os.path.join(os.getcwd(),"data_hp.csv"))

data=data[data['Date'].apply(lambda x: time.strptime(x,"%m/%d/%Y %I:%M:%S %p"))>time.strptime("01 Jan 17", "%d %b %y")]

data=data[['ID','Date','Block','Primary Type','Description','Location Description', 'Arrest','Year', 'Latitude', 'Longitude']]

data=data.dropna(subset=['Latitude', 'Longitude'])
data.to_csv(os.path.join(os.getcwd(),"data.csv"))

data_new=pd.read_csv(os.path.join(os.getcwd(),"data.csv"))
data_new['dt']=data_new['Date'].apply(lambda x: time.strptime(x,"%m/%d/%Y %I:%M:%S %p"))
data_new['dt']=data_new['dt'].apply(lambda x: time.strftime("%Y-%m-%d %X",x))
data_new['Month']=data_new['dt'].apply(lambda x:pd.to_datetime(x).month)
data_new['Hour']=data_new['dt'].apply(lambda x:pd.to_datetime(x).hour)
data_new['dt']=data_new['dt'].apply(lambda x:pd.to_datetime(x))

def is_night(hour):
    if hour>16 or hour<5:
        return 'Yes'
    else:
        return 'No'
    
def season(month):
    if month<6 and month>2:
        return 'Spring'
    if month<9 and month>5:
        return 'Summer'
    if month<12 and month>8:
        return 'Autumn'
    else:
        return 'Winter'
    
data_new['Night']=data_new['Hour'].apply(lambda x: is_night(x))
data_new=data_new.drop(columns=['Unnamed: 0'])
data_new=data_new.rename(columns={'Primary Type':'Primary_Type','Location Description':'Location_Description'})
data_new['Season']=data_new['Month'].apply(lambda x:season(x))
data_new.to_csv(os.path.join(os.getcwd(),"data_clean.csv"))

data_sum=data_new.groupby(['Primary_Type','Year']).size().to_frame().reset_index()
data_sum=data_sum.rename(columns={0:'Count'})
data_sum.to_csv(os.path.join(os.getcwd(),"data_sum.csv"),index=False)


data_latlon=pd.read_csv(os.path.join(os.getcwd(),"data_clean.csv"))
data_latlon=data_latlon[['Latitude','Longitude']]
data_latlon=data_latlon.rename(columns=data_latlon.iloc[0]).drop(data_latlon.index[0])
data_latlon=data_latlon.reset_index(drop=True)
data_latlon.to_csv(os.path.join(os.getcwd(),"data_latlon.csv"),index=False)

