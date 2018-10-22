import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math
# import datetime as dt

metric_list = ['users', 'usersNew', 'usersOld', 'sessions', 'sessionsNew', 'sessionsOld', 'sessionsBounce',
               'sessionsNoBounce', 'avgSessionDuration', 'pageviews', 'pageviewsPerSession', 'uniquePageviews',
               'avgTimeOnPage']

channels = ['(Other)', 'Direct', 'Display', 'Email', 'Organic Search', 'Paid Search', 'Referral', 'Social']

# Read datasets functions

def read_visitors_data(filename):
    """Read venue visitors dataset"""
    print("Reading", filename)
    data = pd.read_csv(filename, parse_dates=['Date'], index_col='Date', dayfirst=True)
    return data.asfreq('D', fill_value=0)


def read_ga_data(filename):
    """Read Google Analytics datasets."""
    print("Reading", filename)
    data = pd.read_csv(filename, encoding='utf_16_le', sep='\t', parse_dates=['ga:date'], index_col='ga:date', dayfirst=True)
    # Rename column names
    data.rename(columns={'ga:users': 'users',
                         'ga:newUsers': 'usersNew',
                         'ga:percentNewSessions': 'percentNewSessions',
                         'ga:sessions': 'sessions',
                         'ga:bounceRate': 'bounceRate',
                         'ga:avgSessionDuration': 'avgSessionDuration',
                         'ga:pageviews': 'pageviews',
                         'ga:pageviewsPerSession': 'pageviewsPerSession',
                         'ga:uniquePageviews': 'uniquePageviews',
                         'ga:avgTimeOnPage': 'avgTimeOnPage'}, inplace=True)
    # Correct percentage
    data['percentNewSessions'] = data['percentNewSessions'] / 100
    data['bounceRate'] = data['bounceRate'] / 100
    # Derive new columns
    data['usersOld'] = data['users'] - data['usersNew']
    data['sessionsNew'] = data['sessions'] * data['percentNewSessions']
    data['sessionsOld'] = data['sessions'] * (1 - data['percentNewSessions'])
    data['sessionsBounce'] = data['sessions'] * data['bounceRate']
    data['sessionsNoBounce'] = data['sessions'] * (1 - data['bounceRate'])
    # Sort by date
    data.sort_index(inplace=True)
    # Complete the dataset
    if 'ga:channelGrouping' in data.columns:
        # For datasets with channel info
        # Rename column
        data.rename(columns={'ga:channelGrouping': 'channel'}, inplace=True)
        # Create dataframes for each channel, complete separatetly and then concatenate in one final dataset
        tmp = pd.DataFrame(columns=data.columns)
        mindate = min(data.index)
        maxdate = max(data.index)
        for ch in channels:
            # Complete missing dates with 0s
            tmp1 = data[data.channel == ch].asfreq('D', fill_value=0)
            if tmp1.empty:
                tmp1 = pd.DataFrame(index=pd.date_range(start=mindate, end=maxdate, freq='D'), columns=data.columns)
                tmp1.fillna(0, inplace=True)
            # If the temporal dataset has a start date bigger than the minimum, complete the dates
            if tmp1.index[0] > mindate:
                # Channel have missing dates at the beginning
                tmpfill = pd.DataFrame(index=pd.date_range(start=mindate, end=(tmp1.index[0]-1), freq='D'), columns=data.columns)
                tmpfill.fillna(0, inplace=True)
                tmp1 = pd.concat([tmpfill, tmp1])
                tmp1 = tmp1.asfreq('D')
            # If the temporal dataset has an end date smaller than the maximum, complete the dates
            if tmp1.index[-1] < maxdate:
                # Channel have missing dates at the end
                tmpfill = pd.DataFrame(index=pd.date_range(start=(tmp1.index[-1]+1), end=maxdate, freq='D'), columns=data.columns)
                tmpfill.fillna(0, inplace=True)
                tmp1 = pd.concat([tmp1, tmpfill])
                tmp1 = tmp1.asfreq('D')
            # Fill the channel column with the channel name
            tmp1.channel = ch
            # Concatenate to final dataframe
            tmp = pd.concat([tmp, tmp1])
        # Change the data type for the metrics to numbers
        tmp[metric_list] = tmp[metric_list].apply(pd.to_numeric)
        data = tmp
    else:
        #
        data = data.asfreq('D', fill_value=0)
    return data


# Plot datasets functions

def plot_visitors(dataset):
    plt.figure(figsize=(10, 4))
    plt.plot_date(x=[mdates.strpdate2num('%d/%m/%y')(d) for d in dataset['Date']], y=dataset['visitors'], fmt='r-')
    plt.title('MoMA visitors')
    plt.ylabel('Visitors')
    plt.grid(True)
    plt.show()


def plot_gametrics(dataset, metricname):
    plt.figure(figsize=(10, 4))
    plt.plot_date(x=[mdates.strpdate2num('%Y%m%d')(d) for d in dataset['date'].astype('str')],
                  y=dataset[metricname],
                  fmt='b-')
    plt.title('MoMA GA metric')
    plt.ylabel(metricname)
    plt.grid(True)
    plt.show()


# Correlation test functions

