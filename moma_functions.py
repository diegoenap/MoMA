import pandas as pd
import numpy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

# Read datasets functions

def read_visitors_data(filename):
    """Read venue visitors dataset"""
    data = pd.read_csv(filename, parse_dates=['Date'], index_col='Date', dayfirst=True)
    return data.asfreq('D', fill_value=0)
    # data = pandas.read_csv(filename)
    # # Create date object column and sort the dataframe by date
    # data['date2'] = [dt.datetime.strptime(d, '%d/%m/%y') for d in data['Date'].astype('str')]
    # return data.sort_values(by='date2', ascending=True).reset_index(drop=True)


# def complete_dates(data, channels):
#     """Complete the missing dates with null values"""
#     # Sort the dataframe by date to get the initial and final date and the difference in days
#     data.sort_values(by='date2', ascending=True, inplace=True)
#     d1 = data.loc[0, 'date2']
#     d2 = data.loc[data.shape[0] - 1, 'date2']
#     # diff is the number of dates between the start and the end dates of the dataset. If diff is greater than the
#     # number of rows it means that there are missing dates
#     diff = d2 - d1
#     if not channels:
#         if data.shape[0] != diff.days + 1:
#             print('Some dates are missing!')
#             # Create a complete sequence of dates
#             step = dt.timedelta(days=1)
#             dateseq = []
#             while d1 <= d2:
#                 dateseq.append(d1)
#                 d1 += step
#             # Check for missing dates and create a temporal dataframe (tmpdf) with the missing rows, filled with 0's.
#             # Then, append tmpdf to the original dataset
#             i = 0
#             j = 0
#             tmpdf = pd.DataFrame()
#             col_list = ['date', 'users', 'usersNew', 'percentNewSessions', 'sessions', 'bounceRate', 'avgSessionDuration',
#                         'pageviews', 'pageviewsPerSession', 'uniquePageviews', 'avgTimeOnPage', 'usersOld', 'sessionsNew',
#                         'sessionsOld', 'sessionsBounce', 'sessionsNoBounce', 'date2']
#             while j < len(dateseq):
#                 if data.loc[i, 'date2'] == dateseq[j]:
#                     i += 1
#                     j += 1
#                 else:
#                     # Add missing row
#                     missrow = pd.DataFrame([[int(dateseq[j].strftime('%Y%m%d')), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, dateseq[j]]],
#                                                columns=col_list)
#                     tmpdf = tmpdf.append(missrow, ignore_index=True)
#                     j += 1
#             # Append the nissing rows to the original dataset and sort again
#             data = data.append(tmpdf, ignore_index=True)
#             return data.sort_values(by='date2', ascending=True).reset_index(drop=True)
#         else:
#             print('Complete dates')
#             return data.reset_index(drop=True)
#     else:
#         print('Dataset with Channel info')
#         print(data.shape)
#         print(diff.days + 1)
#         data.sort_values(by=['date2', 'channel'], inplace=True)
#         channel_names = ['(Other)', 'Direct', 'Display', 'Email', 'Organic Search', 'Paid Search', 'Referral', 'Social']
#         if data.shape[0] != (diff.days + 1) * len(channel_names):
#             print('Some dates are missing!')
#             # Create a complete sequence of dates
#             step = dt.timedelta(days=1)
#             dateseq = []
#             while d1 <= d2:
#                 dateseq.append(d1)
#                 d1 += step
#             # Check for missing dates and create a temporal dataframe (tmpdf) with the missing rows, filled with 0's.
#             # Then, append tmpdf to the original dataset
#             i = 0
#             j = 0
#             tmpdf = pd.DataFrame()
#             col_list = ['date', 'channel', 'users', 'usersNew', 'percentNewSessions', 'sessions', 'bounceRate',
#                         'avgSessionDuration',
#                         'pageviews', 'pageviewsPerSession', 'uniquePageviews', 'avgTimeOnPage', 'usersOld',
#                         'sessionsNew',
#                         'sessionsOld', 'sessionsBounce', 'sessionsNoBounce', 'date2']
#             while j < len(dateseq):
#                 k = 0
#                 #print('Checking channels...')
#                 while k < len(channel_names):
#                     if i < data.shape[0] and data.loc[i, 'date2'] == dateseq[j] and data.loc[i, 'channel'] == channel_names[k]:
#                         #print('Channel FOUND: {} i: {} k: {}'.format(channel_names[k], i, k))
#                         i += 1
#                         k += 1
#                     else:
#                         # Add missing row
#                         #print('Channel missing: {} i: {} k: {}'.format(channel_names[k], i, k))
#                         missrow = pd.DataFrame(
#                             [[int(dateseq[j].strftime('%Y%m%d')), channel_names[k], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                               0, 0, 0, 0, 0, dateseq[j]]],
#                             columns=col_list)
#                         tmpdf = tmpdf.append(missrow, ignore_index=True)
#                         k += 1
#                 #print('Increase j')
#                 j += 1
#             # Append the nissing rows to the original dataset and sort again
#             data = data.append(tmpdf, ignore_index=True)
#             return data.sort_values(by=['date2', 'channel'], ascending=True).reset_index(drop=True)
#         else:
#             print('Complete dates')
#             return data.reset_index(drop=True)


