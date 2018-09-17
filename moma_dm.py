import moma_functions as mf
import pandas

def moma_analysis():
    # Read visitors dataset
    moma_visitors = mf.read_visitors_data('data/visits/MoMA_visitors.csv')

    # Read GA metrics
    ga_bo = mf.read_ga_data('data/ga/moma_both_all_nochn.tsv')

    # Prepare data
    # print(moma_visitors['date2'] > '2015-07-03')
    # print(ga_bo.head(5))
    # print(ga_bo['date2'] > '2016-01-10')
    # print(moma_visitors['date2'][0] == ga_bo['date2'][0])

    # Limit the datasets
    init_date = pandas.to_datetime('2016-07-09')
    end_date = pandas.to_datetime('2018-05-31')
    max_lag = pandas.Timedelta(days=31)
    moma_visitors = moma_visitors.loc[(moma_visitors['date2'] >= init_date+max_lag) & (moma_visitors['date2'] <= end_date), :]
    ga_bo = ga_bo.loc[(ga_bo['date2'] >= init_date) & (ga_bo['date2'] <= end_date), :]

    print(moma_visitors.head())
    print(ga_bo.head())

    # Get correlation matrix
    # mf.get_correlation_matrix(moma_visitors, ga_bo)


if __name__ == '__main__':
    moma_analysis()
