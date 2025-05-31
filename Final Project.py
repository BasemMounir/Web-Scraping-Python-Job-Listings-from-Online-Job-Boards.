# Web Scraping Python Job Listings from Online Job Boards

# install and import modules.
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

# create lists
job_title =[]
company_name = []
location_name = []
skills = []
links = []
salary = []

page_num = 0
#used requests to fetch the url
while True:
    try:
        result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_num}")

        source = result.content

        #create soup object to parse content
        soup = BeautifulSoup(source, "lxml")

        page_limit = int(soup.find("strong").text)
        if page_num > page_limit //15:
            print("pages ended, terminate")
            break
        #find the elements the containing the info we need.
        #job title, job skills, company name, location.

        job_titles = soup.find_all("h2", {"class":"css-m604qf"})
        company_names = soup.find_all("a", {"class":"css-17s97q8"})
        locations_names = soup.find_all("span", {"class":"css-5wys0k"})
        job_skills = soup.find_all("div", {"class":"css-y4udm8"})


        #loop over returned lists to extract the need info into other lists.
        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text)
            links.append(job_titles[i].find("a").attrs['href'])
            company_name.append(company_names[i].text)
            location_name.append(locations_names[i].text)
            skills.append(job_skills[i].text)

        page_num += 1
        print("page switched")
    except Exception as e:
        print(f"Error occurred: {e}")
        break

#extract salary from links
for link in links:
    result = requests.get(link)
    source = result.content
    soup = BeautifulSoup(source, 'lxml')
    salaries = soup.find("span", {"class": "css-4xky9y"})
    salary.append(salaries.text.strip() if salaries else "Not Available")

#creat CSV file and fill with the values
file_list = [job_title, company_name, location_name,skills, links, salary]
exported = zip_longest(*file_list)          #combines multiple iterables

with open("jobtest.csv", "w", newline='', encoding='utf-8') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["job tile", "company name", "location", "job skills", "links", "salary"])
    wr.writerows(exported)
