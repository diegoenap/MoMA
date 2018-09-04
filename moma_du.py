import pandas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
#import moma_functions as mf
# Data Understanding

moma_visitors = pandas.read_csv("data/visits/MoMA_visitors.csv")

moma_visitors.shape
moma_visitors.head(10)
moma_visitors.describe()

# moma_visitors['Date'] = moma_visitors['Date'].astype('datetime64[ns]')


def plot_visitors(dataset):
    plt.figure(figsize=(10,4))
    plt.plot_date(x=[mdates.strpdate2num('%d/%m/%y')(d) for d in dataset['Date']], y=dataset['visitors'], fmt='r-')
    plt.title('MoMA visitors')
    plt.ylabel('Visitors')
    plt.grid(True)
    plt.show()


plot_visitors(moma_visitors)