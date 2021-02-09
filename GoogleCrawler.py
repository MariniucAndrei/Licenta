import json
import urllib
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import csv

def func():
    results = {}
    index = 1
    terms = []
    domains = []
    with open('query.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            terms.append(row["Termen"])
            domains.append(row["Domeniu"])

    for it in range(len(terms)):
        query = terms[it]
        query = query.replace(' ', '+')
        URL = 'https://www.google.com/search?q={}&num={}&hl={}'.format(
            query, 1, 'en')

        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

        headers = {"user-agent": USER_AGENT}
        resp = requests.get(URL, headers=headers)
        print(resp.status_code)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            for rc_item in soup.find_all('div', class_='g'):
                title = rc_item.find('h3').text
                if rc_item.find('div', class_='TbwUpd NJjxre').text:
                    link = rc_item.find('div', class_='TbwUpd NJjxre').text
                else:
                    link = "None"
                description = rc_item.find('span').text
                if rc_item.find('span', class_='f') != -1:
                    date = str(rc_item.find('span', class_='f'))
                    date = date.replace("<span class=\"f\">", "")
                    date = date.replace(" - </span>", "")
                    if date.__contains__("days ago"):
                        today = datetime.today() + timedelta(int(date[0]))
                        d2 = today.strftime("%B %d, %Y")
                        date = str(d2)
                    elif date.__contains__("hours ago"):
                        today = datetime.today()
                        d2 = today.strftime("%B %d, %Y")
                        date = str(d2)
                else:
                    date = "undefined"
                item = {
                    "title": title,
                    "link": link,
                    "description": description,
                    "date": date,
                    "searched_by": terms[it],
                    "domain": domains[it]
                    }
                results.update({str(index): item})
                index = index + 1
        jsonObject = json.dumps(results, indent=4)
        # for item in jsonObject:
        with open("site-uri_utile.json", "w") as outputfile:
            outputfile.write(jsonObject)


    print(results)

if __name__ == '__main__':
    func()