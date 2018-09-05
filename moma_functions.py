import pandas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

# Read datasets functions


def complete_dates(data, channels):
    """Complete the missing dates with null values"""
    # Sort the dataframe by date to get the initial and final date and the difference in days
    data.sort_values(by='date2', ascending=True, inplace=True)
    d1 = data.loc[0, 'date2']
    d2 = data.loc[data.shape[0] - 1, 'date2']
    diff = d2 - d1
    if ~channels:
        if data.shape[0] != diff.days + 1:
            print('Some dates are missing!')
            # Create a complete sequence of dates
            step = dt.timedelta(days=1)
            dateseq = []
            while d1 <= d2:
                dateseq.append(d1)
                d1 += step
            # Check for missing dates and create a temporal dataframe (tmpdf) with the missing rows, filled with 0's.
            # Then, append tmpdf to the original dataset
            i = 0
            j = 0
            tmpdf = pandas.DataFrame()
            col_list = ['date', 'users', 'usersNew', 'percentNewSessions', 'sessions', 'bounceRate', 'avgSessionDuration',
                        'pageviews', 'pageviewsPerSession', 'uniquePageviews', 'avgTimeOnPage', 'usersOld', 'sessionsNew',
                        'sessionsOld', 'sessionsBounce', 'sessionsNoBounce', 'date2']
            while j < len(dateseq):
                if data.loc[i, 'date2'] == dateseq[j]:
                    i += 1
                    j += 1
                else:
                    # Add missing row
                    missrow = pandas.DataFrame([[int(dateseq[j].strftime('%Y%m%d')), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, dateseq[j]]],
                                               columns=col_list)
                    tmpdf = tmpdf.append(missrow, ignore_index=True)
                    j += 1
            # Append the nissing rows to the original dataset and sort again
            data = data.append(tmpdf, ignore_index=True)
            return data.sort_values(by='date2', ascending=True)
        else:
            print('Complete dates')
            return data
    else:
        print('Dataset with Channel info')
        return data


def read_ga_data(filename, channels=False):
    """Read Google Analytics datasets."""
    print('Reading dataset...')
    data = pandas.read_csv(filename, encoding='utf_16_le', sep='\t')
    # Define better column names
    data.rename(columns={'ga:date': 'date',
                         'ga:users': 'users',
                         'ga:newUsers': 'usersNew',
                         'ga:percentNewSessions': 'percentNewSessions',
                         'ga:sessions': 'sessions',
                         'ga:bounceRate': 'bounceRate',
                         'ga:avgSessionDuration': 'avgSessionDuration',
                         'ga:pageviews': 'pageviews',
                         'ga:pageviewsPerSession': 'pageviewsPerSession',
                         'ga:uniquePageviews': 'uniquePageviews',
                         'ga:avgTimeOnPage': 'avgTimeOnPage'}, inplace=True)
    if channels:
        data.rename(columns={'ga:channelGrouping': 'channel'}, inplace=True)
    # Correct percentage
    data['percentNewSessions'] = data['percentNewSessions'] / 100
    data['bounceRate'] = data['bounceRate'] / 100
    # Derive new columns
    data['usersOld'] = data['users'] - data['usersNew']
    data['sessionsNew'] = data['sessions'] * data['percentNewSessions']
    data['sessionsOld'] = data['sessions'] * (1 - data['percentNewSessions'])
    data['sessionsBounce'] = data['sessions'] * data['bounceRate']
    data['sessionsNoBounce'] = data['sessions'] * (1 - data['bounceRate'])
    # Create date object column and sort the dataframe by date
    data['date2'] = [dt.datetime.strptime(d, '%Y%m%d') for d in data['date'].astype('str')]
    # Check and complete range of days if necessary.
    data = complete_dates(data, channels)
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
