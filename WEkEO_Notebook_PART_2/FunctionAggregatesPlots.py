
import xarray as xr
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from dateutil.parser import parse 
import matplotlib as mpl
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
from cycler import cycler
rcParams['figure.figsize'] = 18, 10
rcParams['lines.linewidth'] = 3
import csv
import netCDF4
from scipy import stats


import FunctionAggregatesPlots as fa 


def faGenerate1DTendency(t,NcFile1Doutput):    
    
    """ read file 1D fix dimension NetCDF file for the overall SST tendency 
    """

    lon_name = 'lon'
    lat_name = 'lat'
    
    fy_1D= t.mean(dim=(lat_name, lon_name), skipna=True)    
    fy_dt = fy_1D.groupby('time.year').mean()
    df = fy_dt.to_dataframe().reset_index().set_index('year')
    
    x=df.index
    y=df.thetao
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    k=intercept + slope*x
    fig, axes = plt.subplots(1, figsize=(18,8), dpi= 100)

    plt.plot(df.thetao, color='teal', marker='o', markerfacecolor='firebrick', markeredgecolor='g', markersize=8)
    plt.plot(x, k, 'k')
    plt.grid()
    plt.title('Sea Surface Temperature Annual Trend in the Adriatic Sea', size=20)
    plt.ylabel('Temperature (C)',fontsize=15)
    plt.xlabel('TS',fontsize=15)
    plt.xticks(size = 15)
    plt.yticks(size = 15)
    plt.savefig('image_outputs/annualTrend.png')


def faGenerateDailyTimeSeries(temp_ts):
    
    """ Daily TS SST Analysis 
    """    
    
    file2 = pd.read_csv(temp_ts,index_col='DATE', parse_dates=['DATE'])
    fig, axes = plt.subplots(1, figsize=(18,8), dpi= 100)

    plt.title('Sea Surface Temperature Time Series, Daily Trend in the Adriatic Sea', size=20)
    plt.grid()
    plt.plot(file2, color='teal')
    plt.xticks(size = 20)
    plt.yticks(size = 20)
    plt.savefig('image_outputs/tsTrend.png')

        
def faGenerateDailyTimeSeriesSTD(temp_ts):
    
    """ Daily TS STD Analysis 
    """ 
    
    file2 = pd.read_csv(temp_ts,index_col='DATE', parse_dates=True)
    fy_dt = file2.groupby(pd.Grouper(freq='M')).mean()
    
    
    daily_sdT = fy_dt.rolling(window = 12).std()
    fig, axes = plt.subplots(1, figsize=(18,8), dpi= 100)

    plt.title('Sea Surface Temperature Standard Deviation in the Adriatic Sea', size=20)
    plt.grid()
    plt.plot(daily_sdT, color='teal')
    plt.xticks(size = 20)
    plt.yticks(size = 20)
    plt.savefig('image_outputs/std_sst.png')
    return daily_sdT
    
def faGenerateDailyTimeSeriesPLOT(temp_ts):   

    """ Monthly Mean TS Violin Plot 
    """ 
        
    file2 = pd.read_csv(temp_ts, parse_dates=['DATE'])
    file2['Time Series from 1987 to 2019'] = [d.year for d in file2.DATE]
    file2['Month'] = [d.strftime('%b') for d in file2.DATE]
    years = file2['Time Series from 1987 to 2019'].unique()
    plt.style.use('seaborn')

    fig, axes = plt.subplots(1, figsize=(18,8), dpi= 100)
    sns.violinplot(x='Month', y='TEMPERATURE', data=file2.loc[~file2.Month.isin([1987, 2019]), :], palette="tab10", bw=.2, cut=1, linewidth=1)

    axes.set_title('Monthly Mean Sea Surface Temperature in the Adriatic Sea from 1987 to 2019', fontsize=20); 
    plt.xticks(size = 20)
    plt.yticks(size = 20)
    plt.xlabel('Months',fontsize=18)
    plt.ylabel('Sea Surface Temperature (C)',fontsize=18)
    plt.savefig('image_outputs/MonthlyMean.png')
