import requests
import bs4
import pandas as pd
import numpy as np
import re
from sklearn import preprocessing 
import scipy
import os

# FOR GROUPMATES
# nces.final is the table you want but you can also just use the csv that i
# uploaded as well. still some bugs to fix but it's real close.


data = {"https://nces.ed.gov/programs/digest/d19/tables/dt19_203.90.asp?current=yes" :
[(0, "2007 Average Daily Attendance %"), (6, "2011 Average Daily Attendance %")],

"https://nces.ed.gov/programs/digest/d19/tables/dt19_204.90.asp?current=yes":
[(0, "2004 Students Enrolled in Gifted Programs %"), 
(3, "2006 Students Enrolled in Gifted Programs %"), 
(6, "2011 Students Enrolled in Gifted Programs %"), 
(7, "2013 Students Enrolled in Gifted Programs %")],



"https://nces.ed.gov/programs/digest/d19/tables/dt19_219.85b.asp?current=yes": 
[(0, "2018 Percentage of HS Drop Outs Age 16-24")],

"https://nces.ed.gov/programs/digest/d19/tables/dt19_221.72.asp?current=yes":
[(10, "2019 8th Grade Reading Scores")],



"https://nces.ed.gov/programs/digest/d19/tables/dt19_211.30.asp?current=yes":
[(32, "2007 Average Base Teacher Salary w/ Bachelors"),
(34, "2011 Average Base Teacher Salary w/ Bachelors"),
(40, "2017 Average Base Teacher Salary w/ Bachelors")],


"https://nces.ed.gov/programs/digest/d19/tables/dt19_211.40.asp?current=yes":
[(34, "2007 Average Base Teacher Salary w/ Masters Constant Dollars"),
(36, "2011 Average Base Teacher Salary w/ Masters Constant Dollars"),
(42, "2017 Average Base Teacher Salary w/ Masters Constant Dollars")],


 "https://nces.ed.gov/programs/digest/d20/tables/dt20_213.40.asp?current=yes":
 [(1, "2005 Teacher Percentage of School Staff"),
 (2, "2010 Teacher Percentage of School Staff"),
 (6, "2015 Teacher Percentage of School Staff"),
 (15, "2018 Teacher Percentage of School Staff")],

"https://nces.ed.gov/programs/digest/d19/tables/dt19_214.30.asp?current=yes":
[(1, "2018 Number of Education Agencies")]}

data2 = {"https://nces.ed.gov/programs/digest/d19/tables/dt19_204.75c.asp?current=yes":
(False, (8, 16), 1, "Percent of Students Experiencing Homelessness"),

"https://nces.ed.gov/programs/digest/d19/tables/dt19_219.35.asp?current=yes":
(True, (8, 15), 0, "Average Freshman Graduation Rate"),



"https://nces.ed.gov/programs/digest/d19/tables/dt19_221.40.asp?current=yes":
(True, (5, 13), 1, "4th Grade Reading Scores"),

"https://nces.ed.gov/programs/digest/d19/tables/dt19_222.60.asp?current=yes":
(True, (5, 13), 1, "8th Grade Math Scores"),


"https://nces.ed.gov/programs/digest/d19/tables/dt19_222.50.asp?current=yes": 
(True, (4, 12), 1, "4th Grade Math Scores"),

 "https://nces.ed.gov/programs/digest/d19/tables/dt19_211.60.asp?current=yes":
 (False, (8, 14), 1, "Overall Average Teacher Salary"),

 "https://nces.ed.gov/programs/digest/d20/tables/dt20_216.90.asp?current=yes":
(False, (10, 15), 1, "% of Public Schools That Are Charters"),

"https://nces.ed.gov/programs/digest/d19/tables/dt19_219.46.asp?current=yes":
(True, (0, 8), 1, "Adjusted Cohort Graduation Rate")}


not_states = ['Other jurisdictions', 'American Samoa', 'Guam',
'Northern Marianas', 'Puerto Rico', 'U.S. Virgin Islands', 
'Department of Defense Education Activity (DoDEA)']


#1
def grab_frame(site):
    frame = pd.read_html(site, attrs = {"class" : 
    "tableMain"})[0]
    return frame

#2
def set_index(df):
    df = df.dropna(how = 'all')
    top_left = df.columns.values[0]
    df = df.set_index(top_left)
    return df
    



#4
def remove_footnotes(df):
    index = df.index.tolist()
    for i in range(len(index)):
        new = (re.sub(r'[0-9,]*', "", index[i]))
        index[i] = new
    df.index = index
    return df


#5
def drop_se(df):
    cols = df.columns
    index = len(cols[0]) - 1
    drops = []
    for col in cols:
        if "." in col[index]:
            drops.append(col)
    df.drop(columns=drops, inplace=True)
    
