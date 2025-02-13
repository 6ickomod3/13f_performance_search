import re
import numpy as np
import pandas as pd

# Colume name
"""
1: Filer
2: WhaleScore 1 Yr Equal-Wt
4: Fund Size
5: Holdings
6: MV
7: Turnover
10: Perf Equal All
18: 3 Yr Perf Annualized
19: 5 Yr Perf Annualized
20: 7 Yr Perf Annualized
21: 10 Yr Perf Annualized
37: 3-Year Sortino Equal Weight
38: STDDEV 3-Year
39: 5 Yr Beta
40: 3 Yr Alpha
43: Investing Styles
44: Fund Classifications
"""

pValue = 50
csv_file = '/Users/jdai/Documents/13f/data/form_13f_performance_24q4.csv'

is_filter_by_3yr = True
is_filter_by_5yr = True
is_filter_by_7yr = True
is_filter_by_alpha = False
is_filter_by_beta = False
is_filter_by_all_time = False
is_filter_by_whale_score = False
is_filter_by_fund_style = True
is_filter_by_sortino = True

def print_fund_detail(df, row_id):
    print("fund name: " + str(df.iloc[row_id,1]))
    print("fund holdings: " + str(df.iloc[row_id,6] if not np.isnan(df.iloc[row_id,6]) else 0))
    print("fund whale score: " + str(df.iloc[row_id,3] if not np.isnan(df.iloc[row_id,3]) else 0))
    print("fund all time: " + str(df.iloc[row_id,11] if not np.isnan(df.iloc[row_id,11]) else 0))
    print("fund 3 Yr: " + str(df.iloc[row_id,19] if not np.isnan(df.iloc[row_id,19]) else 0))
    print("fund 5 Yr: " + str(df.iloc[row_id,20] if not np.isnan(df.iloc[row_id,20]) else 0))
    print("fund 7 Yr: " + str(df.iloc[row_id,21] if not np.isnan(df.iloc[row_id,21]) else 0))
    print("fund 10 Yr: " + str(df.iloc[row_id,22] if not np.isnan(df.iloc[row_id,22]) else 0))
    print("fund Sortino 3 Yr: " + str(df.iloc[row_id,38] if not np.isnan(df.iloc[row_id,38]) else 0))
    print("fund Beta 5 Yr: " + str(df.iloc[row_id,40] if not np.isnan(df.iloc[row_id,40]) else 0))
    print("fund Alpha 3 Yr: " + str(df.iloc[row_id,41] if not np.isnan(df.iloc[row_id,41]) else 0))
    print("fund style: " + str(df.iloc[row_id,44]))
    print("fund classification: " + str(df.iloc[row_id,45]))
    print("="*40)

if __name__ == "__main__":
    # Read the Excel file into a Pandas DataFrame
    # The sheet_name parameter specifies the name of the sheet to read ('Rebalancing' in this case)
    df = pd.read_csv(csv_file)

    selected_funds = []
    keys_dict = {}
    # for idx in range(len(df.columns)):
    #     print(idx,df.columns[idx])
        # keys_dict.update({df.columns[idx]:idx})

    annualized_7yr_return = np.round([float(x) if not np.isnan(x) else 0 for x in df['7 Yr Perf Annualized'].values],2)
    annualized_5yr_return = np.round([float(x) if not np.isnan(x) else 0 for x in df['5 Yr Perf Annualized'].values],2)
    annualized_3yr_return = np.round([float(x) if not np.isnan(x) else 0 for x in df['3 Yr Perf Annualized'].values],2)
    annualized_3yr_alpha = np.round([float(x) if not np.isnan(x) else 0 for x in df['3 Yr Alpha'].values],2)
    annualized_5yr_beta = np.round([float(x) if not np.isnan(x) else 0 for x in df['5 Yr Beta'].values],2)
    whale_score = np.round([float(x) if not np.isnan(x) else 0 for x in df['WhaleScore 1 Yr Equal-Wt'].values],2)
    all_time_return = np.round([float(x) if not np.isnan(x) else 0 for x in df['Perf Equal All'].values],2)
    sortino_3yr = np.round([float(x) if not np.isnan(x) else 0 for x in df['3-Year Sortino Equal Weight'].values],2)

    p_threshold_7yr = np.percentile(annualized_7yr_return[np.nonzero(annualized_7yr_return)],pValue)
    p_threshold_5yr = np.percentile(annualized_5yr_return[np.nonzero(annualized_5yr_return)],pValue)
    p_threshold_3yr = np.percentile(annualized_3yr_return[np.nonzero(annualized_3yr_return)],pValue)
    p_threshold_3yr_alpha = np.percentile(annualized_3yr_alpha,pValue)
    p_threshold_5yr_beta = np.percentile(annualized_5yr_beta,pValue)
    p_threshold_whale_score = np.percentile(whale_score[np.nonzero(whale_score)],pValue)
    p_threshold_all_time_return = np.percentile(all_time_return,pValue)
    p_threshold_sortino_3yr = np.percentile(sortino_3yr[np.nonzero(sortino_3yr)],pValue)
    fund_style_set_include = ["Long-Term Focus"]
    fund_style_set_exclude = []

    print(p_threshold_7yr)

    for row_id in range(df.shape[0]):
        fund_name = str(df.iloc[row_id,1])
        fund_holdings = float(df.iloc[row_id,6]) if not np.isnan(df.iloc[row_id,6]) else 0
        fund_3yr_return = float(df.iloc[row_id,19]) if not np.isnan(df.iloc[row_id,19]) else 0
        fund_5yr_return = float(df.iloc[row_id,20]) if not np.isnan(df.iloc[row_id,20]) else 0
        fund_7yr_return = float(df.iloc[row_id,21]) if not np.isnan(df.iloc[row_id,21]) else 0
        fund_5yr_beta = float(df.iloc[row_id,40]) if not np.isnan(df.iloc[row_id,40]) else 0
        fund_3yr_alpha = float(df.iloc[row_id,41]) if not np.isnan(df.iloc[row_id,41]) else 0
        fund_all_time_return = float(df.iloc[row_id,11]) if not np.isnan(df.iloc[row_id,11]) else 0
        fund_whale_score = float(df.iloc[row_id,3]) if not np.isnan(df.iloc[row_id,3]) else 0
        fund_sortino_3yr = float(df.iloc[row_id,38]) if not np.isnan(df.iloc[row_id,38]) else 0
        fund_style = str(df.iloc[row_id,44])
        # if fund_holdings<10:
        #     continue
        if is_filter_by_3yr:
            if fund_3yr_return < p_threshold_3yr:
                continue
        if is_filter_by_5yr:
            if fund_5yr_return < p_threshold_7yr:
                continue
        if is_filter_by_7yr:
            if fund_7yr_return < p_threshold_7yr:
                continue
        if is_filter_by_all_time:
            if fund_all_time_return < p_threshold_all_time_return:
                continue
        if is_filter_by_whale_score:
            if fund_whale_score < p_threshold_whale_score:
                continue
        if is_filter_by_sortino:
            if fund_sortino_3yr < p_threshold_sortino_3yr:
                continue
        if is_filter_by_fund_style:
            if any(substring in fund_style for substring in fund_style_set_exclude):
                continue
            if not all(substring in fund_style for substring in fund_style_set_include):
                continue
        if is_filter_by_alpha:
            if fund_3yr_alpha < p_threshold_3yr_alpha:
                continue
        if is_filter_by_beta:
            if fund_5yr_beta < p_threshold_5yr_beta:
                continue
        selected_funds.append(fund_name)
        print_fund_detail(df, row_id)

    print(len(selected_funds))
    print(selected_funds)
