import moma_functions as mf
import pandas


def moma_analysis():
    # Read visitors dataset
    vsdf = mf.read_visitors_data('data/visits/MoMA_visitors.csv')
    gadf = mf.read_ga_data('data/ga/moma_both_all_nochn.tsv')
    # Limit the range of dates in the datasets. If the Visitors start date is smaller than the GA metrics start date, or
    # if it is between the 'maxlag' range, then use the GA metric start date. Otherwise the Initial date is the Visitors
    # start date minus the 'maxlag'.
    max_lag = pandas.Timedelta(days=31)
    if (vsdf.index[0] - gadf.index[0]) <= max_lag:
        init_date = gadf.index[0]
    else:
        init_date = vsdf.index[0] - max_lag.days
    # For end_date use the smaller final date
    end_date = min(vsdf.index[-1], gadf.index[-1])
    # Limit the datasets with the new initial and end dates
    vsdf = vsdf[init_date + max_lag:end_date]
    gadf = gadf[str(init_date):str(end_date)]

    # Get correlation matrix
    mf.get_correlation_matrix(vsdf, gadf)

    # # Limit the datasets
    # if (vsdf.date2.iloc[0] - gadf.date2.iloc[0]) <= max_lag:
    #     # print('Distance between both init dates allow for using GA metric init date as the initial date')
    #     init_date = gadf.date2.iloc[0]
    # else:
    #     # print('Visitors init date is greater than GA metrics ina  number of dates greater than the lag.')
    #     init_date = vsdf.date2.iloc[0] - max_lag.days
    #
    # # For end_date use the smaller final date
    # end_date = min(vsdf.date2.iloc[-1], gadf.date2.iloc[-1])
    #
    # # Limit the datasets with the new initial and end dates
    # vsdf = vsdf.loc[(vsdf['date2'] >= init_date+max_lag) & (vsdf['date2'] <= end_date), :]
    # gadf = gadf.loc[(gadf['date2'] >= init_date) & (gadf['date2'] <= end_date), :]
    #
    # # Get correlation matrix
    # m = mf.get_correlation_matrix(vsdf, gadf)
    # print(m)


if __name__ == '__main__':
    moma_analysis()
