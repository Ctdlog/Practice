import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request


"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django",
]


db = {}
app = Flask("DayEleven")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/read")
def read():
    args = list(request.args)
    lists = []
    for arg in args:
        print(f"{arg} requesting..")
        url = f"https://www.reddit.com/r/{arg}/top/?t=month"
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        results = soup.find_all("div", {"class": "_1oQyIsiPHYt6nx7VOmd1sz"})
        for result in results:
            # 중간에 광고로 나오는 post 제거
            promoted = result.find("span", {"class": "_2oEYZXchPfHwcf9mTMGMg8"})
            if promoted:
                pass
            else:
                title = result.find("h3").text
                link = result.find("a")["href"]
                language = soup.find("h2", {"class": "_33aRtz9JtW0dIrBNKFAl0y"}).text
                votes = result.find("div", {"class": "_25IkBM0rRUqWX5ZojEMAFQ"}).text
                if "k" in votes:
                    votes = votes.replace("k", "000").replace(".", "")
                votes = int(votes)
                info = {
                    "title": title,
                    "link": link,
                    "votes": votes,
                    "language": language,
                }
                lists.append(info)

    # vote 숫자가 큰 순서대로 정렬하기
    lists = sorted(lists, key=lambda list: list["votes"], reverse=True)
    return render_template("read.html", args=args, lists=lists)


app.run(host="127.0.0.1")
