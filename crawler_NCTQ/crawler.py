import bs4
import csv
import urllib3
import certifi
import util
import queue
import pandas as pd

def crawl_one_page_nctq(soup, nctq_page_url, dic={}):
    #soup = make_soup(nctq_page_url)
    if soup: 
        try:

            policyname = soup.find("section", class_="section-goals")
            policyname = policyname.find("h2").text

            statescoredic = {}
            tag_list = soup.find_all("span", class_="grade__status")
            grade_to_score_map = {"Best practice": 5, "Meets goal": 4, "Nearly meets goal": 3, 
                                    "Meets goal in part": 2, "Meets a small part of goal": 1, 
                                    "Does not meet goal": 0}
            for state_policy in tag_list:
                policyscoretext = state_policy.text
                while state_policy.name != "ul":
                    state_policy = state_policy.next_sibling
                policyscore = grade_to_score_map.get(policyscoretext)
                states = state_policy.find_all("li")
                for state in states:
                    statescoredic[state.text] = policyscore

            if statescoredic and policyname:
                dic[policyname] = statescoredic
                print(nctq_page_url, "succeeded")
        except:
            print(nctq_page_url, "failed")


def crawl_nctq(source_url):
    limiting_domain = "nctq.org"
    source_soup = make_soup(source_url)
    url_lst = linked_urls(source_url, source_soup)
    print(url_lst)
    visited_urls = set()
    nctq = {}

    for url in url_lst:
        if util.is_url_ok_to_follow(url, limiting_domain) and \
           url not in visited_urls:

            soup = make_soup(url)
            visited_urls.update(url)
            crawl_one_page_nctq(soup, url, nctq)
    
    df = pd.DataFrame(nctq)
    df.to_csv("empty.csv", sep='\t')

    return df


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
        print("reading", myurl, "failed")
    
    return soup


"""
def make_soup(url):
    '''
    Given a url, return the soup object and request object of this url

    Input: url (a string)
    Output: the soup object and request object
    '''
    request = util.get_request(url)
    if request:
        text = util.read_request(request)
        soup = bs4.BeautifulSoup(text, 'html5lib')
        
    return soup, request
"""      


"""
    with open(index_filename, mode="w") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter = ",")
        for key in sorted(statescoredic):
            csv_writer.writerow([key, statescoredic[key]])
"""

        



