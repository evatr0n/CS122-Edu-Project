import crawler
import default_stat_analysis
import basic_regression
import nces

print("Loading NCTQ Teaching Policy data.....")
df_dic = crawler.crawl_nctq()
print("Loading NCES Educational Outcome data.....")
nces_df = nces.final



