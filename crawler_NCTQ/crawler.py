# Starting from nctq state comparison homepage, crawls all policy
# databases and returns a dictionary mapping the year to a pandas 
# dataframe containing policy info per year. 
home_url = "https://www.nctq.org/yearbook/home"

import bs4
import csv
import urllib3
import certifi
import util
import queue
import re
import pandas as pd



grade_to_score_map = {"Best practice": 5, "Meets goal": 4, "Nearly meets goal": 3, 
                       "Meets goal in part": 2, "Meets a small part of goal": 1, 
                       "Does not meet goal": 0}


def crawl_one_page_nctq(soup, nctq_page_url, dic={}):
    policyname = soup.find("div", class_="page__head__content").findChildren()
    grades_list = soup.find_all("span", class_="grade__status")
    citation = soup.find("div", class_ = "suggestedCitation")

    if grades_list and citation:
        policyname = " (".join([tag.text for tag in policyname]) + ")"
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

        if not dic.get("nctq_{}".format(year)):
            dic["nctq_{}".format(year)] = {}
        if statescoredic:
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
        df_dic[year].to_csv(year + ".csv")
        
    #df.to_csv(csv_file_name, sep='\t')

    return df_dic


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




        



