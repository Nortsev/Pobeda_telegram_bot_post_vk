import requests
import os
import shutil
from bs4 import BeautifulSoup
from post.create_date_base import SQLApi
import configparser
import re
from post.vk_api_pobeda import VKApi

config = configparser.ConfigParser()
config.read("config.ini")
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

TOP_ITEMS = 5
DOMAIN = "https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/"
filter_apple = config["Filter"]["filter_apple"]


def get_html(url: str, params=None):
    return requests.get(url, headers=HEADERS, params=params)


def write_image(file_name, img) -> bool:
    """Save image to jpg file"""
    try:
        with open(file_name, "wb") as f:
            f.write(img)
    except IOError as error:
        print(error)
        return False
    return True


def get_content(html, chat_id):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all("div", attrs={"card"})
    products = []
    IMAGE_DIR = f'./{chat_id}'
    if os.path.exists(IMAGE_DIR):
        shutil.rmtree(IMAGE_DIR)
    os.mkdir(IMAGE_DIR)
    image_name = 1

    for item in items:
        if len(products) == TOP_ITEMS:
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
        image_path = f'{IMAGE_DIR}/{image_name}.jpg'
        write_image(image_path, photo)
        error = str(photo)
        if re.search('<!DOCTYPE html>', error, re.IGNORECASE):
            continue
        products.append({"title": title,
                         "price": price,
                         "url": url,
                         "url_photo": url_photo,
                         "photo": photo,
                         'image': image_path,
                         })

        image_name += 1
        print(f'Продукт {title} добавлен')
    return products


def post_products(sity, filials, categoriess, chat_id):
    sql = SQLApi()
    url = sql.get_url(sity, filials, categoriess)
    html = get_html(url)
    return get_content(html, chat_id)


def publish_post(products, filial, sity, chat_id):
    vk_api = VKApi()
    photos = [product['image'] for product in products]
    captions = [
        f"{product['title']} \n  Цена: {product['price']} руб\n Ссылка на товар на нашем сайте: {product['url']}"
        for product in products]
    album_id = vk_api.get_album_id()
    vk_api.post_group_wall(photos, captions, filial, sity, album_id=album_id)
    delete_img_dir = f'./{chat_id}'
    try:
        if os.path.exists(delete_img_dir):
            shutil.rmtree(delete_img_dir)
    except OSError as e:
        print("Error: %s : %s" % (delete_img_dir, e.strerror))
