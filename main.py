import requests
from bs4 import BeautifulSoup
import json
import make_json


def get_headers():
    make_json.dump_headers()
    with open('headers.json') as f:
        headers = json.load(f)
    return headers


def web_scraping(search_in: str):
    KEYWORDS = {'Дизайн',"Web", 'Python', 'IT-инфраструктура', "Здоровье", "История IT", 'Карьера в IT-индустрии'}
    habr_main = 'https://habr.com'

    headers = get_headers()

    response = requests.get('https://habr.com/ru/all', headers=headers)
    response.raise_for_status()
    text = response.text
    soup = BeautifulSoup(text, features='html.parser')
    articles = soup.find_all('article')
    number = 1
    for article in articles:
        hubs = article.find_all('a', class_="tm-article-snippet__hubs-item-link")
        title = article.find('a', class_='tm-article-snippet__title-link')
        date_article = article.find('span', class_='tm-article-snippet__datetime-published')
        preview = article.find('div', class_="tm-article-snippet").text.split()
        hubs = set(hub.find('span').text for hub in hubs)
        span_title = title.find('span').text
        date_title = date_article.find('time').get('title')
        if search_in == 'preview':
            if KEYWORDS.intersection(preview):
                print(f"{number}.{date_title} - {span_title} - {habr_main + title.get('href')}")
                number += 1
            elif article == articles[0]:  # Если нет пересечений, и для проверки актуальности получаемых статей
                print(f"NEW: {date_title} - {span_title} - {habr_main + title.get('href')}")
        elif search_in == 'tags':
            if KEYWORDS & hubs:
                print(f"{number}.{date_title} - {span_title} - {habr_main + title.get('href')}")
                number += 1


if __name__ == '__main__':
    web_scraping('preview')
