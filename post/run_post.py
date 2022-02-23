import requests
from bs4 import BeautifulSoup
from post.create_date_base import SQLApi
import configparser
import re

HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

TOP_ITEMS = 5
DOMAIN = "https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/"
config = configparser.ConfigParser()
config.read("config.ini")
login = config["VK"]["login"]
token = config["VK"]["token_vk"]
filter_apple = config["Filter"]["filter_apple"]


def get_html(url: str, params=None):
    return requests.get(url, headers=HEADERS, params=params)


def get_content(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all("div", attrs={"card"})
    products = []
    for item in items:
        if len(products) >= TOP_ITEMS:
            break
        url = item.find("a", attrs={"class": "card-images-wrapper"})['href']
        try:
            url_photo = DOMAIN + \
                        BeautifulSoup(get_html(url).text, "html.parser").find("img")["data-src-original"]
        except TypeError:
            continue
        title = item.find("meta", attrs={"itemprop": "name"})['content']
        if re.search(filter_apple, title, re.IGNORECASE):
            continue
        if re.search('noimage.svg', url_photo, re.IGNORECASE):
            continue
        price = item.find("div", attrs={"itemprop": "price"})['content']
        photo = requests.get(url_photo).content
        products.append({"title": title,
                         "price": price,
                         "url": url,
                         "url_photo": url_photo,
                         "photo": photo
                         })
        print(f'Продукт {title} добавлен')
    return products

def post_products(sity, filials, categoriess):
    sql = SQLApi()
    url = sql.get_url(sity, filials, categoriess)
    html = get_html(url)
    return get_content(html)
