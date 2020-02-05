import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=python&limit={LIMIT}&from=advancedsearch"

def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, 'html.parser')

  pagination = soup.find('div', {"class":"pagination"})

  links = pagination.find_all('a')
  pages = []

  # 마지막 인덱스의 '다음'을 제외하고 string값을 int로 가져오기
  for link in links[0:-1]:
    # pages.append(link.find("span").string)
    pages.append(int(link.string))

  max_page = pages[-1] #마지막 페이지

  return max_page

def extract_job_on_page(html):
  title = html.find('div', {'class':'title'}).find('a')["title"]
  company = html.find('span', {'class':'company'})
  company_anchor = company.find("a")

  if(company_anchor is not None):
    company = str(company_anchor.string[1:])
  else:
    company = str(company.string).strip()
  
  # location = html.find('span', {'class':'location'}).string
  location = html.find('div', {'class':'recJobLoc'})["data-rc-loc"]

  job_id = html["data-jk"]

  return {'title' : title, 'company' : company, 'location' : location, 'link' : f"https://kr.indeed.com/viewjob?jk={job_id}"}


def get_all_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"SCRAPPING INDEED PAGE {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all('div', {'class' :'jobsearch-SerpJobCard'}) # list of html
    for result in results:
      job = extract_job_on_page(result)
      jobs.append(job)
  return jobs

def get_jobs_dictionary():
  last_page = get_last_page()
  jobs = get_all_jobs(last_page)

  return jobs
