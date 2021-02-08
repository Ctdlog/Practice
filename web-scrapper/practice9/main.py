import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
app = Flask("DayEleven")


def extract_so(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("div", {"class": "grid"})
    so_jobs = []
    for result in results:
        try:
            title = result.find("h2", {"class": "mb4"}).text
            company = result.find("h3").find("span").text.strip()
            link = result.find("a")["href"]
            job = {
                "title": title,
                "company": company,
                "link": link,
            }
            so_jobs.append(job)
        except:
            pass
    print("so")
    return so_jobs


extract_so("https://stackoverflow.com/jobs?r=true&q=python")


def extract_ww(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("li", {"class": "feature"})
    ww_jobs = []
    for result in results:
        try:
            title = result.find("span", {"class": "title"}).text
            company = result.find("span", {"class": "company"}).text
            link = result.find("a")["href"]
            job = {
                "title": title,
                "company": company,
                "link": link,
            }
            ww_jobs.append(job)
        except:
            pass
    print("ww")
    return ww_jobs


def extract_rm(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("tr", {"class": "job"})
    rm_jobs = []
    for result in results:
        try:
            title = result.find("h2", {"itemprop": "title"}).text
            company = result.find("h3", {"itemprop": "title"}).text
            link = result.find("a", {"class": "preventLink"})["href"]
            job = {
                "title": title,
                "company": company,
                "link": link,
            }
            rm_jobs.append(job)
        except:
            pass
    print("rm")
    return rm_jobs


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def detail():
    result = request.args.get("term")
    result = result.lower()
    so_url = f"https://stackoverflow.com/jobs?r=true&q={result}"
    ww_url = f"https://weworkremotely.com/remote-jobs/search?term={result}"
    rm_url = f"https://remoteok.io/remote-dev+{result}-jobs"
    jobs = extract_so(so_url) + extract_ww(ww_url) + extract_rm(rm_url)
    num_jobs = len(jobs)
    print(jobs)
    return render_template("search.html", result=result, jobs=jobs, num_jobs=num_jobs)


app.run(host="127.0.0.1")