import requests
from bs4 import BeautifulSoup
import json
headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif, image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "_ym_uid=1638699514337625668; _ym_d=1638699514; _ga=GA1.2.2009362315.1638699514; hl=ru; fl=ru; visited_articles=482464; _gid=GA1.2.1333547691.1640671089; habr_web_home=ARTICLES_LIST_ALL;_gads=ID=978cf60364407044-22eb85b911cd0038:T=1638699514:S=ALNI_MbDGfoGMbivYRF9DmBUv91pVyltaQ; _ym_isad=2",
            "Host": "habr.com",
            "If-None-Match": "W/'3b4fc-Cqbs+DkRkPNsMMkMZKinrLgs3zA'",
            "sec-ch-ua": "'Chromium';v='94', 'Yandex';v='21', ';Not A Brand';v='99' ",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.3.954 (beta) Yowser/2.5 Safari/537.36"
           }

with open('scratch.json', 'w') as f:
    json.dump(headers, f, indent=2)


KEYWORDS = {'Дизайн',"Web", 'Python', 'IT-инфраструктура', "Здоровье", "История IT", 'Карьера в IT-индустрии'}
habr_main = 'https://habr.com'
response = requests.get('https://habr.com/ru/all', headers=headers)
response.raise_for_status()
text = response.text
soup = BeautifulSoup(text, features='html.parser')
articles = soup.find_all('article')
number = 1
for article in articles:
    hubs = article.find_all('a', class_="tm-article-snippet__hubs-item-link")
    hubs = set(hub.find('span').text for hub in hubs)
    title = article.find('a', class_='tm-article-snippet__title-link')
    span_title = title.find('span').text
    date_article = article.find('span', class_='tm-article-snippet__datetime-published')
    if KEYWORDS & hubs:
        print(f"{number}.{date_article.find('time').get('title')} - {span_title} - {habr_main + title.get('href')}")
        number += 1