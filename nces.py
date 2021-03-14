# National Center for Education Statistics (nces) website crawler

import requests
import bs4
import pandas as pd
import numpy as np
import re
from sklearn import preprocessing 
import scipy
import os
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# This file "crawls" through a series of National Center for Education Statistics
# links and extracts relevant information from them to a couple of pandas dataframes
# that form the basis for much of our analysis. Each nces page has a table that is
# trivial to read into a pandas df, which we then extracted the relevant columns from.
# The difficulty of making this "crawler" is that the relevant data on pages we 
# selected appeared in really random locations. Originally, the plan with this file 
# was to write a series of generalizable functions that would perform tasks like 
# extracting the first column, the last column, or a range of columns, and performed
# various tasks to simplify the dataframe, properly set its index, and remove
# extraneous columns. Unfortunately, the locations of relevant data proved too random
# for functions to extract the relevant data without a data structure providing
# information about the relevant columns, which is what is located below.



# data structure: {link: [(index value of relevant column, column header)]}

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


# data2 structure: {link: (boolean stating whether or not the chart has standard
# error values that need to be removed, range of columns to extract, MultiIndex
# index of year, column header (which the year is added to))}

data2 = {"https://nces.ed.gov/programs/digest/d19/tables/dt19_219.35.asp?current=yes":
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


# This section contains the functions that perform essential functions for 
# extracting the dataframes and making them usable to eventually be able to 
# combine them.

def grab_frame(site):
    '''
    Grabs the table from an nces link and reads it into a pandas df.

    Inputs: site (str): link to nces website

    Output: frame(pandas df): the dataframe
    '''
    frame = pd.read_html(site, attrs = {"class" : 
    "tableMain"})[0]
    return frame


def set_index(df):
    '''
    Sets the index of a dataframe to be the values in its first column. Prior to
    doing this, it drops all index values that have rows full of na values in
    front of them (which many raw nces tables have).

    Inputs: df (pandas df): nces data

    Output: df: edited version of df
    '''
    df = df.dropna(how = 'all')
    top_left = df.columns.values[0]
    df = df.set_index(top_left)
    return df
    


def remove_footnotes(df):
    '''
    Many nces dfs' states values contain footnote numbers at the end of each
    string. This proves a problem when trying to join dfs later. This function
    iterates through a list of the index of a df and utilizes a regular
    expression to ensure no extraneous values are present in index names.

    Input: df (pandas df)

    Output: df (pandas df): edited df with corrected index values
    '''

    index = df.index.tolist()
    for i in range(len(index)):
        new = (re.sub(r'[0-9,]*', "", index[i]))
        index[i] = new
    df.index = index
    return df


def drop_se(df):
    '''
    Some nces tables contain standard error values for each data point. Utilizing
    these values was beyond the statistical scope of this project, and as such,
    we removed these values from tables when we were trying to extract a range
    of columns. This function exploits the fact that in nces tables, the final
    value in the MultiIndex header of tables is the number of the column. In tables
    with standard errors the values for the first column would be in column number
    1, but it's standard error values would be in column 1.1 (2, 2.1 and so on). 
    This made it simple to iterate through the column numbers and drop any MultiIndex 
    values where the column number had a decimal in it.

    Input: df

    Output: df (with standard error columns removed)
    '''
    cols = df.columns
    index = len(cols[0]) - 1
    drops = []
    for col in cols:
        if "." in col[index]:
            drops.append(col)
    df.drop(columns=drops, inplace=True)

def last_col(df):
    '''
    Returns a single column dataframe with just the last column of the input frame.
    Not utilized anywhere in this program.

    Input: df

    Output: new (df with just one column)
    '''
    last_col = len(df.columns) - 1
    new = df[[df.columns[last_col]]].copy()
    return new

def first_col(df):
    '''
    Returns a single column dataframe with just the first column of the input frame.
    Not utilized anywhere in this program.

    Input: df

    Output: new (df with just one column)
    '''
    new = df[[df.columns[0]]].copy()
    return new

def replace_na(df):
    '''
    Some of the data we extracted had values that were not filled in. This proved
    quite problematic for our later analysis, so our patchwork solution to this
    was to replace na values with the US average. This function does that.

    Input: df

    Output: df (with na values filled in w/ US averages)
    '''
    df = df.replace({'‡': None, "#": None, "—": None, "---": None})
    df = df.fillna(df.iloc[0])
    return df


def remove_dollar(df):
    '''
    The dfs we extracted with $ values proved tricky because pandas was unable
    to convert values like "$12,345" to an int or float. This function iterates
    through the columns in a df and utilizes a regular expression to remove
    $ and , from the data.

    Input: df

    Output: df (with $ and , removed)
    '''
    for col in df.columns:
        df[col] = df[col].astype(str)
        df[col] = df[col].str.replace(r"[$,]", '')
    return df

def df_crawl1(df_dict):
    '''
    This function is designed to crawl through the links in the data1 dictionary.
    It goes to each key, value pair, extracts the frame from the key, sets the
    index and removes footnotes, names the columns, appends the df to a list
    and returns a list of the resulting dataframes.

    Input: df_dict (specially designed dictionary called data1)

    Output: frames (list of dfs)
    '''
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
    '''
    This function crawls through the links in the data2 dictionary. It grabs the
    frame, sets the index to the states, removes footnotes, drops standard error
    values if ncessary, and then iterates through all the columns in the specified
    range in the dict. As it creates new frames, it goes to the index value
    in the MultiIndex where the year value is located and combines the year
    value with the specified column header name before appending each resulting
    dataframe to a list of dataframes.

    Input: df_dict (specifically designed to call data2)

    Output: dfs (list of dfs)
    ''' 
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




# Here we create our lists of dataframes and do some fixes to them. The DC data
# needed to be manually fixed because it had na values followe by very low numeric
# values. Later we calculate "trends" and when these values got filled in with
# US averages, the trend values ended up as a heavy outlier, so we correct for
# that here. We also utilize remove_dollar to correct dfs with $ values in them.


dfs1 = df_crawl1(data)
dfs1[1].loc['District of Columbia'] = [0, 0 , 0.1, 0.1]
dfs1[4] = remove_dollar(dfs1[4])
dfs1[5] = remove_dollar(dfs1[5])
dfs2 = df_crawl2(data2)
dfs2[4] = remove_dollar(dfs2[4])

def fill_means(dfs):
    '''
    This function iterates through all dataframes created and fills in all na
    values with mean values. This ends up only affecting a few columns that did
    not have us averages as a result of the original df not having these values.

    Input: dfs (list of dfs)

    Output: None (modifies dfs in place)
    '''
    for df in dfs:
        df.fillna(df.mean(), inplace=True)

fill_means(dfs1)
fill_means(dfs2)

def join_dfs(dfs):
    '''
    This function takes in a list of dataframes and joins them all together
    into one happy frame.

    Input: dfs (list of dfs)

    Output: df (df with values from all dfs in list)
    '''
    first_frame = dfs[0]
    for i in range(1, len(dfs)):
        if i == 1:
            df = first_frame.join(dfs[i])
        else:
            df = df.join(dfs[i])
    return df

raw = join_dfs(dfs1).join(join_dfs(dfs2))



def normalize(df):
    '''
    Function to normalize values in a dataframe. It goes into each column, picks
    out the min and max values, and then assigns each other value in the column
    a value based off of where it is relative to the min and max values (halfway
    between min and max = 0.5). We then put this value into a 0-100 scale, rather
    than 0-1 because later on in our analysis, we performed multiplication where
    wanted values to increase, so it was of value to us to make values > 1 (typically).

    Input: df (df)

    Output: normalized (df with normalized values)

    Adapted from: https://stackoverflow.com/questions/26414913/normalize-columns-of-pandas-data-frame
    '''

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
    '''
    This function takes in a row of data and outputs a value of the average of
    percent changes in values between observed points. This function is utilized
    to create trend columns.

    Input: row (df row)

    Output: avg (float)
    '''
    slopes = []
    for i in range(1, len(row)):
        if row[i - 1] == 0:
            continue
        else:
            slope = (row[i] - row[i-1]) / row[i - 1]
            slope *= 100
            slopes.append(slope)
    if len(slopes) > 0:
        avg = sum(slopes) / len(slopes)
    else:
        avg = 0
    return avg


def add_slope(df):
    '''
    This function applies the above get_slope function to a dataframe and returns
    a single column dataframe with the Trend values.

    Input: df

    Output: trend(single column df)
    '''
    col_name = "Trend: " + df.columns[0][5:]
    trend = df.apply(get_slope, axis=1).to_frame(name=col_name)
    return trend


def final_frame(dfs):
    '''
    This function performs the final operations of normalizing the raw data from
    nces and calculating trend values based off of the raw data. It joins all these
    values together into one dataframe, appends those edited frames to a list,
    and then utilizes the join_dfs function to merge all dfs in the list into one.

    Input: dfs (list of dfs)

    Output: final (df)
    '''
    final_dfs = []
    for df in dfs:
        if len(df.columns) == 1:
            df = normalize(df)
            final_dfs.append(df)
        else:
            df = df.astype(float)
            trend = add_slope(df)
            df = normalize(df)
            df = df.join(trend)
            final_dfs.append(df)
    final = join_dfs(final_dfs)
    return final


#Here we do a few final house keeping matters. We run final_frame on both lists
# frames and join them together.

final = final_frame(dfs1).join(final_frame(dfs2))


# Here we subtract 100 from every states HS drop outs statistic. We wanted positive
# values to generally be associated with better outcomes. And this was the
# main statistic we had where higher values were clearly bad.

final["2018 Percentage of HS Drop Outs Age 16-24"] = 100 - final["2018 Percentage of HS Drop Outs Age 16-24"]

# Our other crawler had index values of US state abbreviations. We place a
# dict here to use to change the value of the index immediately afterwards.

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

# Here we change the index to abbreviations, ensure that all na values are in,
# and round all values to 3 digits.
final.rename(index=us_state_abbrev, inplace=True)
final.fillna(final.mean(), inplace=True)
final = final.round(3)


# Finally, we load our data into two csv files.
raw.to_csv("csv/nces_raw.csv")
final.to_csv("csv/nces_final.csv")