#6    
def drop_se2(df):
    last_col = len(df.columns) - 2
    new = df[[df.columns[last_col]]].copy()
    return new

#7
def drop_colnums(df):
    df.columns = df.columns.droplevel(1)
    return df


#8
def last_col(df):
    last_col = len(df.columns) - 1
    new = df[[df.columns[last_col]]].copy()
    return new

#9
def first_col(df):
    new = df[[df.columns[0]]].copy()
    return new
#A
def remove_repeat(df):
    new_cols = []
    for i in range(len(df.columns)):
        new_cols.append(df.columns[i] + str(i))
    df.columns = new_cols
    new = df[[df.columns[0]]].copy()
    return new

def replace_na(df):
    df = df.fillna(0)
    df = df.replace({'‡': 0, "#": 0, "—": 0, "---": 0})
    for col in df.columns:
        df[col].replace({0: df[col][0]}, inplace=True)
    return df

def remove_dollar(df):
    for col in df.columns:
        df[col] = df[col].astype(str)
        df[col] = df[col].str.replace(r"[$,]", '')
    return df

def df_crawl1(df_dict):
    dfs = []
    for key, value in df_dict.items():
        df = grab_frame(key)
        df = set_index(df)
        df = remove_footnotes(df)
        if len(value) == 1:
            df = df[df.columns[value[0][0]]].to_frame()
            df.columns = [value[0][1]]
            df = replace_na(df)
            dfs.append(df)
        else:
            frames = []
            for i in range(len(value)):
                frame = df[df.columns[value[i][0]]].to_frame()
                frame.columns = [value[i][1]]
                frame = replace_na(frame)
                frames.append(frame)
            first_frame = frames[0]
            for i in range(1, len(frames)):
                if i == 1:
                    dataframe = first_frame.join(frames[i])
                else:
                    dataframe = dataframe.join(frames[i])
            dfs.append(dataframe)
    return dfs




def df_crawl2(df_dict):
    dfs = []
    for key, value in df_dict.items():
        df = grab_frame(key)
        df = set_index(df)
        df = remove_footnotes(df)
        if value[0] == True:
            drop_se(df)
        cols = []
        for i in range(value[1][0], value[1][1]):
            col = df[df.columns[i]].to_frame()
            col.columns = [df.columns[i][value[2]][:4] + " " + value[3]] 
            col = replace_na(col)
            cols.append(col)
        first_col = cols[0]
        for i in range(1, len(cols)):
            if i == 1:
                dataframe = first_col.join(cols[i])
            else:
                dataframe = dataframe.join(cols[i])
        dfs.append(dataframe)
    return dfs







dfs1 = df_crawl1(data)
dfs1[4] = remove_dollar(dfs1[4])
dfs1[5] = remove_dollar(dfs1[5])
dfs2 = df_crawl2(data2)
dfs2[5] = remove_dollar(dfs2[5])

def normalize(df):
    x = df.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    normalized = pd.DataFrame(x_scaled)
    normalized.index = df.index
    normalized.columns = df.columns
    for col in normalized.columns:
        normalized[col] = 100* normalized[col]
    return normalized


def get_slope(row):
    axisvalues = list(range(1, len(row) + 1))
    regression = scipy.stats.linregress(row, y=axisvalues)
    return regression.slope 


def add_slope(df):
    col_name = "Trend: " + df.columns[0][5:]
    df[col_name] = df.apply(get_slope, axis=1)
    return df


def final_frame(dfs):
    final_dfs = []
    for df in dfs:
        if len(df.columns) == 1:
            df = normalize(df)
            final_dfs.append(df)
        else:
            df = normalize(df)
            df = add_slope(df)
            final_dfs.append(df)
    first_frame = dfs[0]
    for i in range(1, len(final_dfs)):
        if i == 1:
            final = first_frame.join(final_dfs[i])
        else:
            final = final.join(final_dfs[i])
    return final



final = final_frame(dfs1).join(final_frame(dfs2))

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
    'United States': 'US'
}
final.rename(index=us_state_abbrev, inplace=True)


outfile = "/home/jrgill/Desktop/cmsc12200-win-21-jrgill/Project/place"
y = "final.csv"

final.to_csv(os.path.join(outfile, y))





























# dfs = []
#     df = grab_frame(thing1)
#     df = set_index(df)
#     df = remove_footnotes(df)
#     df = df[thing2[0]].to_frame()
#     df.columns = [thing2[1]]
#     dfs.append(df)

# first_frame = dfs[0]
# for i in range(1, len(dfs)):
#     if i == 1:
#         final = first_frame.join(dfs[i])
#     else:
#         final = final.join(dfs[i])

