import requests
from bs4 import BeautifulSoup
import json
import make_json
# import tqdm


def get_headers():
    make_json.dump_headers()
    with open('headers.json') as f:
        headers = json.load(f)
    return headers


def web_scraping(search_in: str):
    KEYWORDS = {'Дизайн', "Web", 'Python', 'IT-инфраструктура', "Здоровье", "История IT", 'Карьера в IT-индустрии'}
    habr_main = 'https://habr.com'

    headers = get_headers()

    response = requests.get('https://habr.com/ru/all', headers=headers)
    # Не понимаю как здесь работают headers: если передать пустую строку - результат тот же
    response.raise_for_status()
    text = response.text
    soup = BeautifulSoup(text, features='html.parser')
    articles = soup.find_all('article')
    number = 1
    for article in articles:  # Здесь был tqdm
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
        if search_in == 'full':
            article_href = title.get('href')
            response_article = requests.get(habr_main + article_href)
            text_article = response_article.text
            soup_article = BeautifulSoup(text_article, features='html.parser')
            content_tag = soup_article.find('article', class_="tm-article-presenter__content tm-article-presenter__content_narrow")
            article_text = content_tag.get_text()
            article_text_split = article_text.split()
            if KEYWORDS.intersection(article_text_split):
                print(f"{number}.{date_title} - {span_title} - {habr_main + article_href}")
                number += 1


if __name__ == '__main__':
    print('Режимы поиска статей: по превью(default) - (1), по тегам - (2), по статье целиком - (3)')
    user_input = input('Режим: ')
    if user_input == '1':
        print('Статьи, найденные на Хабре по превью:')
        web_scraping('preview')
    elif user_input == '2':
        print('Статьи, найденные на Хабре по тэгам:')
        web_scraping('tags')
    elif user_input == '3':
        print('Статьи, найденные на Хабре по просмотру всей статьи:')
        web_scraping('full')
    else:
        print('Статьи, найденные на Хабре по превью:')
        web_scraping('preview')
