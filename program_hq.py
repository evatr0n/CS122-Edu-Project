import nctq
import default_stat_analysis
import basic_regression
import nces
import numpy as np
import numbers
import fws
import pandas as pd

print("Loading NCTQ Teaching Policy data.....")
nctqdic_original = nctq.crawl_nctq()
print("Loading NCES Educational Outcome data.....")
nces_original = nces.final.sort_index()
nces_filled = nces.filled.sort_index()

nctqdic_filled = nctq.fill_na(nctqdic_original)
avg_nctq = nctq.average_df(nctqdic_filled).sort_index()  
centered_avg = nctq.center_df(avg_nctq) # Use this for default scores.

# computing individual weights of policies through bivariate regression
