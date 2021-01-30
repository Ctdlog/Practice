import os
import requests
from bs4 import BeautifulSoup

os.system("cls")
url = "https://www.iban.com/currency-codes"

# Intro
print("Hello! Please choose select a country by number!")

# country, code list 만들기
result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")
rows = soup.find("tbody").find_all("tr")
list = []
for row in rows:
    data = row.find_all("td")
    country = data[0].text
    code = data[2].text
    # code 없는 row 삭제하기
    if code == "":
        continue
    else:
        list.append((country, code))

print(list[0][0])

# index, country list 나열하기
for idx, country in enumerate(list):
    print(f"# {idx} {country[0]}")

# input 받아서 결과 보여주기
while True:
    try:
        answer = int(input("#: "))
        if answer > len(list):
            print("Choose a number from the list.")
        else:
            print("You choose", list[answer][0])
            print("The currency code is", list[answer][1])
            break
    except:
        print("That wasn't a number.")
