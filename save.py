import csv

def save_to_file(jobs):
  # create file
  file = open("jobs.csv", mode="w") # only to write
  writer = csv.writer(file);
  writer.writerow(["title", "company", "location", "link"]); # title
  for job in jobs:
    writer.writerow(list(job.values()));

  return
