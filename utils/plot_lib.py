import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import re

PLOT_START_DATE='1/1/2015'
PLOT_END_DATE='2/27/2021'
plt.rcParams["figure.figsize"] = (14,8)
plt.rc('font', family='NANUMBARUNGOTHIC',size=15) 


def date_formatter(date_str):
    if re.match(r'(\d{2,4})[/-](\d{1,2})[/-](\d{1,2})', date_str):
        match= re.match(r'(\d{2,4})[/-](\d{1,2})[/-](\d{1,2})',date_str)
        word, year, month, day = match[0], match[1], match[2], match[3]

    elif re.match(r'(\d{1,2})\/(\d{1,2})\/(\d{2,4})', date_str):
        match= re.match(r'(\d{1,2})\/(\d{1,2})\/(\d{2,4})',date_str)
        word, month, day, year = match[0], match[1], match[2], match[3]

    elif re.match(r'(\d{2,4})[/-](\d{1,2})[/-](\d{1,2})', date_str):
        match= re.match(r'(\d{2,4})[/-](\d{1,2})[/-](\d{1,2})', date_str)
        word, year, month, day = match[0], match[1], match[2], match[3]
    date = datetime(int(year),int(month),int(day))
    return date

def single_plot(df, label='', start=PLOT_START_DATE, end=PLOT_END_DATE):
    start_date = date_formatter(start)
    end_date = date_formatter(end)
    label = label if label != '' else df.columns[0]
    
    df = df[(df.index>=start_date) & (df.index<=end_date)]
    fig, ax = plt.subplots(constrained_layout=True)
    #lns = ax.plot(df, color='blue', label=label)
    lns = sns.lineplot(ax=ax, data=df)
    #ax.legend(lns, labels, loc='best', fontsize=18)
    ax.set_xlabel(df.index.name)

def dual_yaxis_plot(df1, df2, label1='', label2='', start=PLOT_START_DATE, end=PLOT_END_DATE):
    start_date = date_formatter(start)
    end_date = date_formatter(end)
    
    label1 = label1 if label1 != '' else df1.columns[0]
    label2 = label2 if label2 != '' else df2.columns[0]
    
    df1 = df1[(df1.index>=start_date) & (df1.index<=end_date)]
    df2 = df2[(df2.index>=start_date) & (df2.index<=end_date)]

    fig1, ax1 = plt.subplots(constrained_layout=True)
    ax2 = ax1.twinx()
    
    lns1 = ax1.plot(df1, color='blue', label=label1)
    lns2 = ax2.plot(df2, color='green', label=label2)
    
    lns = lns1+lns2
    labels = [l.get_label() for l in lns]
    ax2.legend(lns, labels, loc='best', fontsize=18)
    ax1.set_xlabel(df1.index.name)


def compare_lineplot(df1, df2, label1='', label2='', start=PLOT_START_DATE, end=PLOT_END_DATE):
    start_date = datetime.strptime(start,'%m/%d/%Y')
    end_date = datetime.strptime(end,'%m/%d/%Y')
    
    label1 = label1 if label1 != '' else df1.columns[0]
    label2 = label2 if label2 != '' else df2.columns[0]
    
    df1 = df1[(df1.index>=start_date) & (df1.index<=end_date)]
    df2 = df2[(df2.index>=start_date) & (df2.index<=end_date)]

    fig1, ax1 = plt.subplots(constrained_layout=True)
    ax2 = ax1.twinx()
    
    lns1 = ax1.plot(df1, color='blue', label=label1)
    lns2 = ax2.plot(df2, color='green', label=label2)
    
    lns = lns1+lns2
    labels = [l.get_label() for l in lns]
    ax2.legend(lns, labels, loc='best', fontsize=18)
    
    ax1.set_xlabel(df1.index.name)
