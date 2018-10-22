import lagfunc as lf
import pandas as pd
import sys

def analise():
    print("Visitors file   : {}".format(sys.argv[1]))
    print("GA metrics file : {}".format(sys.argv[2]))
    print("Dataset name    : {}".format(sys.argv[3]))
    visitors_file = sys.argv[1]
    gametrics_file = sys.argv[2]
    dataset_name = sys.argv[3]
    # Read visitors dataset
    vsdf = lf.read_visitors_data(visitors_file)
    gadf = lf.read_ga_data(gametrics_file)

    # Limit the range of dates in the datasets. If the Visitors start date is smaller than the GA metrics start date, or
    # if it is between the 'maxlag' range, then use the GA metric start date. Otherwise the Initial date is the Visitors
    # start date minus the 'maxlag'.
    # (Check this code for automaic resize)
    print("Resize datasets...")
    max_lag = pd.Timedelta(days=31)
    if (vsdf.index[0] - gadf.index[0]) <= max_lag:
        init_date = gadf.index[0]
    else:
        init_date = vsdf.index[0] - max_lag.days
    # For end_date use the smaller final date
    end_date = min(vsdf.index[-1], gadf.index[-1])
    # Limit the datasets with the new initial and end dates
    vsdf = vsdf[init_date + max_lag:end_date]
    gadf = gadf[str(init_date):str(end_date)]


    # print(gadf[gadf.channel == '(Other)'].drop(columns=['channel']).rolling(7).mean())

    # Get correlation matrix
    print("Getting correlation matrix...")
    if 'channel' in gadf.columns:
        print("GA metrics dataset contains channel information")
        for ch in lf.channels:
            print("Channel: {}".format(ch))
            # print(gadf[gadf.channel == ch])
            test_table = lf.run_correlation_tests(vsdf, gadf[gadf.channel == ch], max_lag.days, dataset_name + "-" + ch)
            # print(test_table)
            test_table.to_csv("output/corr-" + dataset_name + "-" + ch + ".csv", index=False, na_rep=0)
    else:
        print("")
        test_table = lf.run_correlation_tests(vsdf, gadf, max_lag.days, dataset_name)
        print(test_table)
        test_table.to_csv("output/corr-" + dataset_name + ".csv", index=False, na_rep=0)



if __name__ == '__main__':
    analise()
