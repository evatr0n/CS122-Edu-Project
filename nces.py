import requests
import bs4
import pandas as pd
import numpy as np
import re
from sklearn import preprocessing 

# FOR GROUPMATES
# nces.final produces the table with the raw data. nces.filled is the same frame
# but with all nan values filled in and money values ('$69,420') converted to
# strings ('69420') that pandas can automatically convert to ints. 



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
    
#3 
def remove_states(df):
    for index in df.index:
        if index in not_states:
            df = df.drop(index, axis=0)
    
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
def drop_se1(df):
    df.columns = df.columns.droplevel()
    return df
     
    
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



    



data = {"https://nces.ed.gov/programs/digest/d19/tables/dt19_203.90.asp?current=yes" :
[('[Standard errors appear in parentheses]',
 '2011-12',
 'Total elementary, secondary, and combined elementary/secondary schools',
 'ADA as percent of enrollment','4'), "Average Daily Attendance %"],

"https://nces.ed.gov/programs/digest/d19/tables/dt19_204.75c.asp?current=yes":
[('Homeless students as percent of total public school enrollment',
 '2016-17',
 '17'), "Percent of Students Experiencing Homelessness"],

"https://nces.ed.gov/programs/digest/d19/tables/dt19_204.90.asp?current=yes":
[('[Standard errors appear in parentheses]', '2013-141', 'Total', 'Total', 'Total', '5', '6.7'),
"Students Enrolled in Gifted Programs %"],

"https://nces.ed.gov/programs/digest/d19/tables/dt19_219.35.asp?current=yes":
[('2012-13', '16'), "Average Freshman Graduation Rate"],

"https://nces.ed.gov/programs/digest/d19/tables/dt19_221.40.asp?current=yes":
[('[Standard errors appear in parentheses]', '2019', '14'), "4th Grade Reading Scores"],


"https://nces.ed.gov/programs/digest/d19/tables/dt19_219.85b.asp?current=yes": 
[('[Standard errors appear in parentheses]', 'Total', '2'), 
"Percentage of HS Drop Outs Age 16-24"],

"https://nces.ed.gov/programs/digest/d19/tables/dt19_222.60.asp?current=yes":
[('[Standard errors appear in parentheses]', '2019', '14'), "8th Grade Math Scores"],

"https://nces.ed.gov/programs/digest/d19/tables/dt19_221.72.asp?current=yes":
[('[Standard errors appear in parentheses]', '8th-grade', 'Total', 'Total', '7'),
"8th Grade Reading Scores"],

"https://nces.ed.gov/programs/digest/d19/tables/dt19_222.50.asp?current=yes": 
[('[Standard errors appear in parentheses]', '2019', '13'),
"4th Grade Math Scores"], 

"https://nces.ed.gov/programs/digest/d19/tables/dt19_211.30.asp?current=yes":
[('[Standard errors appear in parentheses]', 'Current dollars', '2017-18',
 'Total', 'Total', '9'), "Average Base Teacher Salary w/ Bachelors"],

"https://nces.ed.gov/programs/digest/d19/tables/dt19_211.40.asp?current=yes":
[('[Standard errors appear in parentheses]', 'Current dollars', '2017-18',
 'Total', 'Total', '10'), "Average Base Teacher Salary w/ Masters"],

 "https://nces.ed.gov/programs/digest/d19/tables/dt19_211.60.asp?current=yes":
 [('Constant 2018-19 dollars1', 'Percentchange,1999-2000to2018-19', '16'), 
 "% Change in Teacher Salary 1999-2019"],

 "https://nces.ed.gov/programs/digest/d19/tables/dt19_211.60.asp?current=yes":
 [('Constant 2018-19 dollars1', '2018-19', '15'), "Overall Average Teacher Salary"],

 "https://nces.ed.gov/programs/digest/d20/tables/dt20_213.40.asp?current=yes":
 [('[In full-time equivalents]', 'Fall 2018', 'Teachers as a percent of staff',
 'Teachers as a percent of staff', 'Teachers as a percent of staff',
 'Teachers as a percent of staff', '17'), "Teacher Percentage of School Staff"],

"https://nces.ed.gov/programs/digest/d19/tables/dt19_214.30.asp?current=yes":
[('Total agencies', 'Total agencies', '2017-18', '3'), "Number of Education Agencies"],

"https://nces.ed.gov/programs/digest/d20/tables/dt20_216.90.asp?current=yes":
[('Charter schools as a percent of total public schools', '2017-18', '15'),
"% of Public Schools That Are Charters"],

"https://nces.ed.gov/programs/digest/d19/tables/dt19_219.46.asp?current=yes":
[('Total, ACGR for all students', '2017-18', '2017-18', '2017-18', '9'), 
"Adjusted Cohort Graduation Rate"]}

dfs = []
for thing1, thing2 in data.items():
    df = grab_frame(thing1)
    df = set_index(df)
    df = remove_footnotes(df)
    df = df[thing2[0]].to_frame()
    df.columns = [thing2[1]]
    dfs.append(df)

first_frame = dfs[0]
for i in range(1, len(dfs)):
    if i == 1:
        final = first_frame.join(dfs[i])
    else:
        final = final.join(dfs[i])

def remove_dollar(df):
    dol_cols = ['Average Base Teacher Salary w/ Bachelors',
    'Average Base Teacher Salary w/ Masters',
    'Overall Average Teacher Salary']

    for col in dol_cols:
        df[col] = df[col].str.replace(r"[$,]", '')
    return df

final = remove_dollar(final)


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



def replace_na(df):
    df = df.fillna(0)
    df = df.replace({'‡': 0, "#": 0})
    for col in df.columns:
        df[col].replace({0: df[col][0]}, inplace=True)
    return df




filled = replace_na(final)




def normalize(df):
    x = df.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df = pd.DataFrame(x_scaled)
    return df




