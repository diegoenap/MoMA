import moma_functions as mf
import pandas as pd
import numpy as np


def moma_analysis():
    # Read visitors dataset
    vsdf = mf.read_visitors_data('data/visits/MoMA_visitors.csv')
    # gadf = mf.read_ga_data('data/ga/moma_both_all_nochn.tsv')

    # ========
    ga_bo = mf.read_ga_data("data/ga/moma_both_all_nochn.tsv")
    ga_bo_os = mf.read_ga_data("data/ga/moma_both_nousa_nochn.tsv")
    ga_bo_us = mf.read_ga_data("data/ga/moma_both_usa_nochn.tsv")
    ga_bo_do = mf.read_ga_data("data/ga/moma_both_nony_nochn.tsv")
    ga_bo_lo = mf.read_ga_data("data/ga/moma_both_ny_nochn.tsv")

    ga_bo_chn = mf.read_ga_data("data/ga/moma_both_all_chn.tsv")
    ga_bo_chn_os = mf.read_ga_data("data/ga/moma_both_nousa_chn.tsv")
    ga_bo_chn_us = mf.read_ga_data("data/ga/moma_both_usa_chn.tsv")
    ga_bo_chn_do = mf.read_ga_data("data/ga/moma_both_nony_chn.tsv")
    ga_bo_chn_lo = mf.read_ga_data("data/ga/moma_both_ny_chn.tsv")

    ga_vi = mf.read_ga_data("data/ga/moma_visit_all_nochn.tsv")
    ga_vi_os = mf.read_ga_data("data/ga/moma_visit_nousa_nochn.tsv")
    ga_vi_us = mf.read_ga_data("data/ga/moma_visit_usa_nochn.tsv")
    ga_vi_do = mf.read_ga_data("data/ga/moma_visit_nony_nochn.tsv")
    ga_vi_lo = mf.read_ga_data("data/ga/moma_visit_ny_nochn.tsv")

    ga_vi_chn = mf.read_ga_data("data/ga/moma_visit_all_chn.tsv")
    ga_vi_chn_os = mf.read_ga_data("data/ga/moma_visit_nousa_chn.tsv")
    ga_vi_chn_us = mf.read_ga_data("data/ga/moma_visit_usa_chn.tsv")
    ga_vi_chn_do = mf.read_ga_data("data/ga/moma_visit_nony_chn.tsv")
    ga_vi_chn_lo = mf.read_ga_data("data/ga/moma_visit_ny_chn.tsv")

    ga_tk = mf.read_ga_data("data/ga/moma_tickets_all_nochn.tsv")
    ga_tk_os = mf.read_ga_data("data/ga/moma_tickets_nousa_nochn.tsv")
    ga_tk_us = mf.read_ga_data("data/ga/moma_tickets_usa_nochn.tsv")
    ga_tk_do = mf.read_ga_data("data/ga/moma_tickets_nony_nochn.tsv")
    ga_tk_lo = mf.read_ga_data("data/ga/moma_tickets_ny_nochn.tsv")

    ga_tk_chn = mf.read_ga_data("data/ga/moma_tickets_all_chn.tsv")
    ga_tk_chn_os = mf.read_ga_data("data/ga/moma_tickets_nousa_chn.tsv")
    ga_tk_chn_us = mf.read_ga_data("data/ga/moma_tickets_usa_chn.tsv")
    ga_tk_chn_do = mf.read_ga_data("data/ga/moma_tickets_nony_chn.tsv")
    ga_tk_chn_lo = mf.read_ga_data("data/ga/moma_tickets_ny_chn.tsv")
    # ========

    # Limit the range of dates in the datasets. If the Visitors start date is smaller than the GA metrics start date, or
    # if it is between the 'maxlag' range, then use the GA metric start date. Otherwise the Initial date is the Visitors
    # start date minus the 'maxlag'.
    # (Check this code for automaic resize)
    max_lag = pd.Timedelta(days=31)
    # if (vsdf.index[0] - gadf.index[0]) <= max_lag:
    #     init_date = gadf.index[0]
    # else:
    #     init_date = vsdf.index[0] - max_lag.days
    # # For end_date use the smaller final date
    # end_date = min(vsdf.index[-1], gadf.index[-1])
    # # Limit the datasets with the new initial and end dates
    # vsdf = vsdf[init_date + max_lag:end_date]
    # gadf = gadf[str(init_date):str(end_date)]

    init_date = pd.to_datetime('2016-03-09')
    end_date = pd.to_datetime('2016-05-31')
    vsdf = vsdf[init_date + max_lag:end_date]
    ga_bo = ga_bo[str(init_date):str(end_date)]
    ga_bo_os = ga_bo_os[str(init_date):str(end_date)]
    ga_bo_us = ga_bo_us[str(init_date):str(end_date)]
    ga_bo_do = ga_bo_do[str(init_date):str(end_date)]
    ga_bo_lo = ga_bo_lo[str(init_date):str(end_date)]
    ga_bo_chn = ga_bo_chn[str(init_date):str(end_date)]
    ga_bo_chn_os = ga_bo_chn_os[str(init_date):str(end_date)]
    ga_bo_chn_us = ga_bo_chn_us[str(init_date):str(end_date)]
    ga_bo_chn_do = ga_bo_chn_do[str(init_date):str(end_date)]
    ga_bo_chn_lo = ga_bo_chn_lo[str(init_date):str(end_date)]
    ga_vi = ga_vi[str(init_date):str(end_date)]
    ga_vi_os = ga_vi_os[str(init_date):str(end_date)]
    ga_vi_us = ga_vi_us[str(init_date):str(end_date)]
    ga_vi_do = ga_vi_do[str(init_date):str(end_date)]
    ga_vi_lo = ga_vi_lo[str(init_date):str(end_date)]
    ga_vi_chn = ga_vi_chn[str(init_date):str(end_date)]
    ga_vi_chn_os = ga_vi_chn_os[str(init_date):str(end_date)]
    ga_vi_chn_us = ga_vi_chn_us[str(init_date):str(end_date)]
    ga_vi_chn_do = ga_vi_chn_do[str(init_date):str(end_date)]
    ga_vi_chn_lo = ga_vi_chn_lo[str(init_date):str(end_date)]
    ga_tk = ga_tk[str(init_date):str(end_date)]
    ga_tk_os = ga_tk_os[str(init_date):str(end_date)]
    ga_tk_us = ga_tk_us[str(init_date):str(end_date)]
    ga_tk_do = ga_tk_do[str(init_date):str(end_date)]
    ga_tk_lo = ga_tk_lo[str(init_date):str(end_date)]
    ga_tk_chn = ga_tk_chn[str(init_date):str(end_date)]
    ga_tk_chn_os = ga_tk_chn_os[str(init_date):str(end_date)]
    ga_tk_chn_us = ga_tk_chn_us[str(init_date):str(end_date)]
    ga_tk_chn_do = ga_tk_chn_do[str(init_date):str(end_date)]
    ga_tk_chn_lo = ga_tk_chn_lo[str(init_date):str(end_date)]
    print("")

    # # Get correlation matrix
    # test_table = mf.run_correlation_tests(vsdf, gadf, max_lag.days, 'Test ALL-DO')
    # print(test_table)




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
