import requests
import os


def check():
    # Intro
    while True:
        print("Welcome to IsItDown.py!")
        URLS = (
            input(
                "Please write a URL or URLs you want to check. (seperated by comma)\n"
            )
            .strip()
            .split(",")
        )

        # URL 반복문 실행
        for URL in URLS:
            URL = URL.strip().lower()
            if ".com" not in URL:
                print(f"{URL} is not valid URL.")

            else:
                if "http://" not in URL:
                    URL = "http://" + URL
                try:
                    r = requests.get(URL)
                    if r.status_code == 200:
                        print(f"{URL} is up!")
                except:
                    print(f"{URL} is down!")

        # 재실행 여부 묻기
        while True:
            restart = input("Do you want to start over? y/n ")
            if restart == "y":
                print("restart!")
                break
            elif restart == "n":
                return "OK, bye!"
            else:
                print("That's not valid answer.")

        # windows 콘솔 초기화
        os.system("cls")

        # linux, mac 에서는 os.system('clear') 사용


# check 함수 실행
print(check())