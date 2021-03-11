# Starting from nctq state comparison homepage, crawls all policy
# databases and returns a dictionary mapping the year to a pandas 
# dataframe containing policy info per year. 
# To get dataframes, run crawler() in terminal.
home_url = "https://www.nctq.org/yearbook/home"

import bs4
import csv
import urllib3
import certifi
import util
import queue
import re
import pandas as pd
import numbers



grade_to_score_map = {"Best practice": 6, "Meets goal": 5, "Nearly meets goal": 4, 
                       "Meets goal in part": 3, "Meets a small part of goal": 2, 
                       "Does not meet goal": 1}


def crawl_one_page_nctq(soup, nctq_page_url, dic={}):
    policyname = soup.find("div", class_="page__head__content").findChildren()
    grades_list = soup.find_all("span", class_="grade__status")
    citation = soup.find("div", class_ = "suggestedCitation")

    if grades_list and citation:
        policyname = " (".join([tag.text for tag in policyname]) + ")"
        policyname = " ".join(policyname.split())  # treats for inconsistent spacing
        year = int(re.findall("\((\d+)\)", citation.text)[0]) #get year collected from citation info
        statescoredic = {}
        total_score = 0
        num_states = 0
        
        for grade_category in grades_list:  # goes through each grade category and states in each category
            qual_score = grade_category.text
            quant_score = grade_to_score_map.get(qual_score)
            while grade_category.name != "ul":
                grade_category = grade_category.next_sibling
            
            states = grade_category.find_all("li")
            for state in states:
                statescoredic[state.text] = quant_score
                total_score += quant_score
                num_states += 1

        dic["nctq_{}".format(year)] = dic.get("nctq_{}".format(year), {})
        statescoredic["US"] = round(total_score / num_states, 2)
        dic["nctq_{}".format(year)][policyname] = statescoredic 
        print(year, nctq_page_url, "read")

    else:
        print(nctq_page_url, "UNABLE TO READ")


def crawl_nctq(source_url=home_url):
    limiting_domain = "nctq.org"
    prefix = "https://www.nctq.org/yearbook/national"
    source_soup = make_soup(source_url)
    url_lst = linked_urls(source_url, source_soup)
    visited_urls = set()
    nctq = {}
    df_dic = {}

    for url in url_lst:
        if util.is_url_ok_to_follow(url, limiting_domain) and \
            url not in visited_urls and prefix in url:
            soup = make_soup(url)
            if soup:
                crawl_one_page_nctq(soup, url, nctq)
        visited_urls.add(url)

    #df_dic = {year: pd.DataFrame(data) for year, data in nctq.items()}
    
    for year, data in nctq.items():
        df_dic[year] = pd.DataFrame(data)
        df_dic[year].to_csv("csv/{}.csv".format(year))
        
    #df.to_csv(csv_file_name, sep='\t')

    return df_dic   


def fill_na(df_dic):
    '''
    Takes pandas dataframe mapping years to policy scores and returns 
    a copy of the dataframe with its NaN values filled in with the 
    US average. By copying, it preserves the original dataframe. 
    Use this when conducting calculations with nonaveraged policy score 
    data by year. 
    Inputs:
      df_dic: pandas dataframe produced by crawl_nctq
    Outputs:
      dfdic_filled: dictionary mapping years("nctq_{year}") to dataframes with
                    filled NaN values. 
    '''
    dfdic_filled = {}
    for key, value in df_dic.items():
        dfdic_filled[key] = value.copy()
        dfdic_filled[key].fillna(dfdic_filled[key].loc["US"], inplace=True)
    
    return dfdic_filled


def average_df(dfdic_filled):
    '''
    Takes output of fill_na, a pandas dataframe with all NaN values filled,
    and computes one dataframe where policyscores are averaged over the 
    years. Many of the NCTQ data for policy has data from different years, 
    and these data points will be averaged to show mid to long term 
    policy performance per state. 
    Inputs:
      dfdic_filled: pd dataframe, no NaN
    Outputs:
      df_average = one dataframe with average scores per policy category.
                   used for default computation. 
    '''

    df_average = pd.concat([value for value in dfdic_filled.values()], axis = 1)
    df_average = df_average.groupby(by=df_average.columns, axis=1)
    df_average = df_average.apply(lambda g: g.mean(axis=1) \
                 if isinstance(g.iloc[0,0], numbers.Number) else g.iloc[:,0])
    df_average.to_csv("csv/average_scores.csv")
    
    return df_average


def linked_urls(source_url, soup):
    '''
    Inputs:
        soup: Soup object
        queue: queue object
    Outputs:
        links: queue object containing all of the links in order
    '''
    url_lst = []
    for link in soup.find_all('a'):
        if link.has_attr("href"):
            relative_url = link['href']
            linked_url = util.convert_if_relative_url(source_url, relative_url)
            filtered_link = util.remove_fragment(linked_url)
            url_lst.append(filtered_link)

    return url_lst


def make_soup(myurl):
    if util.is_absolute_url(myurl):
        try: 
            pm = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())
            html = pm.urlopen(url=myurl, method="GET").data
            soup = bs4.BeautifulSoup(html, features="lxml")
        except Exception:
            soup = None
    else:
        soup = None
    
    return soup




        



