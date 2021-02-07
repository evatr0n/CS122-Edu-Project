import bs4
import csv
html = open(input("HTML_filename: ")).read()
index_filename = input("empty csv file name: ")
soup = bs4.BeautifulSoup(html, features="lxml")
tag_list = soup.find_all("span", class_="grade__status")


statescoredic = {}
for state_policy in tag_list:
    policyscoretext = state_policy.text
    while state_policy.name != "ul":
        state_policy = state_policy.next_sibling
    if policyscoretext == "Best practice":
        policyscore = 5
    elif policyscoretext == "Meets goal":
        policyscore = 4
    elif policyscoretext == "Nearly meets goal":
        policyscore = 3
    elif policyscoretext == "Meets goal in part":
        policyscore = 2
    elif policyscoretext == "Meets a small part of goal":
        policyscore = 1
    elif policyscoretext == "Does not meet goal":
        policyscore = 0

    states = state_policy.find_all("li")
    for state in states:
        statescoredic[state.text] = policyscore

with open(index_filename, mode="w") as csvfile:
    csv_writer = csv.writer(csvfile, delimiter = ",")
    for key in sorted(statescoredic):
        csv_writer.writerow([key, statescoredic[key]])
    
        



