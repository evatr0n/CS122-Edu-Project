import nctq
import default_stat_analysis as d
import basic_regression
import nces
import numpy as np
import fws
import pandas as pd
import os

print("Loading NCTQ Teaching Policy data.....")
nctqdic_original = nctq.crawl_nctq()
print("Loading NCES Educational Outcome data.....")
#nces_original = nces2.original.sort_index()

nces_final = nces.final.sort_index()
nces_trends = nces_final[[col for col in nces_final.columns if col.startswith("Trend")]]

nctqdic_filled = nctq.fill_na(nctqdic_original)
avg_nctq = nctq.average_df(nctqdic_filled).sort_index()  
centered_avg_nctq = nctq.center_df(avg_nctq) # Use this for default scores.

# computing individual weights of policies through bivariate regression
print("Calculating state overall scores...")
states_overall_effectiveness_score, state_to_policy_effectiveness_score, policy_weight_dic =\
    d.default_calc(avg_nctq, centered_avg_nctq, nces_trends, 0.05)
print("Loading completed")

#################################################################################
# get dataframes directly from csv files instead of running crawlers


nctqdic_original = {}
for filename in os.listdir("csv/"):
    if filename.startswith("nctq"):
        nctqdic_original[filename.strip(".csv")] = pd.read_csv("csv/{}".format(filename), index_col = 0)
nctqdic_filled = nctq.fill_na(nctqdic_original)
avg_nctq = nctq.average_df(nctqdic_filled).sort_index()  
centered_avg_nctq = nctq.center_df(avg_nctq)

nces_final = pd.read_csv("csv/nces_final.csv", index_col=0)
nces_trends = nces_final[[col for col in nces_final.columns if col.startswith("Trend")]]
nces_original = pd.read_csv("csv/nces_raw.csv", index_col=0)
'''
    try:
        year = int(filename.strip(".csv")[-4:])
    except Exception:
        year = "string"
    if isinstance(year, int):
        nctqdic_original[filename.strip(".csv")] = pd.read_csv("csv/{}".format(filename))
'''