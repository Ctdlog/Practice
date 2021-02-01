import os
import csv
import requests
from bs4 import BeautifulSoup
from requests.api import request

os.system("cls")
alba_url = "http://www.alba.co.kr"

# place, title, time, pay, date
# ex) 인천 미추홀, 노랑통닭 금호점, 16:00~02:30, "월급2,300,000", 22분전


result = requests.get(alba_url)
soup = BeautifulSoup(result.text, "html.parser")
brand = soup.find("div", {"id": "MainSuperBrand"})
boxes = brand.find_all("li", {"class": "impact"})
names = brand.find_all("span", {"class": "company"})

urls = []
names = []


for box in boxes:
    url = box.find("a")["href"]
    urls.append(url)
    name = box.find("span", {"class": "company"}).text
    names.append(name)


def extract_jobs(url):
    jobs = []
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    rows = soup.find("tbody").find_all("tr")
    for row in rows[::2]:
        try:
            place = row.find("td", {"class": "local"}).text
            place = place.replace("\xa0", " ")
            title = row.find("span", {"class": "company"}).text
            time = row.find("td", {"class": "data"}).text
            pay = row.find("td", {"class": "pay"}).text
            date = row.find("td", {"class": "regDate"}).text
            job = {
                "place": place,
                "title": title,
                "time": time,
                "pay": pay,
                "date": date,
            }

            jobs.append(job)

        except:
            continue

    return jobs


def save_to_file(name, jobs):
    name = name.replace("/", "&")
    print(f"Scrapping job: {name}")
    file = open(f"{name}.csv", mode="w", encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(["place", "title", "time", "pay", "date"])
    for job in jobs:
        try:
            writer.writerow(list(job.values()))
        except:
            pass


for i in range(0, len(urls)):
    jobs = extract_jobs(urls[i])
    save_to_file(names[i], jobs)
