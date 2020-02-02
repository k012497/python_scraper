import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=python&limit={LIMIT}&from=advancedsearch"

def extract_indeed_pages():
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


def extract_indeed_jobs(last_page):
  jobs = []
  # for page in range(last_page):
  result = requests.get(f"{URL}&start={0*LIMIT}")
  soup = BeautifulSoup(result.text, 'html.parser')
  results = soup.find_all('div', {'class' :'jobsearch-SerpJobCard'}) # list of html
  for result in results:
    title = result.find('div', {'class':'title'}).find('a')["title"]
    company = result.find('span', {'class':'company'}).string
    # print(title)
    if(company is not None):
      company = company[1:]
      jobs.append({"title" : title, "company" : company})

  print(jobs)
  return jobs