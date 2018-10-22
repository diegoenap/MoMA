import pandas as pd
import sys
import glob


def consolidate():
    # Get all the correlation files corresponding to a website section and consolidate them in one dataframe. Write the
    # dataframe as CSV file.
    site_section = sys.argv[1]
    path = "output/"
    corr_files = glob.glob(path + "corr-" + site_section + "*.csv")
    df = pd.DataFrame()
    consol = []
    print("Consolidating files for {}".format(sys.argv[1]))
    for f in corr_files:
        tmp = pd.read_csv(f, index_col=None, header=0)
        consol.append(tmp)
    df = pd.concat(consol)
    df.reset_index(drop=True, inplace=True)
    print("Writing new file")
    # df.to_csv("output/correlations-" + site_section + ".csv", index=False, na_rep=0)
    # Getting the best correlation for this section. First, get the max for each transformation test, then get the max

    # print(df.iloc[:, range(1, df.shape[1]-1, 2)])
    # print(df.iloc[:, range(1, df.shape[1]-1, 2)].max())
    # print(df.iloc[:, range(1, df.shape[1]-1, 2)].max().max())

    max_cor = df.iloc[:, range(1, df.shape[1]-1, 2)].max()
    max_pos = df.iloc[:, range(1, df.shape[1]-1, 2)].idxmax()
    print(max_cor.idxmax())


    # tmpmax = []
    # for i in range(1, df.shape[1]-1, 2):
    #     max_corr = max(df.iloc[:, i])
    #     max_loc = df.iloc[:, i].idxmax(axis=1)
    #     # print("Col {} has max {} at {}".format(i, max_corr, max_loc))
    #     tmpmax.append(pd.DataFrame({'Col': [i], 'Max': [max_corr], 'Pos': [max_loc]}))
    # df2 = pd.concat(tmpmax)
    # df2.reset_index(drop=True, inplace=True)
    # max_loc = df2.Max.idxmax(axis=1)
    #
    # print(df.iloc[37, 9:11])






if __name__ == '__main__':
    consolidate()