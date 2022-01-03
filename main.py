import requests
from bs4 import BeautifulSoup
import json
import make_json
from my_decorators import improve_decor


def get_headers():
    make_json.dump_headers()
    with open('headers.json') as f:
        headers = json.load(f)
    return headers


@improve_decor('log_file.txt')
def web_scraping(search_in: str):
    KEYWORDS = {'Дизайн', "Web", 'Python', 'IT-инфраструктура', "Здоровье", "История IT", 'Карьера в IT-индустрии',
                'SmartSpeech'}
    habr_main = 'https://habr.com'

    headers = get_headers()

    response = requests.get('https://habr.com/ru/all', headers=headers)
    # Не понимаю как здесь работают headers: если передать пустую строку - результат тот же
    response.raise_for_status()
    text = response.text
    soup = BeautifulSoup(text, features='html.parser')
    articles = soup.find_all('article')
    number = 1
    for article in articles:
        preview = article.find('div', class_="tm-article-snippet")
        if preview:
            preview = preview.text.split()
            hubs = article.find_all('a', class_="tm-article-snippet__hubs-item-link")
            title = article.find('a', class_='tm-article-snippet__title-link')
            href = title.get('href')
            date_tag = article.find('span', class_='tm-article-snippet__datetime-published')
            hubs = set(hub.find('span').text for hub in hubs)
            article_title = title.find('span').text
            date = date_tag.find('time').get('title')
        elif article.find('div', class_='tm-megapost-snippet') is not None:
            preview = article.find('div', class_='tm-megapost-snippet').text
            preview = preview.split()
            article_title = article.find('h2', class_='tm-megapost-snippet__title').text
            date = article.find('time').get('title')
            href = article.find('a', class_='tm-megapost-snippet__link tm-megapost-snippet__date').get('href')
            hubs = article.find_all('li', class_="tm-megapost-snippet__hub")
            hubs = set(hub.find('span').text for hub in hubs)
        else:
            continue
        if search_in == 'preview':
            if KEYWORDS.intersection(preview):
                print(f"{number}.{date} - {article_title} - {habr_main + href}")
                number += 1
            elif article == articles[0]:  # Если нет пересечений, и для проверки актуальности получаемых статей
                print(f"NEW: {date} - {article_title} - {habr_main + href}")
        elif search_in == 'tags':
            if KEYWORDS & hubs:
                print(f"{number}.{date} - {article_title} - {habr_main + href}")
                number += 1
        if search_in == 'full':
            response_article = requests.get(habr_main + href)
            text_article = response_article.text
            soup_article = BeautifulSoup(text_article, features='html.parser')
            content_tag = soup_article.find('article', class_="tm-article-presenter__content tm-article-presenter__content_narrow")
            if not content_tag:
                content_tag = soup_article.find('div', id='post-content-body')
                if not content_tag:
                    continue
            # try:
            #     article_text = content_tag.text
            # except AttributeError as error:
            #     content_tag = soup_article.find('div', id='post-content-body')
            #     print(error)
            article_text = content_tag.get_text().split()
            if KEYWORDS.intersection(article_text):
                print(f"{number}.{date} - {article_title} - {habr_main + href} ({KEYWORDS & set(article_text)})")
                number += 1


if __name__ == '__main__':
    print('Режимы поиска статей: по превью(default) - (1), по тегам - (2), по статье целиком - (3)')
    user_input = input('Режим: ')
    if user_input == '1':
        print('Статьи, найденные на Хабре по превью:')
        web_scraping('preview')
    elif user_input == '2':
        print('Статьи, найденные на Хабре по тегам:')
        web_scraping('tags')
    elif user_input == '3':
        print('Статьи, найденные на Хабре по просмотру всей статьи:')
        web_scraping('full')
    else:
        print('Статьи, найденные на Хабре по превью:')
        web_scraping('preview')