def get_correlations_matrix(vsdf, gadf, maxlag):
    """
    Returns a matrix where the rows are the GA metrics and the column are the correlation value at each lag point
    (from 0 to maxlag). It keeps the Visitors dataset fixed and try different lags going backwards with the GA metrics,
    that is why GA metrics dataset should be larger (it starts before). The difference in days between both datasets is
    considered as the lag.
    """
    # For each metric in GA metrics
    corr_dict = dict()
    for metric in metric_list:
        gametric = gadf[metric]
        corr_list = []
        # For each lag
        for lag in range(0, maxlag+1):
            # Set range dates based on lag, lag 0 means GA metrics have the same dates as Visitors
            inilag = maxlag - lag
            endlag = -(lag)
            if endlag:
                corr_list.append(vsdf.visitors.corr(gametric[lag:endlag], method='pearson'))
            else:
                corr_list.append(vsdf.visitors.corr(gametric[lag:], method='pearson'))
        # print(len(corr_list))
        corr_dict[metric] = corr_list
        # break
    return corr_dict


def get_max_correlations(corrs_matrix, colnames=None):
    """
    Takes a correlation matrix and returns a table with the maximum correlation value for each GA metric along with the
    the corresponding lag
    :param corrs_matrix: Dictionary where the indexes are the metrics pointing to lists of correlations
    :param colnames: List of labels to replace the default column names
    :return:
    """
    # corr_dict = dict()
    # for metric in metric_list:
    #     max_corr = max(corrs_matrix[metric])
    #     # print("Metric: {}\n  Max corr: {}\n  Lag: {}".format(metric, max_corr, corrs_matrix[metric].index(max_corr)))
    #     corr_dict[metric] = [max_corr, corrs_matrix[metric].index(max_corr)]
    # return corr_dict
    tmp = pd.DataFrame(columns=['metric', 'corr', 'lag'])
    for metric in metric_list:
        max_corr = max(corrs_matrix[metric])
        tmp = tmp.append(pd.DataFrame({'metric': [metric], 'corr': [max_corr], 'lag': [corrs_matrix[metric].index(max_corr)]}))
    if colnames:
        tmp.columns = colnames
    return tmp.reset_index(drop=True)


def moving_average(df, window = 7):
    """
    Calculates the moving average given the window. In case of GA metrics, it assumes that the dataset is already
    filtered by Channel.
    :param df: Visitors or GA metrics (already filtered by Channel)
    :param window: Number of dates to calculate the moving avergae
    :return: A dataframe with the moving average values
    """
    if 'channel' in df.columns:
        return df.drop(columns=['channel']).rolling(window).mean().dropna()
    else:
        return df.rolling(window).mean().dropna()


def log_values(df):
    if 'channel' in df.columns:
        tmp = pd.DataFrame(columns=df.columns, index=df.index)
        tmp.channel = df.channel
        for metric in metric_list:
            tmp.loc[:, metric] = np.log(df.loc[:, metric])
            # print(df[metric])
        return tmp.replace(to_replace=-math.inf, value=0)
    else:
        return df.apply(np.log, axis=1).replace(to_replace=-math.inf, value=0)
    # return df.apply(lambda x: np.log(x) if x.isdigit() else x)


def can_apply_log(df):
    if 'visitors' in df.columns:
        return len(df[df.visitors == 0]) == 0
    else:
        for metric in metric_list:
            len(df[df.loc[metric] == 0]) == 0


def run_correlation_tests(vsdf, gadf, maxlag, dataname):
    """
    Runs the get_correlation methods to different transformations of the original datasets.
    :param vsdf: Visitors dataset
    :param gadf: GA metrics dataset
    :param maxlag:
    :return:
    """
    # tmp = pd.DataFrame(columns=['metric', 'corr', 'lag', 'dataname'])
    # 1) Unchanged Visitors & Unchanged GA
    max_corrs = get_max_correlations(get_correlations_matrix(vsdf, gadf, maxlag),
                                     colnames=['metric1', 'corr1', 'lag1'])
    # max_corrs['dataname'] = dataname
    # tmp = tmp.append(max_corrs)
    # 2) Unchanged Visitors & Log GA
    tmp = get_max_correlations(get_correlations_matrix(vsdf, log_values(gadf), maxlag),
                               colnames=['metric2', 'corr2', 'lag2'])
    max_corrs = pd.concat([max_corrs, tmp], axis=1)

    # 3) Unchanged Visitors & Moving average GA
    tmp = get_max_correlations(get_correlations_matrix(vsdf, moving_average(gadf), maxlag),
                               colnames=['metric3', 'corr3', 'lag3'])
    max_corrs = pd.concat([max_corrs, tmp], axis=1)

    # 4) Unchanged Visitors & Moving average Log GA
    tmp = get_max_correlations(get_correlations_matrix(vsdf, moving_average(log_values(gadf)), maxlag),
                               colnames=['metric4', 'corr4', 'lag4'])
    max_corrs = pd.concat([max_corrs, tmp], axis=1)

    # 5) Moving average Visitors & Moving average GA
    tmp = get_max_correlations(get_correlations_matrix(moving_average(vsdf), moving_average(gadf), maxlag),
                               colnames=['metric5', 'corr5', 'lag5'])
    max_corrs = pd.concat([max_corrs, tmp], axis=1)

    # 6) Moving average Visitors & Moving average Log GA
    tmp = get_max_correlations(get_correlations_matrix(moving_average(vsdf), moving_average(log_values(gadf)), maxlag),
                               colnames=['metric6', 'corr6', 'lag6'])
    max_corrs = pd.concat([max_corrs, tmp], axis=1)

    # Add dataname column
    max_corrs['dataname'] = dataname
    return max_corrs.drop(columns=['metric2', 'metric3', 'metric4', 'metric5', 'metric6'])