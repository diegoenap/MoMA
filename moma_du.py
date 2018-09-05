import pandas
import moma_functions as mf
import datetime
# Data Understanding

import importlib
importlib.reload(mf)

# MoMA Visitors ===========================================================================
moma_visitors = pandas.read_csv('data/visits/MoMA_visitors.csv')

moma_visitors.shape
moma_visitors.head(10)
moma_visitors.describe()

# moma_visitors['Date'] = moma_visitors['Date'].astype('datetime64[ns]')

mf.plot_visitors(moma_visitors)


# MoMA GA ===========================================================================
pandas.set_option('display.max_columns', 20)

ga_bo_us = mf.read_ga_data('data/ga/moma_both_nony_nochn.tsv')


GA_bo = mf.read_ga_data('data/ga/moma_both_all_nochn.tsv')
GA_bo_os = mf.read_ga_data('data/ga/moma_both_nousa_nochn.tsv')
GA_bo_us = mf.read_ga_data('data/ga/moma_both_usa_nochn.tsv')
GA_bo_do = mf.read_ga_data('data/ga/moma_both_nony_nochn.tsv')
GA_bo_lo = mf.read_ga_data('data/ga/moma_both_ny_nochn.tsv')

GA_bo_chn = mf.read_ga_data('data/ga/moma_both_all_chn.tsv', channels=True)
GA_bo_chn_os = mf.read_ga_data('data/ga/moma_both_nousa_chn.tsv', channels=True)
GA_bo_chn_us = mf.read_ga_data('data/ga/moma_both_usa_chn.tsv', channels=True)
GA_bo_chn_do = mf.read_ga_data('data/ga/moma_both_nony_chn.tsv', channels=True)
GA_bo_chn_lo = mf.read_ga_data('data/ga/moma_both_ny_chn.tsv', channels=True)

GA_vi = mf.read_ga_data('data/ga/moma_visit_all_nochn.tsv')
GA_vi_os = mf.read_ga_data('data/ga/moma_visit_nousa_nochn.tsv')
GA_vi_us = mf.read_ga_data('data/ga/moma_visit_usa_nochn.tsv')
GA_vi_do = mf.read_ga_data('data/ga/moma_visit_nony_nochn.tsv')
GA_vi_lo = mf.read_ga_data('data/ga/moma_visit_ny_nochn.tsv')

GA_vi_chn = mf.read_ga_data('data/ga/moma_visit_all_chn.tsv')
GA_vi_chn_os = mf.read_ga_data('data/ga/moma_visit_nousa_chn.tsv')
GA_vi_chn_us = mf.read_ga_data('data/ga/moma_visit_usa_chn.tsv')
GA_vi_chn_do = mf.read_ga_data('data/ga/moma_visit_nony_chn.tsv')
GA_vi_chn_lo = mf.read_ga_data('data/ga/moma_visit_ny_chn.tsv')

GA_tk = mf.read_ga_data('data/ga/moma_tickets_all_nochn.tsv')
GA_tk_os = mf.read_ga_data('data/ga/moma_tickets_nousa_nochn.tsv')
GA_tk_us = mf.read_ga_data('data/ga/moma_tickets_usa_nochn.tsv')
GA_tk_do = mf.read_ga_data('data/ga/moma_tickets_nony_nochn.tsv')
GA_tk_lo = mf.read_ga_data('data/ga/moma_tickets_ny_nochn.tsv')

GA_tk_chn = mf.read_ga_data('data/ga/moma_tickets_all_chn.tsv')
GA_tk_chn_os = mf.read_ga_data('data/ga/moma_tickets_nousa_chn.tsv')
GA_tk_chn_us = mf.read_ga_data('data/ga/moma_tickets_usa_chn.tsv')
GA_tk_chn_do = mf.read_ga_data('data/ga/moma_tickets_nony_chn.tsv')
GA_tk_chn_lo = mf.read_ga_data('data/ga/moma_tickets_ny_chn.tsv')



ga_bo_us.columns
ga_bo_us.shape
ga_bo_us.tail(1)

mf.plot_gametrics(ga_bo_us, 'sessionsOld')



