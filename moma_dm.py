import moma_functions as mf
import pandas


def moma_analysis():
    # Read visitors dataset
    vsdf = mf.read_visitors_data('data/visits/MoMA_visitors.csv')

    # Read GA metrics
    gadf = mf.read_ga_data('data/ga/moma_both_all_nochn.tsv')

    max_lag = pandas.Timedelta(days=31)

    # print('Init date for Visitors: {}'.format(vsdf.date2.iloc[0]))
    # print('Init date for GA metric: {}'.format(gadf.date2.iloc[0]))

    # Limit the datasets
    if (vsdf.date2.iloc[0] - gadf.date2.iloc[0]) <= max_lag:
        # print('Distance between both init dates allow for using GA metric init date as the initial date')
        init_date = gadf.date2.iloc[0]
    else:
        # print('Visitors init date is greater than GA metrics ina  number of dates greater than the lag.')
        init_date = vsdf.date2.iloc[0] - max_lag.days

    # For end_date use the smaller final date
    end_date = min(vsdf.date2.iloc[-1], gadf.date2.iloc[-1])

    # Limit the datasets with the new initial and end dates
    vsdf = vsdf.loc[(vsdf['date2'] >= init_date+max_lag) & (vsdf['date2'] <= end_date), :]
    gadf = gadf.loc[(gadf['date2'] >= init_date) & (gadf['date2'] <= end_date), :]

    # print(vsdf.head(1))
    # print(vsdf.tail(1))
    # print(gadf.head(1))
    # print(gadf.tail(1))

    # Get correlation matrix
    m = mf.get_correlation_matrix(vsdf, gadf)
    print(m)


if __name__ == '__main__':
    moma_analysis()
