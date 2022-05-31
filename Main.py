import json
import time
import requests
from bs4 import BeautifulSoup
import datetime
import csv



start_time = time.time()


def get_data():
   
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
    }

    url = "https://www.olx.pl/d/nieruchomosci/stancje-pokoje/krakow/q-pokoj/"

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    pages_count = soup.find_all("ul", {"class":"pagination-list"},"pagination-list-item")

    rooms_data = []
    #for page in range(1, pages_count + 1):
    for page in range(1, 2):
        url = "https://www.olx.pl/d/nieruchomosci/stancje-pokoje/krakow/q-pokoj/?page={page}"
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        rooms = soup.find("div",class_="listing-grid-container css-qdhg7u").find_all("div",class_="css-19ucd76")

        for bi in rooms:
            room_data = bi.find_all("div")

            try:
                room_title = room_data[0].find("h6").text.strip()
            except:
                room_title = "нет названия"

            try:
                price = room_data[0].find("p").text.strip()

            except:
                price = "no price"

            try:
                link = bi.find("a")['href']

            except:
                link = "no link"

            # print(room_title)
            # print(price)
            # print(link)
            # print("###" * 10)

            rooms_data.append(
                {
                "room_title": room_title,
                "price": price,
                "link": link,

                }
            )

            with open(f"rooms_{cur_time}.csv", "a", encoding="utf-8")as csv_file:
                writer = csv.writer(csv_file, delimiter=',')

                writer.writerow(
                    (
                        room_title,
                        price,
                        link
                    )
                )
        print(f"{page}")#/{pages_count}")
        time.sleep(1)

    with open(f"rooms_{cur_time}.json", "w", encoding="utf-8") as file:
        json.dump(rooms_data,file,indent=4, ensure_ascii=False)


def main():
    get_data()
    #finish_time = time.time() - start_time
    #print(f"{finish_time}")

if __name__ == '__main__':
    main()
