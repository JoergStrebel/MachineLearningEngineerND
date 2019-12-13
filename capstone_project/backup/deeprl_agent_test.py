import sys
import pandas as pd
from agents.deeprlagent import DeepRL_Agent
from task import Task
import numpy as np
import csv
from datetime import datetime
import copy
from market import Market

import pandas as pd
from market import Market
from task import Task



# loading the stock prices
# all trade data is coming from XETRA

df_usinterest =  pd.read_csv('data/FRB_H15.csv', header=5, names=['day','US_rate'], skiprows=0, parse_dates=[0], \
                             infer_datetime_format=True)

df_sp500_prices = pd.read_csv('data/Investing_622391_historic_data.csv', header=0, \
                              names=['day','closing', 'opening', 'high', 'low', 'vol', 'change'], \
                              skiprows=0, parse_dates=[0], infer_datetime_format=True, decimal=',')

df_eurostoxx600_prices = pd.read_csv('data/Investing_DBX1A7_historic_data.csv', header=0, \
                                     names=['day','closing', 'opening', 'high', 'low', 'vol', 'change'], \
                                     skiprows=0, parse_dates=[0], infer_datetime_format=True, decimal=',')

df_msciworld_prices = pd.read_csv('data/Investing_ETF110_historic_data.csv', header=0, \
                                  names=['day','closing', 'opening', 'high', 'low', 'vol', 'change'], \
                                  skiprows=0, parse_dates=[0], infer_datetime_format=True, decimal=',')

# convert vol column to float dtype
#1. remove K, M, -
#2. replace , with .
#3. parse as float
#4. multiply by 1000, 1000000
def vol2float(x):
    if (x.find('-')!=-1):
        return float(0.0)

    if (x.find('K')!=-1):
        return float(x.replace('K','').replace(',','.'))*1000.00

    if (x.find('M')!=-1):
        return float(x.replace('M','').replace(',','.'))*1000000.00

    return float('nan')

df_sp500_prices['SP500_volno'] = df_sp500_prices['vol'].apply(vol2float)
df_eurostoxx600_prices['ESTOXX_volno'] = df_eurostoxx600_prices['vol'].apply(vol2float)
df_msciworld_prices['MSCI_volno'] = df_msciworld_prices['vol'].apply(vol2float)

# remove records without closing price
df_sp500_prices = df_sp500_prices.dropna(subset=['closing'])
df_eurostoxx600_prices = df_eurostoxx600_prices.dropna(subset=['closing'])
df_msciworld_prices = df_msciworld_prices.dropna(subset=['closing'])

# rename price and volumn columns
df_sp500_prices=df_sp500_prices.rename(columns={"closing": "SP500_price"})
df_eurostoxx600_prices = df_eurostoxx600_prices.rename(columns={"closing": "ESTOXX_price"})
df_msciworld_prices = df_msciworld_prices.rename(columns={"closing": "MSCI_price"})


# create calendar with all days
calendar_series = pd.Series(pd.date_range('2009-10-16', '2019-10-16', freq='D', name='date'))
calendarweekday = calendar_series.dt.dayofweek
calendarweekday.name='dayofweek'
calendarmonth = calendar_series.dt.month
calendarmonth.name='month'
calendarday = calendar_series.dt.day
calendarday.name='dayno'
calendarmonthstart = calendar_series.dt.is_month_start
calendarmonthstart.name='monthstart'

df_calendar=pd.concat([calendar_series,calendarweekday,calendarmonth, calendarday,calendarmonthstart], axis=1)

# join each dataframe with calendar and with interest rate
dfdata=pd.merge(df_calendar,df_sp500_prices,how='left',left_on='date', right_on='day')
dfdata=pd.merge(dfdata,df_eurostoxx600_prices,how='left',left_on='date', right_on='day')
dfdata=pd.merge(dfdata,df_msciworld_prices,how='left',left_on='date', right_on='day')
dfdata=pd.merge(dfdata,df_usinterest,how='left',left_on='date', right_on='day')

# remove surplus columns
dfdata = dfdata[['date','dayofweek','month','dayno','monthstart','SP500_price', 'SP500_volno', \
                 'ESTOXX_price', 'ESTOXX_volno', 'MSCI_price', 'MSCI_volno', 'US_rate']]

# remove records without closing price
dfdata = dfdata.dropna(subset=['SP500_price', 'SP500_volno', 'ESTOXX_price', 'ESTOXX_volno', 'MSCI_price', 'MSCI_volno' ])

print(dfdata.head())

# data structure: dataframe with the following columns
#['date','dayofweek','month','dayno','monthstart','SP500_price', 'SP500_volno', \
# 'ESTOXX_price', 'ESTOXX_volno', 'MSCI_price', 'MSCI_volno', 'US_rate']

# create test /validation data
dfdata_norecords = int(round(len(dfdata.index)*0.75))
dfdata_train = dfdata.iloc[0:dfdata_norecords,:]
dfdata_test = dfdata.iloc[dfdata_norecords:,:]

#create markets
market_train = Market(dfdata_train)
market_test = Market(dfdata_test)

#TODO: calculate number of months

# create tasks
task_train = Task(market_train, 1500.0, 120000.0, ['SP500', 'ESTOXX','MSCI'], 'SP500', -10.0, -100.0)
task_test = Task(market_test, 1500.0, 120000.0, ['SP500', 'ESTOXX','MSCI'], 'SP500', -10.0, -100.0)
dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%d-%b-%Y_%H%M%S")

num_episodes = 1000  # no training required
file_output = 'data_deeprl_'+timestampStr+'.csv'          # file name for saved results

done = False

labels = ['episode', 'time', 'action', 'portfolio', 'reward']
rewards = []  # to store the total reward per episode
maxreward = -10000
maxresults = {x : [] for x in labels}  # to store the transactions of the best episode
monthly_allocation = {'SP500': 1000.0} #monthly investment of 1000€ in SP500

agent = DeepRL_Agent(task_train, task_test)

# training runs
with open(file_output, 'w', newline='\n', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(labels)
    for i_episode in range(1, num_episodes+1):
        state = agent.reset_episode() # start a new episode, also resets task
        results = {x : [] for x in labels}  # to store the trajectory of the best episode
        #done = False

        while True:
            action = agent.act(state) # delivers an action for the current state
            next_state, reward, done = task_train.step(action) # push the simulation further

            agent.step(action, reward, next_state, done)

            # store the details of the current episode
            to_write = [i_episode]+[task_train.market.currentdate] + [str(action)] + [str(task_train.portfolio)] +[reward]
            writer.writerow(to_write)
            for ii in range(len(labels)):
                results[labels[ii]].append(to_write[ii])

            state = next_state

            if done:
                rewards.append((i_episode, reward, task_train.market.currentdate)) #keep track of the total reward
                if reward>=maxreward: #save the results of the best run so far
                    maxreward=max(reward,maxreward)
                    maxresults = copy.deepcopy(results) #save the best run
                break
    sys.stdout.flush()

# test runs
state = agent.reset_episode(True) # start a new episode in the test mode
while True:
    action = agent.act(state) # delivers an action for the current state
    next_state, reward, done = task_test.step(action) # push the simulation further
    agent.step(action, reward, next_state, done)
    state = next_state
    if done:
        print('Time: {0:5d}'.format(task_test.market.currentdate))
        print('Portfolio: ' + str(task_test.portfolio))
        print('Total reward: {0:2f}'.format(reward))
        break
    sys.stdout.flush()
