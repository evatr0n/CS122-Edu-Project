import crawler
import default_stat_analysis
import basic_regression
import nces
import numpy as np
import numbers
import fws
import pandas as pd

print("Loading NCTQ Teaching Policy data.....")
nctqdic_original = crawler.crawl_nctq()
print("Loading NCES Educational Outcome data.....")
nces_original = nces.final.sort_index()
nces_filled = nces.filled.sort_index()

nctqdic_filled = crawler.fill_na(nctqdic_original)
avg_nctq = crawler.average_df(nctqdic_filled).sort_index()  # Use this for default scores.

# computing individual weights of policies through bivariate regression
weights_per_outcome = {}
for outcome in nces.filled.columns:
    weights_per_outcome[outcome] = basic_regression.cutoff_R2(avg_nctq, nces.filled[outcome], 0.1)

    fws.forward_selection(avg_nctq[[tup[0] for tup in weights_per_outcome[outcome]])



for y in nces.filled.columns:
    fws.forward_selection(avg_nctq, y)
