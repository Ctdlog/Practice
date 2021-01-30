import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency


"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""

os.system("cls")
url = "https://www.iban.com/currency-codes"


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

# choice_1, choice_2 받아오기
def ask_1():
    global ask_1
    try:
        choice = int(input("\nWhere are you from? Choose a country by number.\n#: "))
        if choice > len(list) or choice < 0:
            print("Choose a number from the list.")
            ask_1()
        else:
            print(list[choice][0])
            ask_1 = list[choice][1]
            return ask_1
    except ValueError:
        print("That wasn't a number.")


def ask_2():
    global ask_2
    try:
        choice = int(input("\nNow choose another country.\n#: "))
        if choice > len(list) or choice < 0:
            print("Choose a number from the list.")
            ask_2()
        else:
            print(list[choice][0])
            ask_2 = list[choice][1]
            return ask_2
    except ValueError:
        print("That wasn't a number.")


# 환전 기능 함수
def convert(a, b, c):
    url = f"https://transferwise.com/gb/currency-converter/{a}-to-{b}-rate?amount={c}"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    currency = float(soup.find("span", {"class": "text-success"}).get_text())

    return c * currency


# 얼마나 환전할지 묻기
def how_many():
    ask_1()
    ask_2()
    try:
        amount = int(input(f"\nHow many {ask_1} do you want to convert to {ask_2}?\n"))
        after_convert = convert(ask_1, ask_2, amount)
        symbol = format_currency(after_convert, ask_2)
        print(f"{ask_1} {amount} is {symbol}")

    except ValueError:
        print("That wasn't a number.")
        how_many()


# 프로그램 실행
print("Welcome to CurrencyConvert PRO 2020\n")
for idx, country in enumerate(list):
    print(f"# {idx} {country[0]}")

how_many()