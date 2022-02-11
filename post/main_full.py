# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import random
from create_date_base import SQLApi
from vk_api_pobeda import VKApi
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

def get_html(url: str, params=None):
    return requests.get(url, headers=HEADERS, params=params)

def get_content(html, update,):
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
        if re.search(config.filter, title, re.IGNORECASE):
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
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Продукт {title} добавлен c ценой {price}')
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
    return products


def main(update, context):
    # Initialize SQLApi
    sql_api = SQLApi()
    # Initialize VKApi
    vk_api = VKApi(config)
    html = get_html(random.choice(config.link))
    if html.status_code != 200:
        print("Error conect")

    web_products = get_content(html, update, context)
    sql_api.insert_products(web_products)
    products = sql_api.get_images()

    photos = [product['image'] for product in products]
    captions = [
        f"{product['title']} \n  Цена: {product['price']} руб\n Ссылка на товар на нашем сайте: {product['url']}"
        for product in products]
    album_id = vk_api.get_album_id()
    vk_api.post_group_wall(photos, captions, album_id=album_id)


