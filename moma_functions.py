import pandas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

# Read datasets functions


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
    # Correct percentage
    data['percentNewSessions'] = data['percentNewSessions'] / 100
    data['bounceRate'] = data['bounceRate'] / 100
    # Derive new columns
    data['usersOld'] = data['users'] - data['usersNew']
    data['sessionsNew'] = data['sessions'] * data['percentNewSessions']
    data['sessionsOld'] = data['sessions'] * (1 - data['percentNewSessions'])
    data['sessionsBounce'] = data['sessions'] * data['bounceRate']
    data['sessionsNoBounce'] = data['sessions'] * (1 - data['bounceRate'])
    # Check complete range of days
    d1 = dt.datetime.strptime(data.iloc[0, 0].astype('str'), '%Y%m%d')
    d2 = dt.datetime.strptime(data.iloc[data.shape[0] - 1, 0].astype('str'), '%Y%m%d')
    diff = d2 - d1
    if data.shape[0] != diff.days + 1:
        print('Some dates are missing!')
    else:
        print('Complete dates')
    return data


# Plot datasets functions

def plot_visitors(dataset):
    plt.figure(figsize=(10,4))
    plt.plot_date(x=[mdates.strpdate2num('%d/%m/%y')(d) for d in dataset['Date']], y=dataset['visitors'], fmt='r-')
    plt.title('MoMA visitors')
    plt.ylabel('Visitors')
    plt.grid(True)
    plt.show()


def plot_gametrics(dataset, metricname):
    plt.figure(figsize=(10,4))
    plt.plot_date(x=[mdates.strpdate2num('%Y%m%d')(d) for d in dataset['date'].astype('str')], y=dataset[metricname], fmt='b-')
    plt.title('MoMA GA metric')
    plt.ylabel(metricname)
    plt.grid(True)
    plt.show()
