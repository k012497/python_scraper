import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python&sort=i"

def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  # print(soup)
  pages = soup.find('div', {'class':'s-pagination'}).find_all('a')
  last_page = pages[-2].find('span').get_text()
  return int(last_page)

def extract_job_on_page(html):
  title = html.find('h2', {'class':'fc-black-800'}).find('a')
  if(title is not None):
    title = title['title']

  # company_row = html.find('h3', {'class':'fc-black-700'})
  company, location = html.find('h3', {'class':'fc-black-700'}).find_all('span', recursive=False)
  # if(company_row is not None):

    # company = company_row.find_all('span')[0].get_text(strip=True)
    # location = company_row.find_all('span')[1].get_text(strip=True)
  return {'title' : title, 'company' : company.get_text(strip=True), 'location' : location.get_text(strip=True)}


def get_all_jobs(last_page):
  jobs = []
  for page in range(last_page):
    result = requests.get(f"{URL}&page ={page + 1}")
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all('div', {'class':'-job'})
    for result in results:
      job = extract_job_on_page(result)
      jobs.append(job)
      print(jobs)
    return jobs

def get_jobs_dictionary():
  last_page = get_last_page()
  jobs = get_all_jobs(last_page)
  return jobs
