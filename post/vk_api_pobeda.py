# -*- coding: utf-8 -*-
import vk_api
from typing import List
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
login_vk = config["VK"]["login"]
password_vk = config["VK"]["password"]
access_token = {'access_token': '1aa43cddf77e5dc676e0c7f9fbbaf62753d84c87866e97f582aac5f0ce7d88229a01d52c1bf6d7f4d9541',
                'email': 'pobeda.kosmos@gmail.com', 'expires_in': '0', 'user_id': '615022059'}
token_vk = config["VK"]["token_vk"]
owner_id = config["VK"]["owner_id"]
album_name = config["VK_POST"]["album_name"]
filial = {'filial': "Энгельс , улица Космонавтов 19",
          'number': '8 (8453) 53-03-51', }
text_message = f"""Дорогие жители и гости нашего города, мы будем рады вас видеть на нашем филиале ПОБЕДЫ по адресу:
                🏪 {filial['filial']}
                ☎Звоните по интересующим вопросам по тел. {filial['number']}, а лучше всего приходите, будем рады Вас видеть! 😉
                👉Производим самую высокую ОЦЕНКУ 🔥🔥
                👉Онлайн ОЦЕНКУ через наш сайт 🔥🔥
                👉 Самые приятные ЦЕНЫ на товар 🔥🔥
                💥Режим работы: КРУГЛОСУТОЧНО! ⏰
                ‼Бронируйте товар прямо сейчас на сайте 👉👉👉победа-63.рф👈👈👈
                ‼‼‼Так же появилось возможность приобрести товар в наших магазинах в кредит через наш сайт проходите по ссылке‼‼‼
                💥Так-же на нашем филиале вы можете приобрести любой аксессуар для своего смартфона" Чехол, зу, наушники, бронь стёкла, моноподы (селфи палка), aux.💥
                🙀При покупки товара вы получаете баллы. 1 балл равняется рублю. за баллы можно приобрести так же товар на ваш выбор 🙀
                Вся техника абсолютно исправна 😊
                Поможем вам с выбором любой техники под ваши нужды 😉"""


class VKApi:

    def __init__(self):
        self.login = login_vk
        self.password = password_vk
        self.access_token = access_token
        self.token = token_vk
        self.owner_id = owner_id
        self.album_name = album_name
        self.text_message = text_message
        self.vk_session = self.create_session(self.login, self.token)

    def create_session(self, login, token_vk):
        vk_session = vk_api.VkApi(login=login, token=token_vk)
        try:
            vk_session.auth(token_only=True)
            print("Соеденение с вк установленно")
        except vk_api.AuthError as error_connect:
            print(error_connect)
        return vk_session

    def upload_photo(self, photo_path: bytes, caption: str, album_id: str):
        upload = vk_api.VkUpload(self.vk_session)
        vk_photo = upload.photo(photos=photo_path, album_id=album_id,
                                caption=[caption])[0]
        return f'photo{vk_photo["owner_id"]}_{vk_photo["id"]}'

    def post_wall(self, owner_id: int, text_message: str, vk_photos: List[str]):
        vk_photos_id = ",".join(vk_photos)
        vk_post = self.vk_session.method('wall.post', {
            'owner_id': -owner_id,
            'message': text_message,
            'attachments': vk_photos_id  # 'photo615022059_457240069,photo615022059_457240054'
        })
        print("Пост в вк готов")
        return vk_post

    def post_group_wall(self, photos_path: list, captions: list, album_id: str):
        vk_photos_id = [self.upload_photo(photo_path, caption, album_id)
                        for photo_path, caption in zip(photos_path, captions)]
        vk_post = self.post_wall(self.owner_id, self.text_message, vk_photos_id)
        return vk_post

    def get_album_id(self):
        self.vk_session.token = access_token
        photo_albums = self.vk_session.method('photos.getAlbums', {"owner_id": 615022059})
        vk_albums = photo_albums['items']
        for album in vk_albums:
            if album['title'] == self.album_name:
                print('Такой альбом уже имется')
                return album['id']
        album = self.vk_session.method('photos.createAlbum', {"title": self.album_name})
        print('Создал новый альбом')
        return album["id"]