def read_ga_data(filename):
    """Read Google Analytics datasets."""
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
        # Create dataframes for each channel, complete separatetly and then append in one final dataset
        channels = ['(Other)', 'Direct', 'Display', 'Email', 'Organic Search', 'Paid Search', 'Referral', 'Social']
        tmp = pd.DataFrame(columns=data.columns)
        mindate = min(data.index)
        maxdate = max(data.index)
        for ch in channels:
            # Complete missing dates with 0s
            tmp1 = data[data.channel == ch].asfreq('D', fill_value=0)
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
            tmp = pd.concat([tmp, tmp1])
        data = tmp
    else:
        #
        data = data.asfreq('D', fill_value=0)

    # print('Reading dataset...')
    # data = pandas.read_csv(filename, encoding='utf_16_le', sep='\t')
    # # Define better column names
    # data.rename(columns={'ga:date': 'date',
    #                      'ga:users': 'users',
    #                      'ga:newUsers': 'usersNew',
    #                      'ga:percentNewSessions': 'percentNewSessions',
    #                      'ga:sessions': 'sessions',
    #                      'ga:bounceRate': 'bounceRate',
    #                      'ga:avgSessionDuration': 'avgSessionDuration',
    #                      'ga:pageviews': 'pageviews',
    #                      'ga:pageviewsPerSession': 'pageviewsPerSession',
    #                      'ga:uniquePageviews': 'uniquePageviews',
    #                      'ga:avgTimeOnPage': 'avgTimeOnPage'}, inplace=True)
    # if channels:
    #     data.rename(columns={'ga:channelGrouping': 'channel'}, inplace=True)
    # # Correct percentage
    # data['percentNewSessions'] = data['percentNewSessions'] / 100
    # data['bounceRate'] = data['bounceRate'] / 100
    # # Derive new columns
    # data['usersOld'] = data['users'] - data['usersNew']
    # data['sessionsNew'] = data['sessions'] * data['percentNewSessions']
    # data['sessionsOld'] = data['sessions'] * (1 - data['percentNewSessions'])
    # data['sessionsBounce'] = data['sessions'] * data['bounceRate']
    # data['sessionsNoBounce'] = data['sessions'] * (1 - data['bounceRate'])
    # # Create date object column and sort the dataframe by date
    # data['date2'] = [dt.datetime.strptime(d, '%Y%m%d') for d in data['date'].astype('str')]
    # # Check and complete range of days if necessary.
    # data = complete_dates(data, channels)
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

def get_correlation_matrix(vsdf, gadf):
    """Returns a matrix where row are the GA metrics and the column are the correlation value at each lag point
    (from 0 to maxlag). It keeps the Visitors dataset fixed and try different lags going backwards with the GA metrics,
    that is why GA metrics dataset should be larger. The diference in day between both datasets is considered as the
    lag."""
    a = vsdf['2017-01'].visitors
    b = gadf['2017-01'].users
    print(a.shape)
    print(b.shape)
    print(a.corr(b, method='pearson'))
    #c = numpy.corrcoef(vsdf.visitors, gadf.loc[:, 'Users'])
    #return c


